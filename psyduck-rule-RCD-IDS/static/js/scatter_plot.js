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

    var color=["red","yellow","green","blue","black","purple"];
    var totaldata = [];
    var rawdata = [];
    var exist_new_label = true;
    option = {
        xAxis: {},
        yAxis: {},
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

        myChart.setOption({
            series: [{
                color: color[0],
                type: 'scatter',
                symbolSize: 5,
                data: rawdata[0]
            },{
                color: color[1],
                type: 'scatter',
                symbolSize: 5,
                data: rawdata[1]
            }
            ]
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
                },
                series: [{
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
    });
}

addLoadEvent(ScatterPlot);