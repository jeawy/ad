
$(document).ready(function() {
    $('#div_register').hide();
    var pattern = /^([\.a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+(\.[a-zA-Z0-9_-])+/;
    /***************************************************************************
    submit new user informations section
    *************************************************************************/
    $('#id_submit_new_user').click(function(e) {
        e.preventDefault();

        var page = $.trim($("#page").val());
        $('.div_err').empty();
        var email = $.trim($('#id_email').val());
        if (email == '') {
            $('.div_err').append('<label class="err_label"  >电子邮件不能为空...</label>'); //
            return;
        }
        var verifycode = $.trim($('#id_verify_code').val());
        if (verifycode == '') {
            $('.div_err').append('<label class="err_label" >验证码不能为空...</label>'); //
            return;
        }
      
        var pwd_1 = $.trim($('#id_pwd_1').val());
        var pwd_2 = $.trim($('#id_pwd_2').val());
        if (pwd_1 == '' || pwd_2 == '') {
            $('.div_err').append('<label class="err_label" >请输入密码...</label>'); //
            return;
        }
        if (pwd_1 != pwd_2) {
            $('.div_err').append('<label class="err_label" >两次输入的密码不一致...</label>'); //
            return;
        }
        var data_user_Form = new FormData($('#id_user_form').get(0));
        $('#id_submit_new_user').prop('disabled', 'disabled');
       

        $.get('/base/reset_password', { email: email, verifycode: verifycode, pwd: pwd_1 }, function(data) {
            var str = data.toString();
            if (data['status'] == 'OK') {
                $().message(data['msg']);
                var delay = 3000; //delay in milliseconds
                setTimeout(function() { window.location.href = '/login'; }, delay);
            }
            else {
                $('.div_err').append('<label class="err_label" >' + data['err_msg'] + '</label>'); //
            }
            $('#id_submit_new_user').removeAttr('disabled');

        });
    }); //id_pwd_1
    $('#id_pwd_1').change(function(e) {
        e.preventDefault();
        var pwd = $.trim($('#id_pwd_1').val());
        $('.div_err').empty();
        if (pwd.length < 6) {
            $('.div_err').append('<label class="err_label" >密码不能少于6位...</label>'); //
            return;
        }

    })

    /***************************************************************************
    validate the uniqueness of email for find pwd function
    *************************************************************************/
   // $('#id_get_verify_code_fpwd').prop('disabled','disabled');
    $('#id_get_verify_code_fpwd').click(function(e) {
        e.preventDefault();
        $('.div_err').empty()
        var email = $('#id_email').val();
        email = $.trim(email);
        if (email == '') {
            $('.div_err').append('<label class="err_label" >电子邮箱不能为空...</label>'); //add input box;
            return
        }
        if (!pattern.test(email)) {
            $('.div_err').append('<label class="err_label" >电子邮箱格式不正确...</label>'); //add input box;
            return
        }
        $('#id_get_verify_code_fpwd').prop('disabled', 'disabled');
        $.post('/base/get_reset_pwd_verify_code', { email: email }, function(data) {
            if (data['status'] == 'OK') {
                $('.div_err').append('<label class="err_label" >' + data['msg'] + '</label>'); //
                $("#div_register").show();
            }
            else {
                $('.div_err').append('<label class="err_label" >' + data['err_msg'] + '</label>'); //
            }
            $('#id_get_verify_code_fpwd').removeAttr('disabled');

        });

    })
});