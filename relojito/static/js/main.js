$(function(){
    Mousetrap.bind('a',
        function() {
            window.location.href = '/task/new/';
        }, 'keyup');

    if ($('#profile-calendar').length > 0) {
        $('#profile-calendar').fullCalendar({
            defaultView: 'basicWeek',
            height: 250,
            lang: 'es',
            header: {
                left: 'prev, next today',
                center: 'title',
                right: 'month, basicWeek, basicDay'
            },
            eventSources: [
                '/tasks/json/' + user_id,
                '/total_tasks/' + user_id
            ],
            eventRender: function(event, element) {
                var tooltip = event.title;
                $(element).attr("data-original-title", tooltip)
                $(element).tooltip({
                    container: "body"
                })
            }
        });
    }

    $('#calendar').fullCalendar({
        defaultView: 'basicWeek',
        lang: 'es',
        header: {
            left: 'prev, next today',
            center: 'title',
            right: 'month, basicWeek, basicDay'
        },
        eventSources: [
            '/tasks/json/',
            '/total_tasks/'
        ],
        eventRender: function(event, element) {
            var tooltip = event.title;
            $(element).attr("data-original-title", tooltip)
            $(element).tooltip({
                container: "body"
            })
        }
    });

    $('#calendar-new-task').fullCalendar({
        defaultView: 'basicDay',
        lang: 'es',
        header: {
            left: 'prev, next today',
            center: 'title',
            right: 'month, basicWeek, basicDay'
        },
        eventSources: [
            '/tasks/json/',
            '/total_tasks/'
        ]
    });

    $('.table').dataTable({
        "language": {
            "url": "//cdn.datatables.net/plug-ins/a5734b29083/i18n/Spanish.json"
        },
        "iDisplayLength": 10,
        "bStateSave": true,
        "sDom": 'T<"clear">lfrtip',
        "oTableTools": {
            "aButtons": [
                "print",
                "csv",
                "pdf"
            ],
            "sSwfPath": "/static/swf/copy_csv_xls_pdf.swf"
        }
    });

    // time fields
    $('.dtpicker.date').datetimepicker({
        pickTime: false
    });
    $('.dtpicker.datetime').datetimepicker({
        minuteStepping: 30,
        sideBySide: true
    });

    $('.color_field').spectrum({
        showInput: true,
        showPalette: true,
        preferredFormat: "hex",
        palette: [
            ["#000", "#444", "#666", "#999", "#ccc", "#eee", "#f3f3f3", "#fff"],
            ["#f00", "#f90", "#ff0", "#0f0", "#0ff", "#00f", "#90f", "#f0f"],
            ["#f4cccc", "#fce5cd", "#fff2cc", "#d9ead3", "#d0e0e3", "#cfe2f3", "#d9d2e9", "#ead1dc"],
            ["#ea9999", "#f9cb9c", "#ffe599", "#b6d7a8", "#a2c4c9", "#9fc5e8", "#b4a7d6", "#d5a6bd"],
            ["#e06666", "#f6b26b", "#ffd966", "#93c47d", "#76a5af", "#6fa8dc", "#8e7cc3", "#c27ba0"],
            ["#c00", "#e69138", "#f1c232", "#6aa84f", "#45818e", "#3d85c6", "#674ea7", "#a64d79"],
            ["#900", "#b45f06", "#bf9000", "#38761d", "#134f5c", "#0b5394", "#351c75", "#741b47"],
            ["#600", "#783f04", "#7f6000", "#274e13", "#0c343d", "#073763", "#20124d", "#4c1130"]
        ]
    });
});
