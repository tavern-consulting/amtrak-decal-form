$( document ).ready(function() {

	$('.datepicker').datepicker();
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
                $('.finish').removeClass('hide');
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
    function removeHighlight($element) {
        $element.removeClass('modal-highlight');
    }
    function addHighlight($element) {
        $element.addClass('modal-highlight');
    }
    $('#border-type select').change(function() {
        var thisValue = $(this).val();
        var $noneRow = $('.modal-border-none');
        var $singleRow = $('.modal-border-single');
        var $doubleRow = $('.modal-border-double');
        removeHighlight($noneRow);
        removeHighlight($singleRow);
        removeHighlight($doubleRow);
        if(thisValue == "None") {
            $('#border-thickness').addClass('hide');
            $('#border-color').addClass('hide');
            addHighlight($noneRow);
        } else {
            $('#border-thickness').removeClass('hide');
            $('#border-color').removeClass('hide');
            if (thisValue == 'Single') {
                addHighlight($singleRow);
            } else {
                addHighlight($doubleRow);
            }
        }
    });
    $('#id_html').editable({
        inlineMode: false,
        fontList: ['Arial', 'Times New Roman', 'Tahoma'],
        buttons: ['bold', 'italic', 'fontSize', 'fontFamily', 'color', 'align', 'insertImage', 'undo', 'redo']
    })
});
