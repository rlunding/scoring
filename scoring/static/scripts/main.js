// A super basic inflection library to pluralize words.
var pluralize = function (word, count) {
    if (count === 1) { return word; }

    return word + 's';
};

// Add a delay before executing something to prevent hammering the server.
var typewatch = function () {
    var timer = 0;

    return function (callback, ms) {
        clearTimeout(timer);
        return timer = setTimeout(callback, ms);
    };
}();

// Format datetimes in multiple ways, depending on which CSS class is set on it.
var momentjsClasses = function () {
    var $fromNow = $('.from-now');
    var $shortDate = $('.short-date');
    var $longDate = $('.long-date');

    $fromNow.each(function (i, e) {
        (function updateTime() {
            var time = moment($(e).data('datetime'));
            $(e).text(time.fromNow());
            $(e).attr('title', time.format('MMMM Do YYYY, h:mm:ss a Z'));
            setTimeout(updateTime, 1000);
        })();
    });

    $shortDate.each(function (i, e) {
        var time = moment($(e).data('datetime'));
        $(e).text(time.format('MMM Do YYYY'));
        $(e).attr('title', time.format('MMMM Do YYYY, h:mm:ss a Z'));
    });

    $longDate.each(function (i, e) {
        var time = moment($(e).data('datetime'));
        $(e).text(time.format('MMM Do YYYY, h:mm:ss'));
        $(e).attr('title', time.format('MMMM Do YYYY, h:mm:ss a Z'));
    });
};

// Bulk delete items.
var bulkDelete = function () {
    var selectAll = '#select_all';
    var checkedItems = '.checkbox-item';
    var colheader = '.col-header';
    var selectedRow = 'warning';
    var updateScope = '#scope';
    var bulkActions = '#bulk_actions';

    $('body').on('change', checkedItems, function () {
        var checkedSelector = checkedItems + ':checked';
        var itemCount = $(checkedSelector).length;
        var pluralizeItem = pluralize('item', itemCount);
        var scopeOptionText = itemCount + ' selected ' + pluralizeItem;

        if ($(this).is(':checked')) {
            $(this).closest('tr').addClass(selectedRow);

            $(colheader).hide();
            $(bulkActions).show();
        }
        else {
            $(this).closest('tr').removeClass(selectedRow);

            if (itemCount === 0) {
                $(bulkActions).hide();
                $(colheader).show();
            }
        }

        $(updateScope + ' option:first').text(scopeOptionText);
    });

    $('body').on('change', selectAll, function () {
        var checkedStatus = this.checked;

        $(checkedItems).each(function () {
            $(this).prop('checked', checkedStatus);
            $(this).trigger('change');
        });
    });
};

// Pagination related stuff
var pagination = function () {

    // Prevent users from clicking on disabled items
    $('li.disabled a').click(function(e) {
        e.preventDefault();
        //do other stuff when a click happens
    });
};

// Deal with displaying datetimepicker for Reservations.
var reservations = function () {
    var start_date = $('#start_date');
    var end_date = $('#end_date');

    if (start_date) {
        start_date.datetimepicker({
            format: 'YYYY-MM-DD HH:mm:ss',
            //minDate: moment(),
            stepping: 15,
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
            stepping: 15,
            useCurrent: false,
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
    momentjsClasses();
    bulkDelete();
    pagination();
    reservations();
});