window.scroll({
  top: 0, 
  left: 0, 
  behavior: 'smooth'
});

window.scrollBy({ 
  top: 100, 
  left: 0, 
  behavior: 'smooth' 
});


mybutton = document.getElementById("myBtn");

window.onscroll = function() {scrollFunction()};

function scrollFunction() {
  if (document.body.scrollTop > 10 || document.documentElement.scrollTop > 10) {
    mybutton.style.display = "block";
  } else {
    mybutton.style.display = "none";
  }
}