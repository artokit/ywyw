$(document).ready(function(){

    function closeAlert() {
        const btnClose = $('.alert-message button'),
            alertBlock = $('.alert-message');
        btnClose.on('click', () => {
            alertBlock.css('display','none');
        });
    }
    closeAlert();

    function checkInputBtn() {
        $('.search-container form input').on('keyup', function() {
            let empty = false;
            $('.search-container form input').each(function() {
                empty = $(this).val().length == 0;
            });
            if (empty) {
                $('.search-container form button').attr('disabled', 'disabled');
            } else {
                $('.search-container form button').attr('disabled', false);
            }
        });
    }
    checkInputBtn();

    function toggleCatalog() {
        const btnCatalog = $('.main-menu .btn'),
            listCatalog = $('#menu-container'),
            btnClose = $('.menu-mob-head label');
        if ($(window).width() <= 834) {
            btnCatalog.on('click', (e) => {
                e.preventDefault();
                listCatalog.addClass('active');
                $('body').addClass('open');
            });
            btnClose.on('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                listCatalog.removeClass('active');
                $('body').removeClass('open');
                $('.menu-item-level-1>li').removeClass('active');
            });
        }
    }
    toggleCatalog();

    function openSecondLevelMenu() {
        const listItems = $('.menu-item-level-1>li');
        if ($(window).width() <= 834) {
            listItems.each(function(e) {
                $(this).find('label.name').on('click', (e) => {
                    e.preventDefault();
                    $(this).addClass('active');
                });
                $(this).find('label.go-back').on('click', (e) => {
                    e.preventDefault();
                    e.stopPropagation();
                    $(this).removeClass('active');
                });
            });
        }
    }
    openSecondLevelMenu();

    function toggleMenu() {
        const btnMenu = $('.menu-burger > label'),
            listMenu = $('.menu-burger__wrapper'),
            btnClose = $('.menu-mob-head label');
        if ($(window).width() <= 834) {
            btnMenu.on('click', (e) => {
                e.preventDefault();
                listMenu.addClass('active');
                $('body').addClass('open');
            });
            btnClose.on('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                listMenu.removeClass('active');
                $('body').removeClass('open');
            });
        }
    }
    toggleMenu();

    $(window).on('resize', () => {
        toggleCatalog();
        openSecondLevelMenu();
        toggleMenu();
    });

});




