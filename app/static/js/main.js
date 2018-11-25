$('.nav-item.navbar-nav > li').on('click', function(e) {
    $('.nav-item.navbar-nav > li').removeClass('active');
    $(this).addClass('active');
});
