
jQuery(document).ready(function($) {

    /*----------------------------------------------------*/
    /* Collapse navigation bar
     ------------------------------------------------------ */

    $(document).on('click','.navbar-collapse.in',function(e) {
        if( $(e.target).is('a') && $(e.target).attr('class') != 'dropdown-toggle' ) {
            $(this).collapse('hide');
        }
    });


    /*----------------------------------------------------*/
    /* Smooth Scrolling
     ------------------------------------------------------ */

    $('.smoothscroll').on('click', function (e) {
        e.preventDefault();

        var target = this.hash,
            $target = $(target);

        $('html, body').stop().animate({
            'scrollTop': $target.offset().top
        }, 800, 'swing', function () {
            window.location.hash = target;
        });


    });

    /*----------------------------------------------------*/
    /* Highlight the current section in the navigation bar
     ------------------------------------------------------*/

    var sections = $("section");
    var navigation_links = $("#nav-wrap a");

    sections.waypoint({
        handler: function(direction) {

            var active_section;

            active_section = this.element.id;
            if (direction === "up") {
                active_section = $("#"+active_section).prev().attr('id');
            }

            var active_link = $('#nav-wrap a[href="#' + active_section + '"]');

            navigation_links.parent().removeClass("active");
            active_link.parent().addClass("active");
        },
        offset: '15%'
    });

    /*----------------------------------------------------*/
    /*	Fade In/Out Primary Navigation
     ------------------------------------------------------*/

    $(window).on('scroll', function() {
        var h = $('.logo-section').height();
        var y = $(window).scrollTop();
        var nav = $('#nav-wrap');

        if ( (y > h * 0.1) && (y < h * 0.8) && ($(window).outerWidth() > 768 ) ) {
            nav.fadeOut('fast');
        } else {
            nav.fadeIn('fast');
        }
    });
});