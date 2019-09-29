$(document).ready(function () {
    $('#process_schedule_dt').dataTable({
        "bAutoWidth": true,
        "bSort": false,
        "bProcessing": true,
        "ajax": "../process_schedule_data/",
        "columns": [
            {"data": "process_schedule_id"},
            {"data": "process_schedule_name"},
            {"data": "process_name"},
            {"data": null},
            {"data": "remark"},
            {"data": null},
            {"data": null}
        ],
        "columnDefs": [{
            "data": null,
            "targets": -4,
            "render": function (data, type, full) {
                // 定时任务
                var per_week = full.per_week && full.per_week != "*" ? '/ 周per_week/ '.replace("per_week", full.per_week) : "";
                var per_month = full.per_month && full.per_month != "*" ? 'per_month月'.replace("per_month", full.per_month) : "";
                return "<td>" + full.hours + ":" + full.minutes + per_week + per_month + "</td>"
            },
        }, {
            "data": null,
            "targets": -2,
            "render": function (data, type, full) {
                // 定时任务状态
                var status = "";
                if (full.status == false) {
                    status = "关闭"
                }
                if (full.status == true) {
                    status = "开启"
                }
                return "<td>" + status + "</td>";
            },
        }, {
            "targets": -1,
            "data": null,
            "width": "100px",
            "render": function (data, type, full) {
                var statusButton = "";
                if (full.status == true) {
                    statusButton = "<button title='关闭'  id='reload' class='btn btn-xs btn-danger' type='button'><i class='fa fa-power-off'></i></button>";
                } else {
                    statusButton = "<button title='启动'  id='reload' class='btn btn-xs btn-primary' type='button'><i class='fa fa-power-off'></i></button>";
                }
                return statusButton + "<button  id='edit' title='编辑' data-toggle='modal'  data-target='#static'  class='btn btn-xs btn-primary' type='button'><i class='fa fa-edit'></i></button><button title='删除'  id='delrow' class='btn btn-xs btn-primary' type='button'><i class='fa fa-trash-o'></i></button>";
            },
        }],
        "oLanguage": {
            "sLengthMenu": "每页显示 _MENU_ 条记录",
            "sZeroRecords": "抱歉， 没有找到",
            "sInfo": "从 _START_ 到 _END_ /共 _TOTAL_ 条数据",
            "sInfoEmpty": "没有数据",
            "sInfoFiltered": "(从 _MAX_ 条数据中检索)",
            "sSearch": "搜索",
            "oPaginate": {
                "sFirst": "首页",
                "sPrevious": "前一页",
                "sNext": "后一页",
                "sLast": "尾页"
            },
            "sZeroRecords": "没有检索到数据",
        }
    });
    // 行按钮
    $('#process_schedule_dt tbody').on('click', 'button#reload', function () {
        var table = $('#process_schedule_dt').DataTable();
        var data = table.row($(this).parents('tr')).data();
        var confirmInfo = "";
        var status = 0;

        if (data.status == true){
            confirmInfo = "确定要关闭该流程计划？";
            status = 0;
        } else {
            confirmInfo = "确定要启动该流程计划？";
            status = 1;
        }

        if (confirm(confirmInfo)) {
            $.ajax({
                type: "POST",
                url: "../change_periodictask/",
                data: {
                    process_schedule_id: data.process_schedule_id,
                    process_periodictask_status: status
                },
                success: function (data) {
                    if (data.ret == 1) {
                        table.ajax.reload();
                    }
                    alert(data.info);
                },
                error: function (e) {
                    alert("定时任务状态修改失败，请于管理员联系。");
                }
            });
        }
    });
    $('#process_schedule_dt tbody').on('click', 'button#delrow', function () {
        if (confirm("确定要删除该条数据？")) {
            var table = $('#process_schedule_dt').DataTable();
            var data = table.row($(this).parents('tr')).data();
            $.ajax({
                type: "POST",
                url: "../hosts_manage_del/",
                data: {
                    host_id: data.host_id,
                },
                success: function (data) {
                    if (data.ret == 1) {
                        table.ajax.reload();
                    }
                    alert(data.info);
                },
                error: function (e) {
                    alert("删除失败，请于管理员联系。");
                }
            });

        }
    });
    $('#process_schedule_dt tbody').on('click', 'button#edit', function () {
        var table = $('#process_schedule_dt').DataTable();
        var data = table.row($(this).parents('tr')).data();

        $("#process_schedule_id").val(data.process_schedule_id);
        $("#process").val(data.process_id);
        $("#process_schedule_name").val(data.process_schedule_name);

        var per_time = data.hours + ":" + data.minutes;
        $("#per_time").val(per_time).timepicker("setTime", per_time);
        $("#per_week").val(data.per_week != "*" ? data.per_week : 0).trigger("change");
        $("#per_month").val(data.per_month != "*" ? data.per_month : 0).trigger("change");
        $("#process_schedule_remark").val(data.remark);
    });

    // time-picker
    $("#per_time").timepicker({
        showMeridian: false,
        minuteStep: 5,
    }).on('show.timepicker', function () {
        $('#static').removeAttr('tabindex');
    }).on('hide.timepicker', function () {
        $('#static').attr('tabindex', -1);
    });

    $("#new").click(function () {
        $("#process_schedule_id").val("0");
        $("#process").val("");
        $("#process_schedule_name").val("");
        $("#per_time").val("00:00").timepicker("setTime", "00:00");
        $("#per_week").val("").trigger("change");
        $("#per_month").val("").trigger("change");
        $("#process_schedule_remark").val("");
    });

    $('#save').click(function () {
        var table = $('#process_schedule_dt').DataTable();

        $.ajax({
            type: "POST",
            dataType: 'json',
            url: "../process_schedule_save/",
            data: {
                process_schedule_name: $("#process_schedule_name").val(),
                process_schedule_id: $("#process_schedule_id").val(),
                process: $("#process").val(),
                per_time: $("#per_time").val(),
                per_week: $("#per_week").val(),
                per_month: $("#per_month").val(),
                process_schedule_remark: $("#process_schedule_remark").val(),
            },
            success: function (data) {
                if (data.ret == 1) {
                    $('#static').modal('hide');
                    table.ajax.reload();
                }
                alert(data.info);
            },
            error: function (e) {
                alert("页面出现错误，请于管理员联系。");
            }
        });
    });

    $('#error').click(function () {
        $(this).hide()
    });
});