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
            data: ['6-08', '6-09', '6-10', '6-11', '6-12', '6-13', '6-14']
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
                data: [0, 0, 0, 0, 0, 0, 0]
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

                data: ['10-1', '10-2', '10-3', '10-4', '10-5', '10-6', '10-7', '10-8', '10-9', '10-10', '10-11', '10-12'],
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
                data: [2.0, 2.2, 3.3, 4.5, 6.3, 10.2, 20.3, 23.4, 23.0, 16.5, 12.0, 6.2]
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
            data: ['', '', '', '', '']
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
                data: [18203, 23489, 29034, 104970, 131744]
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
                    {value: 90, name: '成功'},
                    {value: 10, name: '失败'}

                ],
                itemStyle: {
                    emphasis: {
                        shadowBlur: 10,
                        shadowOffsetX: 0,
                        shadowColor: 'rgba(0, 0, 0, 0.5)'
                    }
                }
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
                $("#drill_monitor").append('<tr>\n' +
                    '    <td> ' + data.drill_monitor[i].process_name + '</td>\n' +
                    '    <td><span class="label label-sm label-success"> 成功 </span></td>\n' +
                    '    <td> 8:00</td>\n' +
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
                $("#drill_log").append('<li '+ drill_log_class +'>\n' +
                    '    <p class="fl"><b>' + data.task_list[i].process_name + '</b><br>\n' +
                    '        ' + data.task_list[i].content + '<br>\n' +
                    '    </p>\n' +
                    '    <p class="fr pt17">' + data.task_list[i].start_time + '</p>\n' +
                    '</li>');
            }
        },
        // error: function (e) {
        //     alert("加载失败，请于管理员联系。");
        // }
    });

});

