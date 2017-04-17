
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

    // Format datetimes in multiple ways, depending on which CSS class is set on it.
    var momentjsClasses = function () {
        var $fromNow = $('.from-now');
        var $shortDate = $('.short-date');
        var $longDate = $('.long-date');

        $fromNow.each(function (i, e) {
            (function updateTime() {
                var time = moment($(e).data('datetime'));
                $(e).text(time.fromNow());
                $(e).attr('title', time.format('MMMM Do YYYY, h:mm:ss a Z'));
                setTimeout(updateTime, 1000);
            })();
        });

        $shortDate.each(function (i, e) {
            var time = moment($(e).data('datetime'));
            $(e).text(time.format('MMM Do YYYY'));
            $(e).attr('title', time.format('MMMM Do YYYY, h:mm:ss a Z'));
        });

        $longDate.each(function (i, e) {
            var time = moment($(e).data('datetime'));
            $(e).text(time.format('MMM Do YYYY, h:mm:ss'));
            $(e).attr('title', time.format('MMMM Do YYYY, h:mm:ss a Z'));
        });
    };
    momentjsClasses();

});