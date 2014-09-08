$( document ).ready(function() {
    var $errorMessage = $('#error-alert');
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
                    $errorMessage.addClass('hide');
                    $('#decal-spec-form').removeClass('hide');
                    $('#user-info-form').addClass('hide');
                $('a.continue').addClass('hide');
                $('a.finish').removeClass('hide');
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
                    $errorMessage.removeClass('hide');
                }
            }
        });
    });
    $('a.finish').click(function(e) {
        console.log('test');
        e.preventDefault();
        $('form').submit();
    });
    $('#border-type select').change(function() {
        if($(this).val() == "None") {
            $('#border-thickness').addClass('hide');
            $('#border-color').addClass('hide');
        } else {
            $('#border-thickness').removeClass('hide');
            $('#border-color').removeClass('hide');
        }
    });
});
