$( document ).ready(function() {
    $('input').focus(function() {
        $(this).removeClass('validation-error');
    });
    $('input').change(function() {
        $(this).removeClass('validation-error');
    });
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
                $('a.continue').removeClass('continue').addClass('finish').text('Finish');
                } else {
                    for (var key in data.errors) {
                        if (data.errors.hasOwnProperty(key)) {
                            var element = $('[name*="' + key + '"]');
                            var errorMessage = data.errors[key][0];
                            element.addClass('validation-error');
                            element.attr('title', errorMessage);
                            element.tooltip();
                        }
                    }
                    $('.form-errors').html(data.errors);
                }
            }
        });
    });
});
