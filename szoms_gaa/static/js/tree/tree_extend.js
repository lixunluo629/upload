odoo.define('tree_extend', function (require) {
    "use strict";
    var ajax = require('web.ajax');
    var ListController = require('web.ListController');
    var ListRenderer = require('web.ListRenderer');

    //
    var controller;
    var renderer;
    var [zero,one,two,tree,four,five] = [0,0,0,0,0,0]

    var chart1 = function () {

        var ctx =renderer.state.getContext();
        ajax.jsonRpc('/web/dataset/call_kw', 'call', {
            model: 'zabbix.trigger',
            method: 'search_read',
            args: [],
            kwargs: {
                domain: [],
                order: 'id asc',  /* 正序倒序 */
                fields:['priority'],/* 需要的数据筛选 */
                context: ctx
            }
            }).then(function (respdata) {
                if (respdata.length > 0) {
                        respdata.forEach(function (item) {
                            if(item.priority == 1)
                                one++
                            else if(item.priority == 2)
                                two++
                            else if(item.priority == 3)
                                tree++
                            else if(item.priority == 4)
                                four++
                            else if(item.priority == 5)
                                five++
                            else
                                zero++
                            }
                        )
                    }
                    trigger_charts()
                    trigger_charts1()
                    one =two =tree =four =five =zero =0

            });

    };
    ListController.include({
        renderPager: function () {
            controller=this;
            return this._super.apply(this, arguments);
        }
    });

 //
    ListRenderer.include({
        _renderView: function () {
            renderer=this;
            var result = this._super.apply(this, arguments);
            if (this.state.model == 'zabbix.event_charts') {
            renderer.$el.css('display','none')
            renderer.$el.after(`<div class="king-container clearfix chart_margin" style="margin: 20px auto;padding-left:20px">
                                    <div class="container-fluid mb0 ">
                                        <div class="row row2">
                                            <div id="main"  class="col-md-6" style="width: 16rem;height: 40rem;margin-top: 20px;background: #fff;box-shadow: rgba(0, 0, 0, 0.2) -1px 3px 3px"></div>
                                            <div id="main1" class="col-md-6" style="width: 800px;height: 500px;padding-top: 20px;box-shadow: black"></div>
                                        </div>

                                    </div>
                                </div>`)
            chart1()
                }
            return result;
        }
    });


    var trigger_charts = function () {
        var myChart = echarts.init(document.getElementById('main'),'macarons');
               var  option = {
                            title : {
                                text: '告警统计',
                                subtext: '优先级',
                                x:'center'
                            },
                            tooltip: {
                                trigger: 'item',
                                formatter: "{a} <br/>{b}: {c} (占比:{d}%)"
                            },
                            legend: {
                                orient: 'vertical',
                                y:'20',
                                x: 'right',
                                data:['未分类','信息','告警','平均','高','灾难']
                            },
                            series: [
                                {
                                    name:'优先级来源',
                                    type:'pie',
                                    avoidLabelOverlap: true,
                                    center: ['50%', '50%'],
                                    label: {
                                        normal: {
                                            show: true,
                                        },
                                        emphasis: {
                                            show: true,
                                            textStyle: {
                                                fontSize: '30',
                                                fontWeight: 'bold'
                                            }
                                        }
                                    },
                                    labelLine: {
                                        normal: {
                                            show: true,
                                        }
                                    },
                                    data:[
                                        {value:zero, name:'未分类'},
                                        {value:one, name:'信息'},
                                        {value:two, name:'告警'},
                                        {value:tree, name:'平均'},
                                        {value:four, name:'高'},
                                        {value:five, name:'灾难'},
                                    ],

                                }
                            ]

                    };
                    myChart.setOption(option);
                    window.onresize = function () {
                       myChart.resize();
                    };　
                }
    var trigger_charts1 = function () {
                Table().init({
            id:'main1',
            align:'left',
            title:'告警数量统计',
            header:['id','优先级','数量'],
            headerBgColor:'#fff',
            evenBgColor:'#f4f4f4',
            oddBgColor:'#fff',
            data:[
                [1,'未分类',zero],
                [2,'信息',one],
                [3,'告警',two],
                [4,'平均',tree],
                [4,'高',four],
                [5,'灾难',five]
            ]
        });


    }
});
