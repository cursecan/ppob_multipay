// JS
$('.ui.sidebar').sidebar();
$('#headbars').click(function() {
    $('.ui.sidebar').sidebar('toggle');
});
$('.ui.dropdown').dropdown({
    action: 'nothing'
});
$('.ui.product.dropdown').dropdown();