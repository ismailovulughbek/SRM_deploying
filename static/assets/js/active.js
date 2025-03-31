/*****************************************
    Template Name: Business Press HTML5 Teamplate
    Description: This is a HTML5 Business Template
    Author: WpOcean
    Version: 1.0
******************************************/
/******************************************
[  Table of contents  ]
*****************************************
    01. Mobile Menu
    02. Sticky Menu
	03. OWl Slider 
	04. OWl Carousel Testimonial
	05. Countdown
    06. Wow js
    07. ScrollUp
	09. preloader
	
	
 
*****************************************
[ End table content ]
******************************************/

(function ($) {
    "use strict";
    
     // 1. Mobile Menu
    $('.main-menu nav').meanmenu({
        meanScreenWidth: "991",
        meanMenuContainer: '.mobile-menu'
    });

    

    // 2. Sticky Menu
    $(window).on('scroll', function () {
        var scroll = $(window).scrollTop();
        if (scroll < 10) {
            $(".header").removeClass("navbar-fixed-top");
        } else {
            $(".header").addClass("navbar-fixed-top");
        }
    });

    // 3. OWl Slider 
    $(".slide-active").owlCarousel({
            items: 1,
            nav: true,
            dots: false,
            autoplay: true,
            loop: true,
            navText: ["<i class='fa fa-angle-left'></i>", "<i class='fa fa-angle-right'></i>"],
            mouseDrag: false,
            touchDrag: false,
        });
        
        $(".slide-active").on("translate.owl.carousel", function(){
            $(".slide-caption h2 , .slide-caption-2 h2, .slide-caption p, .slide-caption-2 p").removeClass("animated fadeInUp").css("opacity", "0");
            $(".slide-caption .slide-btn, .slide-caption-2 .slide-btn").removeClass("animated fadeInDown").css("opacity", "0");
        });
        
        $(".slide-active").on("translated.owl.carousel", function(){
            $(".slide-caption h2, .slide-caption-2 h2, .slide-caption p , .slide-caption-2 p").addClass("animated fadeInUp").css("opacity", "1");
            $(".slide-caption .slide-btn ,.slide-caption-2 .slide-btn").addClass("animated fadeInDown").css("opacity", "1");
        });
    
    
    //4. OWl Carousel Testimonial
	if ($('.testimonial-active').length) {
		$('.testimonial-active').owlCarousel({
			loop:true,
			margin:50,
			nav:true,
			smartSpeed: 700,
			autoplay: 5000,
			navText: [ '<span class="fa fa-angle-left"></span>', '<span class="fa fa-angle-right"></span>' ],
			responsive:{
				0:{
					items:1
				},
				480:{
					items:1
				},
				768:{
					items:2
				},
				800:{
					items:2
				},
				1024:{
					items:2
				}
			}
		});    		
	}
    
    

   // 5. Counter Up


//    CUSTOMIZATION BY (UI) START

    // $('.counter').counterUp();

//    CUSTOMIZATION BY (UI end)


    // 6. Wow js
    new WOW().init();
    
    // 7. ScrollUp
    $.scrollUp({
        scrollText: '<i class="fa fa-long-arrow-up"></i>',
        easingType: 'linear',
        scrollSpeed: 900,
        animation: 'fade'
    });
    
    

    //8. preloader
    $(window).on('load', function () {
        $('.preloader-wave-effect').fadeOut();
        $('#preloader-wrapper').delay(150).fadeOut('slow');
    });






}(jQuery));