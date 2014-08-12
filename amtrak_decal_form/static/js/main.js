$( document ).ready(function() {
    $('a.continue').click(function(e) {
        e.preventDefault();
        $.ajax({
            type: "POST",
            url: "validate_user_info/",
            data: $("form").serialize(),
            success: function(data) {
                if (data.success) {
                    $('#decal-spec-form').removeClass('hide');
                    $('#user-info-form').addClass('hide');
                } else {
                    $('.form-errors').html(data.errors);
                }
            }
        });
    });
});
