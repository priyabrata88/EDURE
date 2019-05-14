$(document).ready(function() {
    function e() {
        $("#addNewEvent").modal("hide"), $("#fullcalendar").fullCalendar("renderEvent", {
            title: $("#inputTitleEvent").val(),
            start: new Date($("#start").val()),
            end: new Date($("#end").val()),
            color: $("#inputBackgroundEvent").val()
        }, !0)
    }

//    toastr.options = {
//        closeButton: !0,
//        progressBar: !0,
//        showMethod: "fadeIn",
//        hideMethod: "fadeOut",
//        timeOut: 5e3
//    }, toastr.info("You have 6 notifications", "Welcome to EduRe"), $(".counter").counterUp({
//        delay: 10,
//        time: 1e3
//    });



    var u = $("#order-table").DataTable({
        lengthChange: !1,
        pageLength: 5,
        colReorder: !0,
        buttons: ["copy", "excel", "pdf", "print"],
        language: {
            search: "",
            searchPlaceholder: "Search records"
        }
    });
    u.buttons().container().appendTo("#order-table_wrapper .col-sm-6:eq(0)"), $(".draggable li").each(function() {
        $(this).data("event", {
            title: $.trim($(this).text()),
            stick: !0
        }), $(this).draggable({
            zIndex: 999,
            revert: !0,
            revertDuration: 0
        })
    }), $("#fullcalendar").fullCalendar({
        header: {
            left: "prev,next",
            center: "title",
            right: "month,agendaWeek,agendaDay"
        },
        buttonIcons: {
            prev: " ti-angle-left",
            next: " ti-angle-right"
        },
        defaultDate: "2016-03-15",
        editable: !0,
        droppable: !0,
        selectable: !0,
        select: function(e, t, a) {
            $("#start").val(moment(e).format("YYYY/MM/DD hh:mm a")), $("#end").val(moment(t).format("YYYY/MM/DD hh:mm a")), $("#inputTitleEvent").val(""), $("#addNewEvent").modal("show")
        },
        eventColor: "#0667D6",
        eventLimit: !0,
        events: [{
            title: "All Day Event",
            start: "2016-03-18",
            color: "#8E23E0"
        }, {
            title: "Long Event",
            start: "2016-03-07",
            end: "2016-03-10",
            color: "#E5343D"
        }, {
            id: 999,
            title: "Repeating Event",
            start: "2016-03-28T16:00:00",
            color: "#FFB61E"
        }, {
            id: 999,
            title: "Repeating Event",
            start: "2016-03-16T16:00:00",
            color: "#FFB61E"
        }, {
            title: "Conference",
            start: "2016-03-11",
            end: "2016-03-13",
            color: "#17A88B"
        }, {
            title: "Meeting",
            start: "2016-03-12T10:30:00",
            end: "2016-03-12T12:30:00",
            color: "#0667D6"
        }, {
            title: "Lunch",
            start: "2016-03-12T12:00:00",
            color: "#1F364F"
        }, {
            title: "Meeting",
            start: "2016-03-12T14:30:00",
            color: "#E5343D"
        }, {
            title: "Happy Hour",
            start: "2016-03-12T17:30:00",
            color: "#888888"
        }, {
            title: "Dinner",
            start: "2016-03-12T20:00:00",
            color: "#0667D6"
        }, {
            title: "Birthday Party",
            start: "2016-03-13T07:00:00",
            color: "#8E23E0"
        }, {
            title: "Click for Google",
            url: "http://google.com/",
            start: "2016-03-28",
            color: "#0667D6"
        }],
        drop: function() {
            $("#drop-remove").is(":checked") && $(this).remove()
        }
    }), $("#btnAddNewEvent").on("click", function(t) {
        t.preventDefault(), e()
    }), $("#inputBackgroundEvent").minicolors({
        theme: "bootstrap"
    });

});