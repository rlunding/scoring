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

// Initialize everything when the browser is ready.
$(document).ready(function() {
    match();
});