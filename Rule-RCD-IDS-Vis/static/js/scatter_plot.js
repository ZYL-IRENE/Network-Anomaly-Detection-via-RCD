function addLoadEvent(func) {
    var oldonload = window.onload;
    if (typeof window.onload != 'function') {
        window.onload = func;
    } 
    else {
        window.onload = function () {
            oldonload();
            func();
        }
    }
}

function ScatterPlot() {
    var myChart = echarts.init(document.getElementById('scatter_plot'));
    var myChart2 = echarts.init(document.getElementById('radar_plot'));

    var series = [];
    var color=["#91cc75","#fac858","#ee6666","#73c0de","#3ba272","#fc8452","#9a60b4","#ea7ccc"];
    var totaldata = [];
    var rawdata = [];
    var exist_new_label = true;
    option = {
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
    };

    $.get('/scatterPlot').done(function (data) {
        console.log("scatter data");
        console.log(data.length);
        console.log(data);

        var labeled = new Array(data.length);
        for (var i=0;i<data.length;i++) {
            labeled[i] = 0;
            var tmpdata = [];
            tmpdata.push(data[i].x);
            tmpdata.push(data[i].y);
            totaldata.push(tmpdata);
        }

        var currentlabel = data[0].label;
        while (exist_new_label) {
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
            console.log(labeled);
            rawdata.push(tmpseriesdata);
            console.log(rawdata);

            exist_new_label = false;
            for(var i=0;i<data.length;i++){
                if (labeled[i] == 0) {
                    currentlabel = data[i].label;
                    exist_new_label = true;
                    break;
                }
            }
        }

        for (var i=0;i<rawdata.length;i++) {
            series.push({
                color: color[i],
                itemStyle: {
                    opacity: 0.5,
                    borderColor: "gray"
                },
                type: 'scatter',
                symbolSize: 7,
                data: rawdata[i]
            });
        }
        myChart.setOption({
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

    myChart.setOption(option);

    myChart2.setOption({
        radar: {
            // shape: 'circle',
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

    myChart.on('click', function (params) {
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
        myChart.setOption({
            series: series
        });

        $.get('/radarPlot').done(function (data) {
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
            console.log(data_plot);

            console.log(Math.max.apply(Math, data.map(function(o) {return o.duration})));
            myChart2.setOption({
                tooltip: {
                    trigger: 'item'
                },
                radar: {
                    // shape: 'circle',

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
            myChart.setOption({
                series: series
            });
            series.pop();
            series.pop();
            
        });

    });
}

addLoadEvent(ScatterPlot);