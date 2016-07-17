$(document).ready(function(){
      $('.btn-concern').click(function(){
            var appid = $('#appinfoid').val();
            $.post('/center/add_like_app/', {appid:appid}, function(data){
                  $().message(data['msg']);
            })
            
      });
});
