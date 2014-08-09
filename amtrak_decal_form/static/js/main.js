$( document ).ready(function() {
    $('a.continue').click(function(e) {
        e.preventDefault();
        $.ajax({
            type: "POST",
            url: "validate_user_info/",
            data: $("form").serialize(),
            success: function(data) {
                if (data.success) {
                    $('.pane-2').removeClass('hide');
                    $('.pane-1').addClass('hide');
                }
            }
        });
    });
});
