$(document).ready(function () {

    /*--usable place start--*/ 
    
  
      $(".switchButtonOuter").bind("click", function () {
          $(this).parents(".loginOrSignupField").toggleClass("signup_ON");
  
          setTimeout(function () {
  
              if ($(".loginOrSignupField").hasClass("signup_ON")) {
                  $("#submit").attr("value", "Sign up");
              } else {
                  $("#submit").attr("value", "Join");
              }
  
              $("#email,#submit,.socialButton.twitter")
                  .animate({
                      "left": "-10px"
                  }, 50)
                  .animate({
                      "left": "10px"
                  }, 50)
                  .animate({
                      "left": "-5px"
                  }, 50)
                  .animate({
                      "left": "5px"
                  }, 50)
                  .animate({
                      "left": "0"
                  }, 50);
              $("#password,.socialButton.facebook,.socialButton.googleplus")
                  .animate({
                      "left": "10px"
                  }, 50)
                  .animate({
                      "left": "-10px"
                  }, 50)
                  .animate({
                      "left": "5px"
                  }, 50)
                  .animate({
                      "left": "-5px"
                  }, 50)
                  .animate({
                      "left": "0"
                  }, 50);
  
              if ($(".loginOrSignupField").hasClass("signup_ON")) {
                  $("#rememberMeField").css("display", "none");
              } else {
                  $("#rememberMeField").css("display", "block");
              }
  
          }, 200);
  
      });
  
  
      $("#submit").bind("mouseover", function () {
          if ($("#email").val() == "") {
              $("#email")
                  .animate({
                      "left": "-10px"
                  }, 50)
                  .animate({
                      "left": "10px"
                  }, 50)
                  .animate({
                      "left": "-5px"
                  }, 50)
                  .animate({
                      "left": "5px"
                  }, 50)
                  .animate({
                      "left": "0"
                  }, 50);
          }
          if ($("#password").val() == "") {
              $("#password")
                  .animate({
                      "left": "10px"
                  }, 50)
                  .animate({
                      "left": "-10px"
                  }, 50)
                  .animate({
                      "left": "5px"
                  }, 50)
                  .animate({
                      "left": "-5px"
                  }, 50)
                  .animate({
                      "left": "0"
                  }, 50);
          }
      });
  
  
      setTimeout(function () {
  
          $(".loginOrSignupField").css({
              "opacity": "1",
              "-webkit-transform": "translateY(-50%) translateX(-50%) scale(1.008)",
              "-moz-transform": "translateY(-50%) translateX(-50%) scale(1.008)",
              "-ms-transform": "translateY(-50%) translateX(-50%) scale(1.008)",
              "-o-transform": "translateY(-50%) translateX(-50%) scale(1.008)",
              "transform": "translateY(-50%) translateX(-50%) scale(1.008)"
          });
  
      }, 500);
  
  
    /*--usable place end--*/
    
  
  
      $(".normal,.mode01,.mode02").on("click", function () {
          if ($(this).is(".normal")) {
              $("body").removeClass("mode01_ON mode02_ON");
          } else if ($(this).is(".mode01")) {
              $("body").removeClass("mode02_ON").addClass("mode01_ON");
          } else if ($(this).is(".mode02")) {
              $("body").removeClass("mode01_ON").addClass("mode02_ON");
          }
      });
  
  });