$(document).ready(function () {
    /*
        初始化
     */
    var csrfToken = $("[name='csrfmiddlewaretoken']").val();

    // 最近七日演练
    var weekDrillChart = echarts.init(document.getElementById('arightboxbott'));
    var weekDrillOption = {
        color: ['#7de494', '#7fd7b1', '#5578cf', '#5ebbeb', '#d16ad8', '#f8e19a', '#00b7ee', '#81dabe', '#5fc5ce'],
        backgroundColor: 'rgba(1,202,217,.2)',

        grid: {
            left: '5%',
            right: '8%',
            bottom: '7%',
            top: '8%',
            containLabel: true
        },
        toolbox: {
            feature: {
                saveAsImage: {}
            }
        },
        xAxis: {
            type: 'category',
            boundaryGap: false,
            axisLine: {
                lineStyle: {
                    color: 'rgba(255,255,255,.2)'
                }
            },
            splitLine: {
                lineStyle: {
                    color: 'rgba(255,255,255,.1)'
                }
            },
            axisLabel: {
                color: "rgba(255,255,255,.7)"
            },
            data: []
        },
        yAxis: {
            type: 'value',
            axisLine: {
                lineStyle: {
                    color: 'rgba(255,255,255,.2)'
                }
            },
            splitLine: {
                lineStyle: {
                    color: 'rgba(255,255,255,.1)'
                }
            },
            axisLabel: {
                color: "rgba(255,255,255,.7)"
            },
        },
        series: [
            {
                name: '最近7日演练次数',
                type: 'line',
                stack: '次数',
                areaStyle: {normal: {}},
                data: [],
                label: {
                    normal: {
                        show: true,
                        position: 'top',
                        textStyle: {
                            color: 'white'
                        }
                    }
                },
            }
        ]
    };
    weekDrillChart.setOption(weekDrillOption);

    // 平均RTO趋势
    var avgRTOChart = echarts.init(document.getElementById('amiddboxtbott2'));
    var avgRTOOption = {
        backgroundColor: 'rgba(1,202,217,.2)',
        grid: {
            left: 60,
            right: 60,
            top: 50,
            bottom: 40
        },
        toolbox: {
            feature: {
                dataView: {show: true, readOnly: false},
                magicType: {show: true, type: ['line', 'bar']},
                restore: {show: true},
                saveAsImage: {show: true}
            }
        },
        legend: {
            top: 10,
            textStyle: {
                fontSize: 10,
                color: 'rgba(255,255,255,.7)'
            },
            data: ['平均RTO']
        },
        xAxis: [
            {
                type: 'category',
                axisLine: {
                    lineStyle: {
                        color: 'rgba(255,255,255,.2)'
                    }
                },
                splitLine: {
                    lineStyle: {
                        color: 'rgba(255,255,255,.1)'
                    }
                },
                axisLabel: {
                    color: "rgba(255,255,255,.7)"
                },

                data: [],
                axisPointer: {
                    type: 'shadow'
                }
            }
        ],
        yAxis: [
            {
                type: 'value',
                name: '',
                min: 0,
                max: 30,
                interval: 5,
                axisLine: {
                    lineStyle: {
                        color: 'rgba(255,255,255,.3)'
                    }
                },
                splitLine: {
                    lineStyle: {
                        color: 'rgba(255,255,255,.1)'
                    }
                },

                axisLabel: {
                    formatter: '{value} min'
                }
            },

        ],
        series: [
            {
                name: '平均RTO',
                type: 'line',
                itemStyle: {
                    normal: {
                        color: new echarts.graphic.LinearGradient(
                            0, 0, 0, 1,
                            [
                                {offset: 0, color: '#fffb34'},
                                {offset: 1, color: '#fffb34'}
                            ]
                        )
                    }
                },
                yAxisIndex: 0,
                data: [],
                label: {
                    normal: {
                        show: true,
                        position: 'top',
                        textStyle: {
                            color: 'white'
                        }
                    }
                },
            }
        ]
    };
    avgRTOChart.setOption(avgRTOOption);

    // 系统演练次数TOP5
    var drillTopTimeChart = echarts.init(document.getElementById('pleftbox2bott_cont'));
    var drillTopTimeOption = {
        color: ['#7ecef4'],
        backgroundColor: 'rgba(1,202,217,.2)',
        grid: {
            left: 40,
            right: 20,
            top: 30,
            bottom: 0,
            containLabel: true
        },

        xAxis: {
            type: 'value',
            axisLine: {
                lineStyle: {
                    color: 'rgba(255,255,255,0)'
                }
            },
            splitLine: {
                lineStyle: {
                    color: 'rgba(255,255,255,0)'
                }
            },
            axisLabel: {
                color: "rgba(255,255,255,0)"
            },
            boundaryGap: [0, 0.01]
        },
        yAxis: {
            type: 'category',
            axisLine: {
                lineStyle: {
                    color: 'rgba(255,255,255,.5)'
                }
            },
            splitLine: {
                lineStyle: {
                    color: 'rgba(255,255,255,.1)'
                }
            },
            axisLabel: {
                color: "rgba(255,255,255,.5)"
            },
            data: []
        },
        series: [
            {
                name: '系统演练次数TOP5',
                type: 'bar',
                barWidth: 20,
                itemStyle: {
                    normal: {
                        color: new echarts.graphic.LinearGradient(
                            1, 0, 0, 1,
                            [
                                {offset: 0, color: 'rgba(230,253,139,.7)'},
                                {offset: 1, color: 'rgba(41,220,205,.7)'}
                            ]
                        )
                    }
                },
                data: [],
                label: {
                    normal: {
                        show: true,
                        position: 'right',
                        textStyle: {
                            color: 'white'
                        }
                    }
                },
            }
        ]
    };
    drillTopTimeChart.setOption(drillTopTimeOption);

    // 演练成功率
    var drillRateChart = echarts.init(document.getElementById('lpeftbot'));
    var drillRateOption = {
        color: ['#00b7ee', '#d2d17c', '#5578cf', '#5ebbeb', '#d16ad8', '#f8e19a', '#00b7ee', '#81dabe', '#5fc5ce'],
        backgroundColor: 'rgba(1,202,217,.2)',
        grid: {
            left: 20,
            right: 20,
            top: 0,
            bottom: 20
        },
        legend: {
            top: 10,
            textStyle: {
                fontSize: 10,
                color: 'rgba(255,255,255,.7)'
            },
            data: ['成功', '失败']
        },
        series: [
            {
                name: '演练成功率',
                type: 'pie',
                radius: '55%',
                center: ['50%', '55%'],
                data: [
                    {value: 50, name: '成功'},
                    {value: 50, name: '失败'}

                ],
                itemStyle: {
                    emphasis: {
                        shadowBlur: 10,
                        shadowOffsetX: 0,
                        shadowColor: 'rgba(0, 0, 0, 0.5)'
                    },
                    normal: {
                        label: {
                            show: true,
                            formatter: '{b}:{d}%'
                        },
                        labelLine: {show: true}
                    }
                },
            }
        ]
    };
    drillRateChart.setOption(drillRateOption);

    /*
    大屏动态加载数据
        最近7日演练次数:
            weekDrillChart.setOption({
                xAxis: {
                    data: data.week_drill.drill_day
                },
                series: [{
                    data: data.week_drill.drill_times
                }]
            });
            weekDrillChart.setOption({
                xAxis: {
                    data: data.avgRTO.drill_day
                },
                series: [{
                    data: data.avgRTO.drill_rto
                }]
            });
            drillTopTimeChart.setOption({
                xAxis: {
                    data: data.drill_top_time.drill_name
                },
                series: [{
                    data: data.drill_top_time.drill_time
                }]
            });
     */
    $.ajax({
        type: "POST",
        url: "../get_monitor_data/",
        data: {
            "csrfmiddlewaretoken": csrfToken
        },
        success: function (data) {
            // 最近七日演练
            weekDrillChart.setOption({
                xAxis: {
                    data: data.week_drill.drill_day
                },
                series: [{
                    data: data.week_drill.drill_times
                }]
            });
            // 平均RTO
            avgRTOChart.setOption({
                xAxis: {
                    data: data.avgRTO.drill_day
                },
                series: [{
                    data: data.avgRTO.drill_rto
                }]
            });
            // 系统演练次数TOP5
            drillTopTimeChart.setOption({
                yAxis: {
                    data: data.drill_top_time.drill_name
                },
                series: [{
                    data: data.drill_top_time.drill_time
                }]
            });
            // 演练成功率
            drillRateChart.setOption({
                series: [{
                    data: [
                        {value: data.drill_rate[0], name: '成功'},
                        {value: data.drill_rate[1], name: '失败'}

                    ],
                }]
            });

            // 演练监控
            $("#drill_monitor").empty();
            for (var i = 0; i < data.drill_monitor.length; i++) {
                var status_label = "",
                    status_name = "";
                if (data.drill_monitor[i].state == "DONE") {
                    status_label = "label-success";
                    status_name = "成功";
                } else if (data.drill_monitor[i].state == "STOP") {
                    status_label = "label-warning";
                    status_name = "终止";
                } else if (data.drill_monitor[i].state == "ERROR") {
                    status_label = "label-danger";
                    status_name = "错误";
                } else if (data.drill_monitor[i].state == "RUN") {
                    status_label = "label-info";
                    status_name = "运行中";
                } else if (data.drill_monitor[i].state == "REJECT") {
                    status_label = "label-warning";
                    status_name = "已取消";
                } else {
                    status_label = "label-primary";
                    status_name = "未演练";
                }

                $("#drill_monitor").append('<tr>\n' +
                    '    <td> ' + data.drill_monitor[i].process_name + '</td>\n' +
                    '    <td><span class="label label-sm ' + status_label + '"> ' + status_name + ' </span></td>\n' +
                    '    <td> ' + data.drill_monitor[i].schedule_time + '</td>\n' +
                    '    <td> ' + data.drill_monitor[i].start_time + '</td>\n' +
                    '    <td> ' + data.drill_monitor[i].end_time + '</td>\n' +
                    '    <td> ' + data.drill_monitor[i].percent + '</td>\n' +
                    '</tr>');
            }

            // 演练日志
            $("#drill_log").empty();
            for (var i = 0; i < data.task_list.length; i++) {
                var drill_log_class = "";
                if (i % 2 == 0) {
                    drill_log_class == ' class="bg"';
                }
                $("#drill_log").append('<li ' + drill_log_class + '>\n' +
                    '    <p class="fl"><b>' + data.task_list[i].process_name + '</b><br>\n' +
                    '        ' + data.task_list[i].content + '<br>\n' +
                    '    </p>\n' +
                    '    <p class="fr pt17">' + data.task_list[i].start_time + '</p>\n' +
                    '</li>');
            }

            // 今日作业
            $("#running_job").text(data.today_job.running_job);
            $("#success_job").text(data.today_job.success_job);
            $("#error_job").text(data.today_job.error_job);
            $("#not_running").text(data.today_job.not_running);

            // 客户端状态
            $("#service_status").text(data.clients_status.service_status);
            $("#net_status").text(data.clients_status.net_status);
            $("#all_clients").text(data.clients_status.all_clients);
            $("#error_clients").text(data.clients_status.error_clients);
        },
    });
    $.ajax({
        type: "POST",
        url: "../get_clients_status/",
        data: {
            "csrfmiddlewaretoken": csrfToken
        },
        success: function (data) {
            // 客户端状态
            $("#service_status").text(data.clients_status.service_status);
            $("#net_status").text(data.clients_status.net_status);
            $("#all_clients").text(data.clients_status.all_clients);
            $("#error_clients").text(data.clients_status.error_clients);

            // 报警客户端
            var warning_client_num = 0;
            var whole_list = data.data;

            for (var i = 0; i < whole_list.length; i++) {
                // 报警客户端
                for (var j = 0; j < agent_job_list.length; j++) {
                    if (agent_job_list[j].job_backup_status.indexOf("失败") != -1) {
                        warning_client_num += 1;
                        break
                    }
                }
            }

            $("#warning_client_num").text(warning_client_num);
            if (warning_client_num > 0) {
                $("#warning_client_num").css("color", "red");
            }
        },
    });
});


