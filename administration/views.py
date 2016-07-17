# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.conf import settings
from django.shortcuts import redirect 
import pdb
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import  Group
import os
from administration.models import User, VerifyCode
import json
import random
import string
from django.utils import timezone
from .e_mail import Email, EmailEx
import re
import threading
"""
layer 2 start
"""

from .form import UploadPortrainForm, GroupForm, UserForm
from django.contrib.auth import logout

"""
layer 2 end
"""

from django.contrib import auth

#from socialoauth import SocialSites,SocialAPIError	

import logging

from mobile.detectmobilebrowsermiddleware import DetectMobileBrowser

dmb     = DetectMobileBrowser()

logger = logging.getLogger(settings.LOGGER);

#validate email format
EMAIL_REGEX = re.compile(r'[^@]+@[^@]+\.[^@]+')

#list all user portraits in a page
def list_users(request):
    isMble  = dmb.process_request(request)
    
    context = {  }
     
    #get user list
    user_list = User.objects.all().order_by('-date')
           
    context = { 'user_list':user_list }
    if isMble:
        return render(request, 'map2family/m_users.html', context)
    else:
        return render(request, 'map2family/users.html', context)


#list all user for administrator to manage
def admin_list_users(request):
    isMble  = dmb.process_request(request)
    
    context = {  }
     
    #get user list
    user_list = User.objects.all().order_by('-date')
           
    context = { 'user_list':user_list }
    if isMble:
        return render(request, 'admin_user/m_userslist.html', context)
    else:
        return render(request, 'admin_user/userslist.html', context)
    
@csrf_exempt
def portrait(request):
    #response for the social site user login
    #socialsites = SocialSites(settings.SOCIALOAUTH_SITES) 
    if request.GET.get('state',None)=='socialoauth':
        
        auth.logout(request) #logout first
         
        access_code = request.GET.get('code')
         
        qq_object = socialsites.get_site_object_by_name('qq')
        try:
            qq_object.get_access_token(access_code)
            fake_email = qq_object.uid+"@qq.com"
            try:
                #user exist
                User.objects.get(email=fake_email)
            except User.DoesNotExist:
                #user doesn't exist, need add it first
                social_user = User(name=qq_object.name,email=fake_email,head_portrait=qq_object.avatar,social_user_status=1,social_site_name=1,social_user_id=qq_object.uid)
                social_user.set_password(qq_object.uid)
                social_user.date = timezone.now()
                social_user.save()
            
            user = auth.authenticate(email=fake_email, password=qq_object.uid)    
            request.user = user
            auth.login(request, user)
            return HttpResponseRedirect("/")
        except SocialAPIError as e:
            print e  
    isMobile = dmb.process_request(request)
     
    
    result = {} 
    if request.method == 'POST':
        usesr = request.user
        
        #remove the old portraint
        ''' 
        if 'media' in usesr.head_portrait.name[1:]:
            oldportraint = os.path.join(settings.MEDIA_ROOT, usesr.head_portrait.name[7:])
        else:
            oldportraint = os.path.join(settings.MEDIA_ROOT, usesr.head_portrait.name[1:])
         
        if os.path.isfile(oldportraint):
            os.remove(oldportraint)
            #rename the fake portrait 
            if 'media' in usesr.fake_head_portrait.name[1:]:
                  os.rename(os.path.join(settings.MEDIA_ROOT,usesr.fake_head_portrait.name[7:]), oldportraint)
            else:
                  os.rename(os.path.join(settings.MEDIA_ROOT,usesr.fake_head_portrait.name[1:]), oldportraint)
        
	'''
	usesr.head_portrait     = usesr.fake_head_portrait
	usesr.is_head_portrait  = True
	usesr.save()
	
	result['status'] = 'OK'
	result['msg']    = '头像上传成功...' 
	return HttpResponse(json.dumps(result), content_type='application/json')
	 
    else:
        form = UploadPortrainForm()
        form.fields['portrain'].label = '点击上传头像'
        admin_granted = has_admin_perm(request.user)
        
        context = {
            'form':form.as_ul(),
            'admin_granted':admin_granted,
            }
        if isMobile:
            return render(request, 'admin_user/m_change_portrait.html', context)
        else:
            return render(request, 'admin_user/change_portrait.html', context)
 
		
@csrf_exempt
def upload_fake_portrait(request):
    isMobile = dmb.process_request(request)
    
    result = {}		 
    if request.method == 'POST':
	form = UploadPortrainForm(request.POST, request.FILES)
	if form.is_valid(): 
	    usesr = request.user

            #remove the old portraint 
            if 'media' in usesr.head_portrait.name[1:]:
                oldportraint = os.path.join(settings.MEDIA_ROOT, usesr.head_portrait.name[7:])
            else:
                oldportraint = os.path.join(settings.MEDIA_ROOT, usesr.head_portrait.name[1:])
            
            
            if os.path.isfile(oldportraint):
                os.remove(oldportraint)
                 
	    
	    code    = ''.join(random.choice(string.lowercase + string.digits) for i in range(4))
	    filename = handle_uploaded_file(request.FILES['portrain'], str(usesr.id)+'_'+ code)
	    
            logger.debug('1',extra={'user': request.user.get_full_name()})    
	    #usesr.is_head_portrait = False	 
	    usesr.head_portrait = filename.replace('\\', '/')
	    usesr.is_head_portrait  = True
	    usesr.save()
	    result['status'] = 'OK'
	    result['msg']    = '头像上传成功...'
	    result['file']    = filename  
	else:
            result['status'] = 'ERROR'
	    result['msg']    = '请先选择图片..'
             
    else:
	result['status'] = 'ERROR'
	result['msg']    = '请先选择图片..'
  
    return HttpResponse(json.dumps(result), content_type='application/json')

def handle_uploaded_file(f, userid):
	#with open(os.path.join(settings.MEDIA_ROOT, 'portrait'), 'wb+') as destination: 
	filename = str(userid) + '.png' 
	logger.debug('handle_uploaded_file',extra={'user': str(userid)})  
	with open(os.path.join(settings.MEDIA_ROOT, 'portrait', filename), 'wb+') as destination:
		for chunk in f.chunks() :
			destination.write(chunk)
        logger.debug('handle_uploaded_file saved',extra={'user':str(userid)})  
	return os.path.join(settings.MEDIA_URL, 'portrait', filename)

def grouplist(request):
    isMobile = dmb.process_request(request)
   
     
    #get group list
    group_list = Group.objects.all()
        
    context = { 'group_list':group_list }
    if isMobile:
        return render(request, 'admin_user/m_grouplist.html', context)
    else:
        return render(request, 'admin_user/grouplist.html', context)

			 
def newgroup(request):
    isMobile = dmb.process_request(request)
    if  request.user.is_anonymous():
        pass
    
    if  not has_admin_perm(request.user):
        context = {
                     'not_granted' : True, 
                  }
    else: 
        if request.method == 'POST':
            form = GroupForm(request.POST)
            
            if form.is_valid(): 
                new_group = form.save() 
                form = GroupForm()
                context = {
                     'form'       :  form,
                     'saved'      :  True,
                     'validate'   :  True,
                  }
            else:
                #invalide form
                form = GroupForm()
                context = {
                     'form'       : form,
                     'validate'   : False,
                  }
        else: 
            form = GroupForm()
            context = {
                     'form'       : form,
                     'validate'   :  True,
                  }
    if isMobile:    
        return render(request, 'admin_user/m_group.html', context)
    else:
        return render(request, 'admin_user/m_group.html', context)

def modify_group(request, groupid):
    isMobile = dmb.process_request(request)
    if  request.user.is_anonymous():
        pass
    
    

    if  not has_admin_perm(request.user):
        context = {
                     'not_granted' : True, 
                  }
    else:
        try:
            group = Group.objects.get(pk=groupid)
            if request.method == 'POST':
                form = GroupForm(request.POST, instance=group) 
                if form.is_valid(): 
                    form.save() 
                    context = { 
                         'form'       :  form,
                         'saved'      :  True,
                         'validate'   :  True,
                      }
                else:
                    #invalide form
                    form = GroupForm()
                    context = {
                         'form'       : form,
                         'validate'   : False,
                      }
            else: 
                form = GroupForm(instance = group)
                context = {
                         'form'       : form,
                         'validate'   :  True,
                      }
        except Group.DoesNotExist:
            context = {
                         'usernotexist'   :  True,
                      }
        
    
    if isMobile:    
        return render(request, 'admin_user/m_group.html', context)
    else:
        return render(request, 'admin_user/m_group.html', context)

def has_admin_perm(user):
    '''
       if a user has permission to manage user, group and permission
       if has, return True, else return False
    '''
    if user.is_superuser:
        return True
    else:
        return user.has_perm('administration.admin_management') 


def modify_user(request, userid):
    isMobile = dmb.process_request(request)
    if  request.user.is_anonymous():
        pass #return comm.redirect_login_path(isMobile, request)
    
  
    if  not has_admin_perm(request.user):
        context = {
                     'not_granted' : True, 
                  }
    else:
        try:
            user = User.objects.get(pk=userid)
            if request.method == 'POST':
                form = UserForm(request.POST, instance=user) 
                if form.is_valid(): 
                    form.save() 
                    context = { 
                         'form'       :  form,
                         'saved'      :  True,
                         'validate'   :  True,
                      }
                else:
                    #invalide form
                    form = UserForm()
                    context = {
                         'form'       : form,
                         'validate'   : False,
                      }
            else: 
                form = UserForm(instance = user)
                context = {
                         'form'       : form,
                         'validate'   :  True,
                      }
        except User.DoesNotExist:
            context = {
                         'usernotexist'   :  True,
                      }
        
    
    if isMobile:    
        return render(request, 'admin_user/m_change_user.html', context)
    else:
        return render(request, 'admin_user/change_user.html', context)


@csrf_exempt
def get_email_verify_code(request):
    result={} 
    if request.method == 'POST':
        if 'email' in request.POST:
            email       = request.POST["email"]
            result={} 
            if not EMAIL_REGEX.match(email):
                result['status'] = '1'
                result['err_msg'] = '亲， 电子邮件格式不正确哦 !' 
            else: 
                    try:
                        obj = User.objects.get(email__exact=email)
                        result['status'] = '2'
                        result['err_msg'] = '亲， 这个邮箱已经注册过了你可以找回密码' 
                    except User.DoesNotExist: 
                        email_insance = EmailEx()
                        #get verify code
                        code    = ''.join(random.choice(string.lowercase + string.digits) for i in range(5))
                        Subject = 'Jason  注册邮箱验证码' 
                        content = '您好， 欢迎您注册Jason AD， 您的邮箱验证码是：  ' + code
                        
                        logger.info('Start to send email', extra={'user':'anonymous'})
                        try:
                            email_insance.send_text_email(Subject, content, email)
                            
                            try:
                                verify_code = VerifyCode.objects.get(email__exact = email, type ='0')
                                verify_code.code = code
                                verify_code.save()
                            except VerifyCode.DoesNotExist:
                                verify_code = VerifyCode(email=email, code=code, type ='0')
                                verify_code.save()
                                
                            result['status'] = '3'
                            result['err_msg'] = '验证码已发至您的邮箱中， 请到邮箱中查看您的验证码!'    
                        except   Exception, e:
                            result['status'] = '4'
                            result['err_msg'] = '发送邮件的过程中发生错误： '+ e 
        else:
            result['status'] = '5'
            result['err_msg'] = '非法参数， 你在干什么 !' 
    else:
         result['status'] = '5'
         result['err_msg'] = '非法参数， 你在干什么 !'
        
    return HttpResponse(json.dumps(result), content_type = 'application/json')

@csrf_exempt
def user_register(request):
 
    dmb     = DetectMobileBrowser() 
    
    content = {'page':'user_register',
	'page_title':'注册为新会员'} 
     
    if request.method == 'POST':
        result = save_user(request)
         
        content['email']      = request.POST["email"]
        content['verifycode'] = request.POST["verifycode"]
        content['name']       = request.POST["name"]
        content['msg']        = result['err_msg']
        content['status']     = result['status']  
         
         
    return render(request, 'admin_user/register.html', content)
 
def save_user(request): 
    result={} 
    if request.method == 'POST':
        if 'email' in request.POST and 'verifycode' in request.POST and 'name' in request.POST and  'pwd_1' in request.POST \
                and  'pwd_2' in request.POST:

            user_email  = request.POST["email"]
            verifycode  = request.POST["verifycode"]
            name        = request.POST["name"]
            
            pwd_1       = request.POST["pwd_1"]
            pwd_2       = request.POST["pwd_2"]
           
            #validate email format
            EMAIL_REGEX = re.compile(r'[^@]+@[^@]+\.[^@]+')
            if not EMAIL_REGEX.match(user_email):
                result['status'] = '0'
                result['err_msg'] = '邮箱格式不正确 !'  
                return result
                
            if pwd_1 != pwd_2:
                result['status'] = '1'
                result['err_msg'] = '您两次输入的密码不一致， 请重新输入 。 ' 
                return result
 
            if len(pwd_1) < 6:
                result['status'] = '2'
                result['err_msg'] = '密码不能少于6位...' 
                return result
            #验证用户名
            try:  
                obj = User.objects.get(name__exact=name)
                result['status'] = '9'
                result['err_msg'] = '这个用户昵称已被占用，请重新输入... ' 
                return result
            except User.MultipleObjectsReturned:
                result['status'] = '9'
                result['err_msg'] = '这个用户昵称已被占用，请重新输入... ' 
                return result
            except  User.DoesNotExist:
                pass  
             
            try:
                obj = User.objects.get(email__exact=user_email)
                result['status'] = '3'
                result['err_msg'] = '亲, 这个邮箱已经注册过了你是不是把密码忘了 ? ' 
            except User.DoesNotExist:
                try:
                    verifycode_instance = VerifyCode.objects.get(email__exact = user_email)
                    if verifycode_instance.code == verifycode:
                        try:
                            user = User(name= name, email = user_email, date=timezone.now(), password=pwd_1, is_active=True)
                            user.set_password(pwd_1)   
                            user.save()
                            verifycode_instance.delete()
                            result['status'] = '4'
                            result['err_msg'] = '注册成功， 你可以登录了， 开始使用吧 !'
                                                  
                            Subject = 'New user in map2family'
                            email_content = 'New user: '+ user_email
                            
			    t_send_email =  threading.Thread(target=send_email, args=[Subject, email_content, settings.SUPPORTOR_EMAIL])
			    t_send_email.start()
			      
                        except Exception, e:
                            result['status'] = '5'
                            result['err_msg'] = '保存用户失败! ERROR: ' + str(e) 
                    else:
                        result['status'] = '6'
                        result['err_msg'] = '验证码不对哦， 请重新查看您的验证码!' 
                except VerifyCode.DoesNotExist: 
                    result['status'] = '7'
                    result['err_msg'] = '请先获取邮箱验证码!' 
        else:
            result['status'] = '8'
            result['err_msg'] = '参数错误， 非法的输入 !'
        return result 
        
def send_email(subject, content, receiver):
    email_insance = EmailEx()
    print 'Thread for sending email'
    #get verify code
    try:
        email_insance.send_text_email(subject, content, receiver)
    except   Exception, e:
        print '发送邮件的过程中发生错误： '+ str(e)

@csrf_exempt    
def login(request):
    
    if 'email' in request.POST and 'password' in request.POST:
            auth.logout(request)
            u_email       = request.POST['email']
            password      = request.POST['password']
            user = auth.authenticate(email=u_email, password=password)
            next_url = request.POST.get('next')
            context ={}
            if user:
                # User is valid.  Set request.user and persist user in the session
                # by logging the user in.
                request.user = user
                auth.login(request, user)
                # redirect to the value of next if it is entered, otherwise
		# to settings.APP_WEB_PC_LOGIN_URL
		 
		if next_url:
                    #after login, return to the previous page, but if the previous page is logout, 
                    #then return to the host page
                    if 'logout' not in str(next_url):
                         return redirect(next_url)
                
                #if isMble:
                return HttpResponseRedirect("/")
                #return render(request, 'home.html', context)
                #else:
                #        return render(request, 'map2family/hostpage.html', context)
            else:
                try:
                    user_instance = User.objects.get(email = u_email)
                    msg = '登录失败，密码错误...'
                except User.DoesNotExist:
                    msg = '登录失败，用户未注册...'
                    
                context = {'next':next_url,
                           'error':msg,
                           'email':u_email}
                return render(request, 'admin_user/login.html', context)
                #if isMble: 
		#	return render(request, 'registration/m_login.html', context)
		#else:  
		#	return render(request, 'registration/login.html', context)
		    
    else:
                next_url = request.GET.get('next')
                email = request.POST.get('email')
		context = {'next':next_url,
                           'error':'',
                           'email':email}
                return render(request, 'admin_user/login.html', context)
		#if isMble: 
		#	return render(request, 'registration/m_login.html', context)
		#else:  
		#	return render(request, 'registration/login.html', context)
def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/")

@csrf_exempt
def find_password(request):
    #StatComm.count_page_traffic(request)
    isMble  = dmb.process_request(request) 
    content = {'page':'find_password',
	'page_title':'重置密码'}
    
    if request.method == 'POST':
        result = {}
        result =  reset_password(request)
        content['status'] = result['status']
        content['msg']    = result['msg']
    if isMble:
        return render(request, 'admin_user/m_user_register.html', content)
    else:
        return render(request, 'admin_user/register.html', content)
             

def reset_password(request):
    result = {}
    if request.method == 'POST':
            if 'email' in request.POST and 'verifycode' in request.POST and 'pwd_1' in request.POST  and 'pwd_2' in request.POST:
                email           = request.POST["email"]
                verifycode      = request.POST["verifycode"]
                pwd_1       = request.POST["pwd_1"]
                pwd_2       = request.POST["pwd_2"]
            
                #validate email format
                EMAIL_REGEX = re.compile(r'[^@]+@[^@]+\.[^@]+')
                if not EMAIL_REGEX.match(email):
                    result['status'] = 'ERROR'
                    result['msg'] = '邮箱格式不正确 !'  
                    return result
                    
                if pwd_1 != pwd_2:
                    result['status'] = 'ERROR'
                    result['msg'] = '您两次输入的密码不一致， 请重新输入 。 ' 
                    return result
                
                if len(pwd_1) < 6:
                    result['status'] = 'ERROR'
                    result['msg'] = '密码不能少于6位...' 
                    return result
                   
                try:
                    verify_code = VerifyCode.objects.get(email__exact = email, code=verifycode, type ='1')
                    try:
                        user    = User.objects.get(email = email)
                        user.set_password(pwd_1)
                        user.save()
                        verify_code.delete()
                        
                        #send email
                        email_insance = EmailEx()
                        Subject = '密码已重置' 
                        content = '您好, 您在AD Jason中的密码已重置成功. <br />若不是您本人操作请立即登录重新修改...'
                        try:
                            email_insance.send_text_email(Subject, content, email)
                            result['status'] = 'OK'
                            result['msg'] = '密码重置成功...' 
                        except   Exception, e: 
                            result['status'] = 'ERROR'
                            result['msg'] = '发送邮件的过程中发生错误： '+ e
                    except User.DoesNotExist:
                        result['status'] = 'ERROR'
                        result['msg'] = '您输入的邮箱用户不存在， 请重试... !'
                except VerifyCode.DoesNotExist:
                    result['status'] = 'ERROR'
                    result['msg'] = '验证码与邮箱不匹配, 请检查邮件和验证码... !'
            else:
                result['status']  = 'ERROR'
                result['msg'] = '非法参数， 你在干什么 !'
                
    else:
        result['status'] = 'ERROR'
        result['msg'] = '非法参数， 你在干什么 !'
        
    return result     

@csrf_exempt
def get_reset_pwd_verify_code(request):
    
                        
    result = {}
    if request.method == 'POST':
        if 'email' in request.POST:
            email       = request.POST["email"]
            
            if not EMAIL_REGEX.match(email):
                result['status'] = 'ERROR'
                result['err_msg'] = '电子邮件格式不正确 !'
                return HttpResponse(json.dumps(result), content_type='application/json')
            else: 
                try:
                    user    = User.objects.get(email = email)
                except User.DoesNotExist:
                    result['status'] = 'ERROR'
                    result['err_msg'] = '用户不存在,该用户尚未注册... !'
                    return HttpResponse(json.dumps(result), content_type='application/json')  
                        
                email_insance = EmailEx()
                #get verify code
                code    = ''.join(random.choice(string.lowercase + string.digits) for i in range(4))
                Subject = '重置密码验证码' 
                content = '您好， 您正在重置您在AD Jason的密码，输入正确的验证码后，即可修改您的密码。  验证码是：  ' + code + ' <br />感谢您使用AD Jason。'
                try: 
                    email_insance.send_text_email(Subject, content, email)
                except   Exception, e: 
                    result['status'] = 'ERROR'
                    result['err_msg'] = '发送邮件的过程中发生错误： '+ e
                    return HttpResponse(json.dumps(result), content_type='application/json')
                try:
                    verify_code = VerifyCode.objects.get(email__exact = email, type ='1')
                    verify_code.code = code
                    verify_code.save()
                except VerifyCode.DoesNotExist:
                    verify_code = VerifyCode(email=email, code=code, type ='1')
                    verify_code.save()
                result['status'] = 'OK'
                result['msg'] = '验证码已发至您的邮箱中， 请到邮箱中查看您的验证码 !'
                return HttpResponse(json.dumps(result), content_type='application/json')    
                 
        else:
            result['status'] = 'ERROR'
            result['err_msg'] = '非法参数， 你在干什么 !'
            return HttpResponse(json.dumps(result), content_type='application/json')  
    else:
        result['status'] = 'ERROR'
        result['err_msg'] = '非法参数， 你在干什么 !'
        return HttpResponse(json.dumps(result), content_type='application/json')  
