$(document).ready(function(){

  //auto adjust #content left margin depending on nav width.
  $nav = $('#nav').outerWidth();
  $content = $('#content');
  
  $content.css({'margin-left': $nav});
  
  //listen for window resize and adjust again.
  $(window).resize(function(e){
    $content.css({'margin-left': $nav});
  });
  
  $('#date').datepicker();
});