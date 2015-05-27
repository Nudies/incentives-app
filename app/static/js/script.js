$(document).ready(function(){

  //auto adjust #content left margin depending on nav width.
  $nav = $('#nav').outerWidth();
  $content = $('#content');
  
  if($(window).width() > 768){ //css breakpoint
    $content.css({'margin-left': $nav});
  }
  else{
    $content.css({'margin-left': 0});
  }
  
  //listen for window resize and adjust again.
  $(window).resize(function(e){
    if($(window).width() > 768){
      $content.css({'margin-left': $nav});
    }
    else{
      $content.css({'margin-left': 0});
    }
  });
  
  $('#date').datepicker();
  
  //Mobile nav
  if($(window).width() < 769){
    $('#mobile-nav').on('click', function(e){
      $('#nav').css({'display': 'block'});
    });
  }
});