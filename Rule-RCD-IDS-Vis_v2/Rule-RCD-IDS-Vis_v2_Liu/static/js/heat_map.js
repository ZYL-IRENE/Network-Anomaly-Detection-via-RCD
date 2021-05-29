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


function HeatMap() {
    var myChart = echarts.init(document.getElementById('heat_map'));

    var features = ["duration", "service", "flag", "src_bytes", "dst_bytes", "count", "serror_rate", "srv_rerror_rate", "same_srv_rate", "dst_host_count", "dst_host_srv_count", "dst_host_same_src_port_rate", "dst_host_serror_rate", "dst_host_srv_serror_rate"];
    var days = ['Saturday', 'Friday', 'Thursday',
        'Wednesday', 'Tuesday', 'Monday', 'Sunday'];

    var data = [[0,7,1],[0,10,5],[0,1,2],[0,0,1],[0,13,0],[0,5,1],[0,12,1],[0,11,2],[0,9,1],[1,7,1],[1,11,1],[1,2,5],[1,0,1],[1,3,2],[1,13,1],[1,5,1],[1,12,1],[1,9,5],[2,10,5],[2,1,2],[2,0,1],[2,13,1],[2,5,1],[2,6,1],[2,3,2],[2,8,5],[2,9,5],[3,10,5],[3,11,1],[3,0,1],[3,13,1],[3,6,1],[3,3,1],[3,12,1],[3,8,5],[3,9,5],[4,4,3],[4,11,1],[4,2,5],[4,0,1],[4,13,1],[4,6,1],[4,12,1],[4,8,5],[4,9,5],[5,7,1],[5,4,2],[5,2,5],[5,13,1],[5,10,4],[5,6,1],[5,3,1],[5,12,1],[5,9,5],[6,7,1],[6,11,1],[6,0,1],[6,13,1],[6,4,2],[6,5,1],[6,6,1],[6,12,1],[6,9,5]];

    data = data.map(function (item) {
        return [item[1], item[0], item[2] || '-'];
    });

    var option = {
        tooltip: {
            position: 'top'
        },
        grid: {
            height: '80%',
            width: '85%',
            top: '0%'
        },
        gradientColor:['#b3e5fc','#01579b'],
        xAxis: {
            type: 'category',
            data: features,
            splitArea: {
                show: true
            },
            axisLabel:{ rotate:40,},
            show: true
        },
        yAxis: {
            type: 'category',
            data: days,
            splitArea: {
                show: true
            },
            show: false
        },
        visualMap: {
            min: 0,
            max: 10,
            calculable: true,
            orient: 'horizontal',
            left: 'center',
            bottom: '15%',
            show: false
        },
        series: [{
            name: 'Punch Card',
            type: 'heatmap',
            data: data,
            label: {
                show: true
            },
            emphasis: {
                itemStyle: {
                    shadowBlur: 10,
                    shadowColor: 'rgba(0, 0, 0, 0.5)'
                }
            }
        }]
    };

    myChart.setOption(option);

}

addLoadEvent(HeatMap);