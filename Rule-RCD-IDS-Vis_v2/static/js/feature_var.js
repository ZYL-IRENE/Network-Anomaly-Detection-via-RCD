$(function (){
    var chartDom = document.getElementById('feature_variance');
    var myChart = echarts.init(chartDom);
    var option;

    option = {
        yAxis: {
            type: 'category',
            data: ["duration", "service", "flag", "src_bytes", "dst_bytes", "count", "serror_rate", "srv_rerror_rate", "same_srv_rate", "dst_host_count", "dst_host_srv_count", "dst_host_same_src_port_rate", "dst_host_serror_rate", "dst_host_srv_serror_rate"],
            show: false
        },
        xAxis: {
            type: 'value',
        },
        tooltip:{
            position:'top',
        },
        grid: {
            height: '98%',
            width: '95%',
            top: '1%',
            left:'5%'
        }
        // series: [{
        //     data: [120, 200, 150, 80, 70, 110, 130,90,90,90,90,90,90,90],
        //     type: 'bar',
        //     showBackground: true,
        //     backgroundStyle: {
        //         color: 'rgba(180, 180, 180, 0.2)'
        //     }
        // }]
    };

    $.get('/featureVar').done(function (data) {

        myData = data


        myChart.setOption({
            series: [{
                type: 'bar',
                data: myData,
                showBackground: true,
                backgroundStyle: {
                    color: 'rgba(180, 180, 180, 0.2)'
                },
                label: {
                    show: false
                }

            }]
        });
    });

    myChart.setOption(option);
});
