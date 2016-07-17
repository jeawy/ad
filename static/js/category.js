$(document).ready(function(e){
      $('.li-category').click(function(e){
           var $current = $(this);
           var category = $current.find('.a-category').attr('data-filter');
           
           $('.li-category').each(function(i, obj){
               $(obj).removeClass('active');
           });
           $('.hid-category').val(category);
           $current.addClass('active');
           $('.search-form').submit();
      });
      var default_category = $('.hid-category').val();
      if (default_category != "")
      {
            $('.li-category').each(function(i, obj){
                $(obj).removeClass('active');
            });
            $('.li-category').each(function(i, obj){
                  if($(obj).find('.a-category').attr('data-filter').indexOf(default_category) >= 0)
                  $(obj).addClass('active');
            });
      }
});