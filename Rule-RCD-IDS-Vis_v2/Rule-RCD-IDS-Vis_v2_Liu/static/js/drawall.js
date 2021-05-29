// 我尝试把大部分js文件放在一起

$(function (){
    var ScatterChart = echarts.init(document.getElementById('scatter_plot'));
    var RadarChart = echarts.init(document.getElementById('radar_plot'));
    var myTable = $('#view_table');
    var paraChart = echarts.init(document.getElementById('parallel_coord'));

    var series = [];
    var color=["#91cc75","#fac858","#ee6666","#73c0de","#3ba272","#fc8452","#9a60b4","#ea7ccc"];
    var totaldata = [];
    var scatterrawdata = [];
    var pararawdata = [];
    var exist_new_class = true;
    var center = [];

    $.get('/centerArray').done(function (data) {
        // 获得label
        center = data;
        for (var i=0;i<center.length;i++) {
            var text=window.prompt("Group "+i.toString()+"'s center data point is point "+(center[i]+1).toString()+
                                    "\nThis group's type is:\n(Please select one from normal,DOS,PROBE,U2R,R2L)","normal");
            if (text!=null && text!="") {
                $.post(
                    "/labelArray",
                    {label: text},
                    function (result) {
                        console.log("lala")
                    }
                );
            }  
        } 

        $.get('/tableQuery').done(function (data){
            console.log(data);
        });

        // 绘制表格
        $(function () {
            myTable.bootstrapTable({
                url: '/tableQuery', // 请求数据源的路由
                dataType: "json",
                data: [],
                pagination: false, //前端处理分页
                singleSelect: false,//是否只能单选
                search: false, //显示搜索框，此搜索是客户端搜索，不会进服务端，所以，个人感觉意义不大
                toolbar: '#toolbar', //工具按钮用哪个容器
                striped: true, //是否显示行间隔色
                cache: false, //是否使用缓存，默认为true，所以一般情况下需要设置一下这个属性（*）
                pageNumber: 1, //初始化加载第10页，默认第一页F
                pageSize: 10, //每页的记录行数（*）
                pageList: [10, 20, 50, 100], //可供选择的每页的行数（*）
                strictSearch: true,//设置为 true启用 全匹配搜索，false为模糊搜索
                showColumns: true, //显示内容列下拉框
                showRefresh: false, //显示刷新按钮
                minimumCountColumns: 2, //当列数小于此值时，将隐藏内容列下拉框
                clickToSelect: true, //设置true， 将在点击某行时，自动勾选rediobox 和 checkbox
                height: $("#view2").height(), //表格高度，如果没有设置height属性，表格自动根据记录条数决定表格高度#
                uniqueId: "id", //每一行的唯一标识，一般为主键列
                showToggle: true, //是否显示详细视图和列表视图的切换按钮
                cardView: false, //是否显示详细视图
                sidePagination: "server", //分页方式：client客户端分页，server服务端分页（*）
                showExport: true,
                exportDataType: "all",
                buttonsAlign: "left",  //按钮位置
                iconSize: "sm",
                loadingFontSize: "8px",
                smartDisplay:false,
        
                columns: [{
                    checkbox: true,
                    visible: true
                }, {
                    field: 'class',
                    title: 'class',
                    events: { 'change .ss': function (e, value, row, index) { } },
                    formatter: function (value, row, index) {
                        var strHtml = "";
        
                        if (value == "DOS") {
                            strHtml = "<select class='ss'><option value='normal' >normal</option><option value='DOS' selected='selected'>DOS</option><option value='PROBE'>PROBE</option><option value='U2R'>U2R</option><option value='R2L'>R2L</option></select>";
                        }
                        else if (value == "PROBE") {
                            strHtml = "<select class='ss'><option value='normal' >normal</option><option value='DOS'>DOS</option><option value='PROBE' selected='selected'>PROBE</option><option value='U2R'>U2R</option><option value='R2L'>R2L</option></select>";
                        }
                        else if (value == "U2R") {
                            strHtml = "<select class='ss'><option value='normal' >normal</option><option value='DOS'>DOS</option><option value='PROBE'>PROBE</option><option value='U2R' selected='selected'>U2R</option><option value='R2L'>R2L</option></select>";
                        }
                        else if (value == "R2L") {
                            strHtml = "<select class='ss'><option value='normal' >normal</option><option value='DOS'>DOS</option><option value='PROBE'>PROBE</option><option value='U2R'>U2R</option><option value='R2L' selected='selected'>R2L</option></select>";
                        }
                        else
                            strHtml = "<select class='ss'><option value='normal' selected='selected'>normal</option><option value='DOS'>DOS</option><option value='PROBE'>PROBE</option><option value='U2R'>U2R</option><option value='R2L'>R2L</option></select>";
                        return strHtml;
        
                    }
        
                }, {
                    field: 'id',
                    title: 'id',
                    align: 'center',
                    width: 200,
                }, {
                    field: 'duration',
                    title: 'duration',
                    align: 'center'
                }, {
                    field: 'service',
                    title: 'service',
                    align: 'center',
                }, {
                    field: 'flag',
                    title: 'flag',
                    align: 'center',
                }, {
                    field: 'src_bytes',
                    title: 'src_bytes',
                    align: 'center',
                }, {
                    field: 'dst_bytes',
                    title: 'dst_bytes',
                    align: 'center',
                    width : 100,
                }, {
                    field: 'count',
                    title: 'count',
                    align: 'center',
                }, {
                    field: 'serror_rate',
                    title: 'serror_rate',
                    align: 'center',
                }, {
                    field: 'srv_rerror_rate',
                    title: 'srv_rerror_rate',
                    align: 'center',
                }, {
                    field: 'same_srv_rate',
                    title: 'same_srv_rate',
                    align: 'center',
                }, {
                    field: 'dst_host_count',
                    title: 'dst_host_count',
                    align: 'center',
                }, {
                    field: 'dst_host_srv_count',
                    title: 'dst_host_srv_count',
                    align: 'center',
                }, {
                    field: 'dst_host_same_src_port_rate',
                    title: 'dst_host_same_src_port_rate',
                    align: 'center',
                }, {
                    field: 'dst_host_serror_rate',
                    title: 'dst_host_serror_rate',
                    align: 'center',
                }, {
                    field: 'dst_host_srv_serror_rate',
                    title: 'dst_host_srv_serror_rate',
                    align: 'center',
                }
                ],
            });
        });
        
        // 绘制平行坐标
        var paraoption = {
            parallelAxis: [
                {dim: 0, name: 'id'},
                {dim: 1, name: 'duration'},
                {
                    dim: 2,
                    name: 'service',
                    type: 'category',
                    data: ["http", 'ecr_i', 'smtp', 'domain_u', 'auth', 'finger', 'private', 'imap4', 'telnet', 'uucp','hostnames', 'gopher', 'ftp_data', 'pm_dump', 'eco_i', 'ftp', 'other']
                },
                {
                    dim: 3, 
                    name: 'flag',
                    type: 'category',
                    data: ['SF', 'REJ', 'S0', 'SH', 'S1', 'RSTO', 'RSTR', 'S2']
                },
                {dim: 4, name: 'src_bytes'},
                {dim: 5, name: 'dst_bytes'},
                {dim: 6, name: 'count'},
                {dim: 7, name: 'serror_rate'},
                {dim: 8, name: 'srv_rerror_rate'},
                {dim: 9, name: 'same_srv_rate'},
                {dim: 10, name: 'dst_host_count'},
                {dim: 11, name: 'dst_host_srv_count'},
                {dim: 12, name: 'dst_host_same_src_port_rate'},
                {dim: 13, name: 'dst_host_serror_rate'},
                {dim: 14, name: 'dst_host_srv_serror_rate'},
            ],
            parallel: {
                top: 50,
                bottom: 10,       
                left: 50,
                right: 100,
                parallelAxisDefault: {
                    type: 'value',
                    nameLocation: "end",
                    nameRotate: 30,
                    nameGap: 5,
                }
            }
        };
    
        $.get('/parallelQuery').done(function (data) {
            console.log("parallel data",data.length);
    
            for(var i=0;i<data.length;i++){
                var tmpdata = [];
                tmpdata.push(data[i].id);
                tmpdata.push(data[i].duration);
                tmpdata.push(data[i].service);
                tmpdata.push(data[i].flag);
                tmpdata.push(data[i].src_bytes);
                tmpdata.push(data[i].dst_bytes);
                tmpdata.push(data[i].count);
                tmpdata.push(data[i].serror_rate);
                tmpdata.push(data[i].srv_rerror_rate);
                tmpdata.push(data[i].same_srv_rate);
                tmpdata.push(data[i].dst_host_count);
                tmpdata.push(data[i].dst_host_srv_count);
                tmpdata.push(data[i].dst_host_same_src_port_rate);
                tmpdata.push(data[i].dst_host_serror_rate);
                tmpdata.push(data[i].dst_host_srv_serror_rate);
                pararawdata.push(tmpdata);
            }  
            
            paraChart.setOption({
                series: {
                    type: 'parallel',
                    lineStyle: {
                        width: 0.5
                    },
                    data: pararawdata
                }
            });
        });
    
        paraChart.setOption(paraoption);

        // 绘制散点图
        ScatterChart.setOption({
            xAxis: {
                show : true,
                axisLine:{
                    show:false
                },
                axisTick:{
                    show:false
                },
                axisLabel: {
                    show: false
                },
                splitLine: {
                    show: true
                }
            },
            yAxis: {
                show : true,
                axisLine:{
                    show:false
                },
                axisTick:{
                    show:false
                },
                axisLabel: {
                    show: false
                },
                splitLine: {
                    show: true
                }
            }
        });

        $.get('/scatterTSNEPlot').done(function (data) {
            console.log(data);
            console.log("scatter data",data.length);

            var labeled = new Array(data.length);
            for (var i=0;i<data.length;i++) {
                var tmpdata = [];
                labeled[i] = 0;
                tmpdata.push(data[i].x);
                tmpdata.push(data[i].y);
                totaldata.push(tmpdata);
            }

            var currentlabel = data[0].label;
            while (exist_new_class) {
                var tmpdata = [];
                var tmpseriesdata = [];
                for(var i=0;i<data.length;i++){
                    if (labeled[i] == 0 && data[i].label == currentlabel) {
                        tmpdata = [];
                        tmpdata.push(data[i].x);
                        tmpdata.push(data[i].y);
                        tmpseriesdata.push(tmpdata);
                        labeled[i] = 1;
                    }
                }
                scatterrawdata.push(tmpseriesdata);

                exist_new_class = false;
                for(var i=0;i<data.length;i++){
                    if (labeled[i] == 0) {
                        currentlabel = data[i].label;
                        exist_new_class = true;
                        break;
                    }
                }
            }

            for (var i=0;i<scatterrawdata.length;i++) {
                series.push({
                    color: color[i],
                    itemStyle: {
                        opacity: 0.5,
                        borderColor: "gray"
                    },
                    type: 'scatter',
                    symbolSize: 7,
                    data: scatterrawdata[i]
                });
            }
            ScatterChart.setOption({
                series: series,
                tooltip: {
                    trigger: 'axis',
                    formatter: function (params) {
                        var str="";
                        var index = totaldata.findIndex(value=>(value[0] == params[0].data[0] && value[1] == params[0].data[1]));
                        str += "Index:" + index + '<br>';
                        return str;
                    }
                }
            });
        });

        RadarChart.setOption({
            radar: {
                indicator: [
                    { name: 'dst_bytes'},
                    { name: 'dst_host_count'},
                    { name: 'dst_host_same_src_port_rate'},
                    { name: 'dst_host_serror_rate'},
                    { name: 'dst_host_srv_count'},
                    { name: 'dst_host_srv_serror_rate'},
                    { name: 'duration'},
                    { name: 'flag'},
                    { name: 'id'},
                    { name: 'same_srv_rate'},
                    { name: 'serror_rate'},
                    { name: 'service'},
                    { name: 'src_bytes'},
                    { name: 'srv_rerror_rate'}
                ]
            }
        });

        ScatterChart.on('click', function (params) {
            var index_plot = totaldata.findIndex(value=>(value[0] == params.data[0] && value[1] == params.data[1]));
            var name = "Index" + index_plot;

            var highlight_data = [];
            var tmpdata = [];
            tmpdata.push(params.data[0]);
            tmpdata.push(params.data[1]);
            highlight_data.push(tmpdata);
            series.push({
                color: "#F9713C",
                type: 'scatter',
                symbolSize: 10,
                data: highlight_data
            });
            ScatterChart.setOption({
                series: series
            });

            $.get('/radarPlot').done(function (data) {
                console.log("radar data",data.length);

                var data_plot = [];
                data_plot.push(data[index_plot].dst_bytes);
                data_plot.push(data[index_plot].dst_host_count);
                data_plot.push(data[index_plot].dst_host_same_src_port_rate);
                data_plot.push(data[index_plot].dst_host_serror_rate);
                data_plot.push(data[index_plot].dst_host_srv_count);
                data_plot.push(data[index_plot].dst_host_srv_serror_rate);
                data_plot.push(data[index_plot].duration);
                data_plot.push(data[index_plot].flag);
                data_plot.push(data[index_plot].id);
                data_plot.push(data[index_plot].same_srv_rate);
                data_plot.push(data[index_plot].serror_rate);
                data_plot.push(data[index_plot].service);
                data_plot.push(data[index_plot].src_bytes);
                data_plot.push(data[index_plot].srv_rerror_rate);

                RadarChart.setOption({
                    tooltip: {
                        trigger: 'item'
                    },
                    radar: {
                        indicator: [
                            {
                                name: 'dst_bytes',
                                max: Math.max.apply(Math, data.map(function(o) {return o.dst_bytes}))
                            },
                            {
                                name: 'dst_host_count',
                                max: Math.max.apply(Math, data.map(function(o) {return o.dst_host_count}))
                            },
                            {
                                name: 'dst_host_same_src_port_rate',
                                max: Math.max.apply(Math, data.map(function(o) {return o.dst_host_same_src_port_rate}))
                            },
                            {
                                name: 'dst_host_serror_rate',
                                max: Math.max.apply(Math, data.map(function(o) {return o.dst_host_serror_rate}))
                            },
                            {
                                name: 'dst_host_srv_count',
                                max: Math.max.apply(Math, data.map(function(o) {return o.dst_host_srv_count}))
                            },
                            {
                                name: 'dst_host_srv_serror_rate',
                                max: Math.max.apply(Math, data.map(function(o) {return o.dst_host_srv_serror_rate}))
                            },
                            {
                                name: 'duration',
                                max: Math.max.apply(Math, data.map(function(o) {return o.duration}))
                            },
                            {
                                name: 'flag',
                                max: Math.max.apply(Math, data.map(function(o) {return o.flag}))
                            },
                            {
                                name: 'id',
                                max: Math.max.apply(Math, data.map(function(o) {return o.id}))
                            },
                            {
                                name: 'same_srv_rate',
                                max: Math.max.apply(Math, data.map(function(o) {return o.same_srv_rate}))
                            },
                            {
                                name: 'serror_rate',
                                max: Math.max.apply(Math, data.map(function(o) {return o.serror_rate}))
                            },
                            {
                                name: 'service',
                                max: Math.max.apply(Math, data.map(function(o) {return o.service}))
                            },
                            {
                                name: 'src_bytes',
                                max: Math.max.apply(Math, data.map(function(o) {return o.src_bytes}))
                            },
                            {
                                name: 'srv_rerror_rate',
                                max: Math.max.apply(Math, data.map(function(o) {return o.srv_rerror_rate}))
                            }
                        ],
                        shape: 'circle',
                        center: ['60%','50%'],
                    },
                    series: [{
                        name: name,
                        type: 'radar',
                        data:  [
                            {
                                value: data_plot
                            }
                        ],
                        itemStyle: {
                            color: '#F9713C'
                        },
                        areaStyle: {
                            opacity: 0.1
                        },
                        symbol: 'none',
                    }]
                });
            });

            $.get('/circlePlot').done(function (data) {
                var edge_index = data[index_plot].kneighbors;
                var center_x = totaldata[index_plot][0];
                var center_y = totaldata[index_plot][1];
                var edge_x   = totaldata[edge_index][0];
                var edge_y   = totaldata[edge_index][1];
                var radius   = Math.sqrt((edge_x-center_x)**2 + (edge_y-center_y)**2)

                circledata = [];
                for (var i=0;i<5000;i++) {
                    var tmpdata = [];
                    var ran = Math.random();
                    var x = center_x + radius * Math.cos(ran*2*Math.PI);
                    var y = center_y + radius * Math.sin(ran*2*Math.PI);
                    tmpdata.push(x);
                    tmpdata.push(y);
                    circledata.push(tmpdata);
                }

                series.push({
                    color: "#90a4ae",
                    type: 'scatter',
                    symbolSize: 1,
                    data: circledata
                });
                ScatterChart.setOption({
                    series: series
                });
                series.pop();
                series.pop();
            });
        });

        $("#dimension_method").change(function(){
            var type=$(this).children('input:checked').val();
            
            series = [];
            totaldata = [];
            scatterrawdata = [];
            exist_new_class = true;

            if (type == "MDS") {
                $.get('/scatterMDSPlot').done(function (data) {
                    console.log("mds scatter data",data.length);
                    ScatterChart.clear();

                    var labeled = new Array(data.length);
                    for (var i=0;i<data.length;i++) {
                        var tmpdata = [];
                        labeled[i] = 0;
                        tmpdata.push(data[i].x);
                        tmpdata.push(data[i].y);
                        totaldata.push(tmpdata);
                    }
            
                    var currentlabel = data[0].label;
                    while (exist_new_class) {
                        var tmpdata = [];
                        var tmpseriesdata = [];
                        for(var i=0;i<data.length;i++){
                            if (labeled[i] == 0 && data[i].label == currentlabel) {
                                tmpdata = [];
                                tmpdata.push(data[i].x);
                                tmpdata.push(data[i].y);
                                tmpseriesdata.push(tmpdata);
                                labeled[i] = 1;
                            }
                        }
                        scatterrawdata.push(tmpseriesdata);
            
                        exist_new_class = false;
                        for(var i=0;i<data.length;i++){
                            if (labeled[i] == 0) {
                                currentlabel = data[i].label;
                                exist_new_class = true;
                                break;
                            }
                        }
                    }

                    for (var i=0;i<scatterrawdata.length;i++) {
                        series.push({
                            color: color[i],
                            itemStyle: {
                                opacity: 0.5,
                                borderColor: "gray"
                            },
                            type: 'scatter',
                            symbolSize: 7,
                            data: scatterrawdata[i]
                        });
                    }

                    ScatterChart.setOption({
                        series: series,
                        tooltip: {
                            trigger: 'axis',
                            formatter: function (params) {
                                var str="";
                                var index = totaldata.findIndex(value=>(value[0] == params[0].data[0] && value[1] == params[0].data[1]));
                                str += "Index:" + index + '<br>';
                                return str;
                            }
                        },
                        xAxis: {
                            show : true,
                            axisLine:{
                                show:false
                            },
                            axisTick:{
                                show:false
                            },
                            axisLabel: {
                                show: false
                            },
                            splitLine: {
                                show: true
                            }
                        },
                        yAxis: {
                            show : true,
                            axisLine:{
                                show:false
                            },
                            axisTick:{
                                show:false
                            },
                            axisLabel: {
                                show: false
                            },
                            splitLine: {
                                show: true
                            }
                        }
                    });
                });
            }
            if (type == "LDA") {
                $.get('/scatterLDAPlot').done(function (data) {
                    console.log("lda scatter data",data.length);
                    ScatterChart.clear();

                    var labeled = new Array(data.length);
                    for (var i=0;i<data.length;i++) {
                        var tmpdata = [];
                        labeled[i] = 0;
                        tmpdata.push(data[i].x);
                        tmpdata.push(data[i].y);
                        totaldata.push(tmpdata);
                    }
            
                    var currentlabel = data[0].label;
                    while (exist_new_class) {
                        var tmpdata = [];
                        var tmpseriesdata = [];
                        for(var i=0;i<data.length;i++){
                            if (labeled[i] == 0 && data[i].label == currentlabel) {
                                tmpdata = [];
                                tmpdata.push(data[i].x);
                                tmpdata.push(data[i].y);
                                tmpseriesdata.push(tmpdata);
                                labeled[i] = 1;
                            }
                        }
                        scatterrawdata.push(tmpseriesdata);
            
                        exist_new_class = false;
                        for(var i=0;i<data.length;i++){
                            if (labeled[i] == 0) {
                                currentlabel = data[i].label;
                                exist_new_class = true;
                                break;
                            }
                        }
                    }

                    for (var i=0;i<scatterrawdata.length;i++) {
                        series.push({
                            color: color[i],
                            itemStyle: {
                                opacity: 0.5,
                                borderColor: "gray"
                            },
                            type: 'scatter',
                            symbolSize: 7,
                            data: scatterrawdata[i]
                        });
                    }

                    ScatterChart.setOption({
                        series: series,
                        tooltip: {
                            trigger: 'axis',
                            formatter: function (params) {
                                var str="";
                                var index = totaldata.findIndex(value=>(value[0] == params[0].data[0] && value[1] == params[0].data[1]));
                                str += "Index:" + index + '<br>';
                                return str;
                            }
                        },
                        xAxis: {
                            show : true,
                            axisLine:{
                                show:false
                            },
                            axisTick:{
                                show:false
                            },
                            axisLabel: {
                                show: false
                            },
                            splitLine: {
                                show: true
                            }
                        },
                        yAxis: {
                            show : true,
                            axisLine:{
                                show:false
                            },
                            axisTick:{
                                show:false
                            },
                            axisLabel: {
                                show: false
                            },
                            splitLine: {
                                show: true
                            }
                        }
                    });
                });
            }
            if (type == "T-SNE") {
                $.get('/scatterTSNEPlot').done(function (data) {
                    console.log("tsne scatter data",data.length);
                    ScatterChart.clear();

                    var labeled = new Array(data.length);
                    for (var i=0;i<data.length;i++) {
                        var tmpdata = [];
                        labeled[i] = 0;
                        tmpdata.push(data[i].x);
                        tmpdata.push(data[i].y);
                        totaldata.push(tmpdata);
                    }
            
                    var currentlabel = data[0].label;
                    while (exist_new_class) {
                        var tmpdata = [];
                        var tmpseriesdata = [];
                        for(var i=0;i<data.length;i++){
                            if (labeled[i] == 0 && data[i].label == currentlabel) {
                                tmpdata = [];
                                tmpdata.push(data[i].x);
                                tmpdata.push(data[i].y);
                                tmpseriesdata.push(tmpdata);
                                labeled[i] = 1;
                            }
                        }
                        scatterrawdata.push(tmpseriesdata);
            
                        exist_new_class = false;
                        for(var i=0;i<data.length;i++){
                            if (labeled[i] == 0) {
                                currentlabel = data[i].label;
                                exist_new_class = true;
                                break;
                            }
                        }
                    }

                    for (var i=0;i<scatterrawdata.length;i++) {
                        series.push({
                            color: color[i],
                            itemStyle: {
                                opacity: 0.5,
                                borderColor: "gray"
                            },
                            type: 'scatter',
                            symbolSize: 7,
                            data: scatterrawdata[i]
                        });
                    }

                    ScatterChart.setOption({
                        series: series,
                        tooltip: {
                            trigger: 'axis',
                            formatter: function (params) {
                                var str="";
                                var index = totaldata.findIndex(value=>(value[0] == params[0].data[0] && value[1] == params[0].data[1]));
                                str += "Index:" + index + '<br>';
                                return str;
                            }
                        },
                        xAxis: {
                            show : true,
                            axisLine:{
                                show:false
                            },
                            axisTick:{
                                show:false
                            },
                            axisLabel: {
                                show: false
                            },
                            splitLine: {
                                show: true
                            }
                        },
                        yAxis: {
                            show : true,
                            axisLine:{
                                show:false
                            },
                            axisTick:{
                                show:false
                            },
                            axisLabel: {
                                show: false
                            },
                            splitLine: {
                                show: true
                            }
                        }
                    });
                });      
            }
        });   

    });

});