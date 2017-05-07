// Deal with displaying datetimepicker for Reservations.
var match = function () {
    var start_date = $('#start_date');
    var end_date = $('#end_date');

    if (start_date) {
        start_date.datetimepicker({
            format: 'YYYY-MM-DD HH:mm:ss',
            //minDate: moment(),
            //stepping: 15,
            showTodayButton: true,
            icons: {
                time: 'fa fa-clock-o',
                date: 'fa fa-calendar',
                up: 'fa fa-arrow-up',
                down: 'fa fa-arrow-down',
                previous: 'fa fa-chevron-left',
                next: 'fa fa-chevron-right',
                clear: 'fa fa-trash'
            }
        });
    }

    if (end_date) {
        end_date.datetimepicker({
            format: 'YYYY-MM-DD HH:mm:ss',
            //stepping: 15,
            useCurrent: false,
            showTodayButton: true,
            icons: {
                time: 'fa fa-clock-o',
                date: 'fa fa-calendar',
                up: 'fa fa-arrow-up',
                down: 'fa fa-arrow-down',
                previous: 'fa fa-chevron-left',
                next: 'fa fa-chevron-right',
                clear: 'fa fa-trash'
            }
        });
    }
    if (start_date && end_date) {
        start_date.on('dp.change', function (e) {
           end_date.data("DateTimePicker").minDate(e.date);
        });
        end_date.on('dp.change', function (e) {
           start_date.data("DateTimePicker").maxDate(e.date);
        });
    }
};


var add_buttons_to_score_fields = function () {
    var score_field_1 = $('#score_1');
    var score_field_2 = $('#score_2');
    if (score_field_1.length) {
        add_buttons(score_field_1);
    }
    if (score_field_2.length) {
        add_buttons(score_field_2);
    }

    var start_button = $('<input class="btn btn-lg btn-default" type="button" id="now_start" value="Now"/>');
    $('#start_date').parent().append(start_button);
    $('#now_start').click(function () {
        $('#start_date').data('DateTimePicker').date(new Date());
    });

    var end_button = $('<input class="btn btn-lg btn-default" type="button" id="now_end" value="Now"/>');
    $('#end_date').parent().append(end_button);
    $('#now_end').click(function () {
        $('#end_date').data('DateTimePicker').date(new Date());
    });

    $('#submit').addClass('btn-lg');
};

var add_buttons = function (score_field) {
    var values = [1, 10, 100, -1, -10, -100];

    for (var i = 0; i < values.length; i++) {
        (function () {
            var value = values[i];
            var sign = value > 0 ? '+' : '';
            var id = score_field.attr('id') + '_button_' + values[i];
            var button = $('<input class="btn btn-lg btn-default" type="button" id="'+id+'" value="'+sign + value+'"/>');
            var div = score_field.parent();
            div.append(button);

            $("#"+id).click(function () {
                score_field.val(parseInt(score_field.val(), 10) + value);
            });
        })();
    }
};

// Initialize everything when the browser is ready.
$(document).ready(function() {
    match();
    add_buttons_to_score_fields();
});