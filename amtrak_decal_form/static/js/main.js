$( document ).ready(function() {
    $('a.continue').click(function(e) {
        e.preventDefault();
        $('.pane-2').removeClass('hide');
        $('.pane-1').addClass('hide');
    });
});
