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

function Rare_HeatMap() {
    var myChart = echarts.init(document.getElementById('rare_heat_map'));

    var features = ["duration", "service", "flag", "src_bytes", "dst_bytes", "count", "serror_rate", "srv_rerror_rate", "same_srv_rate", "dst_host_count", "dst_host_srv_count", "dst_host_same_src_port_rate", "dst_host_serror_rate", "dst_host_srv_serror_rate"];
    var days = ['Saturday'];

    var data = [[0,0,1],[0,1,1],[0,2,2],[0,3,1],[0,4,1],[0,5,5],[0,6,3],[0,7,5],[0,8,1],[0,9,5],[0,10,1],[0,11,1],[0,12,3],[0,13,1]];

    data = data.map(function (item) {
        return [item[1], item[0], item[2] || '-'];
    });

    var option = {
        tooltip: {
            position: 'top'
        },
        grid: {
            height: '100%',
            width: '85%',
            top: '2%'
        },
        xAxis: {
            type: 'category',
            data: features,
            splitArea: {
                show: false
            },
            axisLabel:{ rotate:40},
            show: false
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

addLoadEvent(Rare_HeatMap);