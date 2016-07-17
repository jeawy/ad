$(document).ready(function() {
    $('#i_upload').prop('disabled', 'disabled');
    var pattern = /\.(jpe?g|png|gif|bmp)$/i;
      
    $("#id_portrain").change(function(e) {

        e.preventDefault();
        $('.div_err').empty();
        var file = $('#id_portrain').get(0).files[0];

        if (!pattern.test(file.name)) {
            $('.div_err').append('<label class="err_label" >你选择的不是图片，请选择图片...</label>'); //
            return;
        }
        if (file == null)
            $().message("请选择图片 !");
        else {
            var dataForm = new FormData($('#id_user_form').get(0));
            $.ajax({
                url: '/user/upload_fake_portrait/',
                type: 'POST',
                enctype: 'multipart/form-data',
                data: dataForm,
                processData: false,
                contentType: false,
                success: function(data) {
                    if (data['status'] == 'OK') {
                        data['file'] = data['file'].replace('\\', '/');
                        $('#id_portrait_upload').css("background-image", "url(" + data['file'] + ")");
                        $('#id_user_portrait').css("background-image", "url(" + data['file'] + ")");
                        $('#mark').val('1');
                        $().message(data['msg']);
                        var delay = 3000;
                        setTimeout(function(){window.location.href="/";}, delay);
                    }
                    else {
                        $('.div_err').append('<label class="err_label" >' + data['msg'] + '</label>'); //
                    }
                }
            });
        } 
    });

    $("#i_upload").click(function(e) {
        e.preventDefault();
        $.post('/user/portrait/', {}, function(data) {
            $().message(data['msg']);
            var delay = 3000; //delay in milliseconds
            setTimeout(function() { window.location="/" }, delay);
        });
    });
});