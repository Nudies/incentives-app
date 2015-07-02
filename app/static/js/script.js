$(document).ready(function(){

  //auto adjust #content left margin depending on nav width.
  var $nav = $('#nav').outerWidth();
  var $content = $('#content');


  if($(window).width() > 768){ //css breakpoint
    $content.css({'margin-left': $nav});
  }
  else{
    $content.css({'margin-left': 0});
  }


  //listen for window resize and adjust again.
  $(window).resize(function(e){
    $nav = $('#nav').outerWidth();
    $content = $('#content');
    if($(window).width() > 768){
      $content.css({'margin-left': $nav});
      $('#nav').css({'display': 'block'});
    }
    else{
      $content.css({'margin-left': 0});
      $('#nav').css({'display': 'none'});

      $('#mobile-nav').on('click', function(e){
        var $dispType = $('#nav').css('display');
        if($dispType === 'none'){
          $('#nav').css({'display': 'block'});
        }
        else if($dispType === 'block'){
          $('#nav').css({'display': 'none'});
        }
      });
    }
  });


  //Mobile nav toggle
  if($(window).width() < 769){
    $('#mobile-nav').on('click', function(e){
      var $dispType = $('#nav').css('display');
      if($dispType === 'none'){
        $('#nav').css({'display': 'block'});
      }
      else if($dispType === 'block'){
        $('#nav').css({'display': 'none'});
      }
    });
  }


  $('#date').datepicker();
});
