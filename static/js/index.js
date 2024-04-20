function myFunction() {
    var x = document.getElementById("myTopnav");
    if (x.className === "topnav") {
      x.className += " responsive";
    } else {
      x.className = "topnav";
    }
  }



  // marquee

  $(document).ready(function(){
    $('.customer-logos').slick({
        slidesToShow: 6,
        slidesToScroll: 1,
        autoplay: true,
        autoplaySpeed: 1500,
        arrows: false,
        dots: false,
        pauseOnHover: false,
        responsive: [{
            breakpoint: 768,
            settings: {
                slidesToShow: 4
            }
        }, {
            breakpoint: 520,
            settings: {
                slidesToShow: 3
            }
        }]
    });
});



// popup

// document.addEventListener('DOMContentLoaded', function() {
//   setTimeout(function() {
//     var popup = document.getElementById('image-popup');
//     popup.style.display = 'block';
//   }, 5000); // 10,000 milliseconds = 10 seconds
// });


// start 

document.addEventListener("DOMContentLoaded", function() {
  setTimeout(showPopup, 2000);
});

function showPopup() {
  var popupContainer = document.querySelector(".popup-container");
  popupContainer.style.display = "flex";
}

// JavaScript code to close the pop-up when the close button is clicked
var closeButton = document.querySelector(".close-button");
closeButton.addEventListener("click", function() {
  var popupContainer = document.querySelector(".popup-container");
  popupContainer.style.display = "none";
});


// end 






