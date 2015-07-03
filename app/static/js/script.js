$(document).ready(function(){

  $(".nav li").on("click", function() {
    $(".nav li").removeClass("active");
    $(this).addClass("active");
  });

  $('#date').datepicker();

});
