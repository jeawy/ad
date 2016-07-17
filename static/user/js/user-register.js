
$(document).ready(function() {
    $('#div_register').hide();
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
        var name = "";
        if (page == "user_register") {
            name = $.trim($('#id_name').val());
            if (name == '') {
                $('.div_err').append('<label class="err_label" >姓名不能为空...</label>'); //
                return;
            }
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

        $.ajax({
            url: '/base/save_user',
            type: 'POST',
            data: data_user_Form,
            processData: false,
            contentType: false,
            success: function(data) {
                if (data['status'] == '4') {
                    $().message(data['suc_msg']);
                    var delay = 3000; //delay in milliseconds
                    setTimeout(function() { window.location.href = '/user/portrait/'; }, delay);
                }
                else {
                    $('.div_err').append('<label class="err_label" >' + data['err_msg'] + '</label>'); //
                }
                $('#id_submit_new_user').removeAttr('disabled');
            }
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
    validate the uniqueness of email
    *************************************************************************/
    $('#id_get_verify_code').click(function(e) {
        e.preventDefault();
         
        $('.div_err').empty()
        var email = $('#id_email').val();
        email = $.trim(email);
        if (email == '') {
            $('.div_err').append('<label class="err_label" >电子邮箱不能为空...</label>'); //add input box;
            return
        }
        $.post('/base/get_email_verify_code', { email: email }, function(data) {

            if (data['status'] == '3')
            {
                $('#div_register').show();
            }

            $('.div_err').append('<label class="err_label" >' + data['err_msg'] + '</label>'); //add input box;

        });
    });
});