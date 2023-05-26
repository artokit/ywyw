$(document).ready(function(){

    function toggleFocus() {
        $('.order_form_box').on('click', function () {
            $(this).find('.num_card').focus();
        });
    }
    toggleFocus();

    function toggleFilter() {
        const btnFilter = $('.call_filter, .filter_btn_call'),
            listFilter = $('.filter_main, .review_panel, .analytics-head'),
            btnClose = $('.close_filter');

        btnFilter.on('click', (e) => {
            e.preventDefault();
            listFilter.addClass('active');
            btnFilter.addClass('active');
            $('body').addClass('open');
        });
        btnClose.on('click', (e) => {
            e.preventDefault();
            e.stopPropagation();
            listFilter.removeClass('active');
            btnFilter.removeClass('active');
            $('body').removeClass('open');
        });
    }

    toggleFilter();

    function toggleSortDesk() {
        $('.catalog-label').each(function() {
            $(this).on('click', (e) => {
                e.preventDefault();
                $(this).next('.catalog_sort_box').toggleClass('active');
                $(this).toggleClass('active');
            });
        });
    }
    toggleSortDesk();

    function toggleFilterLk() {
        const btnFilter = $('.lk .review_panel_custom .lk_btn_call'),
            listFilter = $('.form_preorder_wrap'),
            btnClose = $('.close_filter');

        btnFilter.on('click', (e) => {
            e.preventDefault();
            listFilter.addClass('active');
            btnFilter.addClass('active');
            $('body').addClass('open');
        });
        btnClose.on('click', (e) => {
            e.preventDefault();
            e.stopPropagation();
            listFilter.removeClass('active');
            btnFilter.removeClass('active');
            $('body').removeClass('open');
        });
    }
    toggleFilterLk();

});