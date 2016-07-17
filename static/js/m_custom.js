(function($){ 
    var clicked = true;
    $('.overlay-container').click(function(e){
      e.stopPropagation();
      var id = $(this).find('.hid_creative_id').val();
      var hid_creative_url = $('.hid_creative_url').val();
      
      $('.div_description_holder').empty();
      if(clicked )
      {     clicked = false;
            $.get('/get_creative_info', {id:id}, function(data){
             
            var app = $.parseJSON(data.serialized_obj)[0]['fields'].ad_app;
            var icon_url60 = $.parseJSON(data.app_obj)[0]['fields'].icon_url60;
            var title      = $.parseJSON(data.app_obj)[0]['fields'].title;
            
            var current_version      = $.parseJSON(data.app_obj)[0]['fields'].current_version;
            var category             = $.parseJSON(data.app_obj)[0]['fields'].category;
            var description          = $.parseJSON(data.app_obj)[0]['fields'].description;
            var seller               = $.parseJSON(data.app_obj)[0]['fields'].seller;
             
             
            var width     = $.parseJSON(data.serialized_obj)[0]['fields'].width;
            var height    = $.parseJSON(data.serialized_obj)[0]['fields'].height;
            var filesize  = $.parseJSON(data.serialized_obj)[0]['fields'].filesize;
            var first_seen = data['first'];
             
            //$.parseJSON(data.serialized_obj)[0]['fields'].first_seen;
            var last_seen  = data['last'];
            //$.parseJSON(data.serialized_obj)[0]['fields'].last_seen;
            var url_md5    = $.parseJSON(data.serialized_obj)[0]['fields'].url_md5;
            var file_ext   = $.parseJSON(data.serialized_obj)[0]['fields'].file_ext;
            
            
            
            var filename   = url_md5+'-' + id;
            
            var image_url = $.parseJSON(data.serialized_obj)[0]['fields'].image_url;
            var video_url = $.parseJSON(data.serialized_obj)[0]['fields'].video_url;
            
       
            
            var network_count = data['network_obj'].length;
            var net_html_name = '';
            var net_html_logo = '';
           
            creative_url  = hid_creative_url + filename;
            if (file_ext.length > 0)
            {
                  creative_url += '.' + file_ext;
            }
            var type= '';
            if (image_url.length > 0)
            {
                  type = '图片';  
                  image_url  = creative_url;
            } 
            else
            {
                  type = '视频';  
            }
            
            if (title.length > 40)
            {
                  title = title.substring(0, 40);
            }
            var height_right = window.innerHeight;
            height_right = height_right*0.8;
            var width_ratio  =  window.innerWidth/parseInt(width);
            var height_ratio =  window.innerHeight/parseInt(height);

            $('.div_description_holder .overlay-container-strength').empty();
            var html='<div class="modal fade" id="project-'+id+'" tabindex="-1" role="dialog" aria-labelledby="project-1-label" aria-hidden="true">'+
                              '<div class="modal-dialog modal-lg">'+
                                    '<div class="modal-content">'+ 
                                    '<div class="modal-body">'+ 
                                          '<div class="row">'+
                                                '<div class="col-md-6 col-md-6-left">'+
                                                '<span class="button-wrap popup-close">'+
                                                      '<button class="button button-circle">'+
                                                            '<i class="fa fa-close"></i>'+
                                                      '</button>'+
                                                      '</span>'+
                                                '<ul>'+
                                                      '<li>'+
                                                            '<div class="bg_top_caontainer">'+
                                                            '<div class="bg-top-left">'+
                                                                  '<a href="/app_detail/'+app+'" ><img class="thumbnail_footer_left" src="'+icon_url60+'" alt=""></a>'+
                                                            '</div>'+
                                                            '<div class="bg-top-right">'+
                                                                  '<label class="bg_version" >版本：'+current_version+'</label> '+ 
                                                                  '<label class="bg_version bg_catogary" >分类：'+category+'</label>'+
                                                                  '<br/>'+
                                                                  '<label class="bg_corpname">'+seller+'</label>'+
                                                                  '</div>'+
                                                            '</div>'+
                                                      '</li>'+
                                                      '<li>'+
                                                            '<div class="bg_top_caontainer">'+
                                                            '<div class="bg-app-title">'+
                                                                  '<strong>'+title+'</strong>'+
                                                            '</div>'+
                                                            '<div class="bg-category-right">'+
                                                                  
                                                            '</div>'+
                                                             
                                                            '</div>'+ 
                                                      '</li>'+
                                                      '<hr>';

                                                      html += '<li>'+
                                                      '<div class="col-md-6 col-md-6-right big-image big-image-'+id+'" ';//
                                                            
                                                      if (image_url.length > 0)
                                                      {
                                                            //add css style
                                                            html += 'style="background:url('+image_url+') no-repeat center center;';
                                                            if (height_right < parseInt(height) || parseInt(width) > window.innerWidth)
                                                            {
                                                                  html +='background-size:contain; background-color : #999" >';
                                                            }
                                                            else
                                                            {
                                                                  html +='background-color : #999" >'; 
                                                            } 
                                                      }    
                                                      else
                                                      {
                                                            var video_width = parseInt(width)*width_ratio;
                                                            var video_height = parseInt(height)*width_ratio;
                                                            html +='><video class="ad-video" width="'+video_width+'" height="'+video_height+'" controls>'+
                                                                        '<source src="'+creative_url+'" type="video/mp4">'+
                                                                        '<source src="'+creative_url+'" type="video/ogg">'+
                                                                        'Your browser does not support the video tag.'+
                                                                        '</video>';
                                                      }   
                                                            
                                                      html += '</div>'+
                                                      '</li><hr>';

                                                      html +='<li>'+
                                                            '<div class="bg_desc">'+description+
                                                            '</div>'+
                                                      '</li>'+
                                                      '<hr>'+ 
                                                      '<li>'+
                                                      '<table class="popup-table">'+
                                                      '<tr>'+
                                                      '</tr>'+
                                                          '<td>'+'<label class="bg_version" >'+type+'规格：'+width+'x'+height+'</label>'+
                                                          '</td>'+
                                                          '<td>'+  '<label class="bg_version" >文件大小：'+filesize+' B  </label>'+
                                                          '</td>'+
                                                      '<tr>'+
                                                           '<td>'+'<label class="bg_version" >首次推送：'+first_seen+'</label>'+ 
                                                          '</td>'+
                                                          '<td>'+  '<label class="bg_version" >最近看到：'+last_seen+'</label>'+
                                                          '</td>'+
                                                      '</tr>'+
                                                      '<tr>'+
                                                          '<td>'+'<label class="bg_version" >广告类型：'+type+'</label>'+ 
                                                          '</td>'+
                                                          '<td>'+  
                                                          '</td>'+
                                                      '</tr>'+
                                                      '</table>'+ 
                                                      '</li>'+
                                                      '<hr>';
                                                       if (network_count > 0)
                                                            {
                                                                  html += '<li class="li_network_lb">广告网络：</li>';
                                                                  for(var i=0; i <network_count; i++ )
                                                                  {
                                                                        html += '<li class="li_network">'+
                                                                        '<div class="li_network_div_left">'+
                                                                        '<img class="network_logo" src="'+data['network_url']+data['network_obj'][i].logo_url+'" alt="">'+
                                                                        '</div>';
                                                                         
                                                                  }
                                                                  
                                                            }
                                                      
                                                      
                                                html +='</ul>'+
                                                '</div>';
                                              

                                         var last = '</div>'+
                                    '</div> '+
                                    '</div>'+
                              '</div>'+
                        '</div>'  ;
                        
                        html += last;
                        //$('.div_description_holder').append(html);
                        $('body').append(html);
                        //$('.modal').modal('toggle');
                        $('.modal').modal('show');
                       

                       if (parseInt(height) < parseInt(width))
                       {
                              $('.col-md-6-right').each(function(e){
                                    $(this).css({'height': (parseInt(height)*width_ratio).toString()+'px'});
                              });
                       }
                       else{
                              $('.col-md-6-right').each(function(e){
                                    $(this).css({'height': (height_right+5).toString()+'px'});
                              });
                       }
                         /*      
                              $('.col-md-6-left').each(function(e){
                                    $(this).css({'height': height_right.toString()+'px'});
                              });
                        */
                              height_right = height_right*0.3;
                              $('.bg_desc').css({'height': height_right.toString()+'px'});
                        
                        clicked = true;
                         
            });
            }
      //
   });
   
   $(document).on('hidden.bs.modal', function () {
    // do something…
    //$('.div_description_holder').empty();
    $('.modal').remove();
    $('.modal-backdrop').remove();
   });
   $(document).on('click', '.popup-close .button-circle',  function(e){
      //$('.div_description_holder').empty();
      //$('.modal').modal('hide');
      $('.modal').remove();
      $('.modal-backdrop').remove();
   });
})(this.jQuery);