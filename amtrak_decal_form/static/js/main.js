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
        var $noneRow = $('.modal-border-type-none');
        var $singleRow = $('.modal-border-type-single');
        var $doubleRow = $('.modal-border-type-double');
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
    $('#border-thickness select').change(function() {
        var thisValue = $(this).val();
        var $veryThin = $('.modal-border-thickness-very-thin');
        var $thin = $('.modal-border-thickness-thin');
        var $medium = $('.modal-border-thickness-medium');
        var $thick = $('.modal-border-thickness-thick');
        var $veryThick = $('.modal-border-thickness-very-thick');
        removeHighlight($veryThin);
        removeHighlight($thin);
        removeHighlight($medium);
        removeHighlight($thick);
        removeHighlight($veryThick);
        if(thisValue == "5px") {
            addHighlight($veryThin);
        } else if(thisValue == '10px') {
            addHighlight($thin);
        } else if(thisValue == '15px') {
            addHighlight($medium);
        } else if(thisValue == '20px') {
            addHighlight($thick);
        } else if(thisValue == '25px') {
            addHighlight($veryThick);
        }
    });
    $('#id_rolling_stock_or_not').change(function() {
        var value = $(this).find(':checked').val();
        var $fleetType = $('#fleet-type');
        if (value === 'Rolling Stock') {
            $fleetType.removeClass('hide');
        } else {
            $fleetType.addClass('hide');
        }
    });
    $('#id_placard_or_decal').change(function() {
        var value = $(this).find(':checked').val();
        console.log(value);
        var $requiredSubstrate = $('#required-substrate');
        if (value === 'Placard') {
            $requiredSubstrate.addClass('hide');
        } else {
            $requiredSubstrate.removeClass('hide');
        }
    });
    $('#id_html').editable({
        inlineMode: false,
        fontList: ['Arial', 'Times New Roman', 'Tahoma'],
        buttons: ['bold', 'italic', 'fontSize', 'fontFamily', 'color', 'align', 'insertImage', 'undo', 'redo']
    })
});
