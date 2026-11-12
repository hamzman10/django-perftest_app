
(function ($) {
    "use strict";

    // ==========================================
    // 1. Spinner
    // ==========================================
    var spinner = function () {
        setTimeout(function () {
            if ($('#spinner').length > 0) {
                $('#spinner').removeClass('show');
            }
        }, 100);
    };

    spinner();


    // ==========================================
    // 2. Back to top button
    // ==========================================
    $(window).on('scroll', function () {
        if ($(this).scrollTop() > 300) {
            $('.back-to-top').fadeIn('slow');
        } else {
            $('.back-to-top').fadeOut('slow');
        }
    });

    $('.back-to-top').on('click', function () {
        $('html, body').animate({
            scrollTop: 0
        }, 1500, 'easeInOutExpo');

        return false;
    });


    // ==========================================
    // 3. Sidebar Toggler
    // ==========================================
    $('.sidebar-toggler').on('click', function () {
        $('.sidebar, .content').toggleClass('open');
        return false;
    });


    // ==========================================
    // 4. Progress Bar
    // ==========================================
    if ($.fn.waypoint) {

        $('.pg-bar').waypoint(function () {

            $('.progress .progress-bar').each(function () {

                $(this).css(
                    "width",
                    $(this).attr("aria-valuenow") + '%'
                );

            });

        }, {
            offset: '80%'
        });

    }


    // ==========================================
    // 5. Calendar
    // ==========================================
    if ($.fn.datetimepicker && $('#calender').length > 0) {

        $('#calender').datetimepicker({
            inline: true,
            format: 'L'
        });

    }


    // ==========================================
    // 6. Testimonials Carousel
    // ==========================================
    if ($.fn.owlCarousel) {

        $('.testimonial-carousel').each(function () {

            $(this).owlCarousel({
                autoplay: true,
                smartSpeed: 1000,
                items: 1,
                dots: true,
                loop: true,
                nav: false
            });

        });

    }


    // ==========================================
    // 7. Chart.js
    // ==========================================
    if (typeof Chart !== "undefined") {

        Chart.defaults.color = "#6C7293";
        Chart.defaults.borderColor = "#000000";


        // Fonction commune de création des graphiques
        function createChart(selector, config) {

            var canvas = $(selector).get(0);

            // Vérifier si le Canvas existe
            if (!canvas) {
                return null;
            }

            // Vérifier si le contexte Canvas existe
            var ctx = canvas.getContext('2d');

            if (!ctx) {
                return null;
            }

            return new Chart(ctx, config);
        }


        // ======================================
        // 7.1 Worldwide Sales Chart
        // ======================================
        createChart('#worldwide-sales', {

            type: 'bar',

            data: {

                labels: [
                    '2016', '2017', '2018',
                    '2019', '2020', '2021', '2022'
                ],

                datasets: [

                    {
                        label: 'USA',

                        data: [15, 30, 55, 65, 60, 80, 95],

                        backgroundColor: 'rgba(235, 22, 22, .7)'
                    },

                    {
                        label: 'UK',

                        data: [8, 35, 40, 60, 70, 55, 75],

                        backgroundColor: 'rgba(235, 22, 22, .5)'
                    },

                    {
                        label: 'AU',

                        data: [12, 25, 45, 55, 65, 70, 60],

                        backgroundColor: 'rgba(235, 22, 22, .3)'
                    }

                ]
            },

            options: {
                responsive: true
            }

        });


        // ======================================
        // 7.2 Sales & Revenue Chart
        // ======================================
        createChart('#salse-revenue', {

            type: 'line',

            data: {

                labels: [
                    '2016', '2017', '2018',
                    '2019', '2020', '2021', '2022'
                ],

                datasets: [

                    {
                        label: 'Sales',

                        data: [15, 30, 55, 45, 70, 65, 85],

                        backgroundColor: 'rgba(235, 22, 22, .7)',

                        fill: true
                    },

                    {
                        label: 'Revenue',

                        data: [99, 135, 170, 130, 190, 180, 270],

                        backgroundColor: 'rgba(235, 22, 22, .5)',

                        fill: true
                    }

                ]
            },

            options: {
                responsive: true
            }

        });


        // ======================================
        // 7.3 Single Line Chart
        // ======================================
        createChart('#line-chart', {

            type: 'line',

            data: {

                labels: [
                    50, 60, 70, 80, 90,
                    100, 110, 120, 130, 140, 150
                ],

                datasets: [

                    {
                        label: 'Sales',

                        fill: false,

                        backgroundColor: 'rgba(235, 22, 22, .7)',

                        data: [
                            7, 8, 8, 9, 9,
                            9, 10, 11, 14, 14, 15
                        ]
                    }

                ]
            },

            options: {
                responsive: true
            }

        });


        // ======================================
        // 7.4 Single Bar Chart
        // ======================================
        createChart('#bar-chart', {

            type: 'bar',

            data: {

                labels: [
                    'Italy', 'France',
                    'Spain', 'USA', 'Argentina'
                ],

                datasets: [

                    {
                        backgroundColor: [

                            'rgba(235, 22, 22, .7)',
                            'rgba(235, 22, 22, .6)',
                            'rgba(235, 22, 22, .5)',
                            'rgba(235, 22, 22, .4)',
                            'rgba(235, 22, 22, .3)'

                        ],

                        data: [55, 49, 44, 24, 15]
                    }

                ]
            },

            options: {
                responsive: true
            }

        });


        // ======================================
        // 7.5 Pie Chart
        // ======================================
        createChart('#pie-chart', {

            type: 'pie',

            data: {

                labels: [
                    'Italy', 'France',
                    'Spain', 'USA', 'Argentina'
                ],

                datasets: [

                    {
                        backgroundColor: [

                            'rgba(235, 22, 22, .7)',
                            'rgba(235, 22, 22, .6)',
                            'rgba(235, 22, 22, .5)',
                            'rgba(235, 22, 22, .4)',
                            'rgba(235, 22, 22, .3)'

                        ],

                        data: [55, 49, 44, 24, 15]
                    }

                ]
            },

            options: {
                responsive: true
            }

        });


        // ======================================
        // 7.6 Doughnut Chart
        // ======================================
        createChart('#doughnut-chart', {

            type: 'doughnut',

            data: {

                labels: [
                    'Italy', 'France',
                    'Spain', 'USA', 'Argentina'
                ],

                datasets: [

                    {
                        backgroundColor: [

                            'rgba(235, 22, 22, .7)',
                            'rgba(235, 22, 22, .6)',
                            'rgba(235, 22, 22, .5)',
                            'rgba(235, 22, 22, .4)',
                            'rgba(235, 22, 22, .3)'

                        ],

                        data: [55, 49, 44, 24, 15]
                    }

                ]
            },

            options: {
                responsive: true
            }

        });

    }


})(jQuery);
