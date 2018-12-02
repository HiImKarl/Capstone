window.onload = function () {
  var videos = document.getElementsByTagName('video')
  var video1 = videos[0];
  var video2 = videos[1];
  var video3 = videos[2];
  var video4 = videos[3];
  document.getElementById('btn-two').style.display = 'None';
  document.getElementById('btn-three').style.display = 'None';
  document.getElementById('btn-four').style.display = 'None';

  video1.onended = function(e) {
    var button = document.getElementsByClassName("btn-one")[0]
    button.style.display = "block";
  }
  video2.onended = function(e){
    var button = document.getElementById("btn-two");
    button.style.display = "block";
  }
  video3.onended = function(e){
    var button = document.getElementById("btn-three");
    button.style.display = "block";
  }
  video4.onended = function(e){
    var button = document.getElementById("btn-four");
    button.style.display = "block";
  }
};

var curOpen;
$(document).ready(function() {
  curOpen = $('.step')[0];
  $('.next-btn').on('click', function() {
    let cur = $(this).closest('.step');
    let next = $(cur).next();
    $(cur).addClass('minimized');
    setTimeout(function() {
      $(next).removeClass('minimized');
      curOpen = $(next);
    }, 400);
  });
  
  $('.close-btn').on('click', function() {
    let cur = $(this).closest('.step');
    $(cur).addClass('minimized');
    curOpen = null;
  });
  
  $('.step .step-content').on('click' ,function(e) {
    e.stopPropagation();
  });
  
  $('.step').on('click', function() {
    if (!$(this).hasClass("minimized")) {
      curOpen = null;
      $(this).addClass('minimized');
    }
    else {
      let next = $(this);
      if (curOpen === null) {
        curOpen = next;
        $(curOpen).removeClass('minimized');
      }
      else {
        $(curOpen).addClass('minimized');
        setTimeout(function() {
          $(next).removeClass('minimized');
          curOpen = $(next);
        }, 300);
      }
    }
  });
})
