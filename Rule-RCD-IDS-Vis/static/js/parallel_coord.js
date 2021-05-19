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

function DrawParallel() {
    var myChart = echarts.init(document.getElementById('parallel_coord'));
    var rawdata=[];

    var option = {
        // backgroundColor: '#333',
        parallelAxis: [
            {dim: 0, name: 'id'},

            {dim: 2, name: 'duration'},
            {
                dim: 3,
                name: 'service',
                type: 'category',
                data: ['http', 'ecr_i','smtp','domain_u','auth','finger']
            },
            {
                dim: 4, 
                name: 'flag',
                type: 'category',
                data: ['SF']
            },
            {dim: 5, name: 'src_bytes'},
            {dim: 6, name: 'dst_bytes'},
            {dim: 7, name: 'count'},
            {dim: 8, name: 'serror_rate'},
            {dim: 9, name: 'srv_rerror_rate'},
            {dim: 10, name: 'same_srv_rate'},
            {dim: 11, name: 'dst_host_count'},
            {dim: 12, name: 'dst_host_srv_count'},
            {dim: 13, name: 'dst_host_same_src_port_rate'},
            {dim: 14, name: 'dst_host_serror_rate'},
            {dim: 15, name: 'dst_host_srv_serror_rate'},
        ],
        parallel: {
            // axisExpandable: true,
            // axisExpandCenter: 0,
            // axisExpandCount: 8,
            // axisExpandWidth: 70,
            // axisExpandTriggerOn: 'mousemove',
            top: 50,
            bottom: 10,       
            left: 50,
            right: 100,
            // height: '90%',
            // width: '70%',
            parallelAxisDefault: {
                type: 'value',
                nameLocation: "end",
                nameRotate: 30,
                nameGap: 5,
            }
        }
    };
    $.get('/parallelQuery').done(function (data) {
        console.log("parallel data");
        // rawdata = data;
        console.log(data.length);  
        console.log(data);
        for(var i=0;i<data.length;i++){
            var tmpdata = [];
            tmpdata.push(data[i].id);
            tmpdata.push(data[i].class);
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
            rawdata.push(tmpdata);
        }  
        console.log(rawdata); 
        
        myChart.setOption({
            series: {
                type: 'parallel',
                lineStyle: {
                    width: 0.5
                },
                // smooth: true,
                data: rawdata
            }
        });
    });

    // 使用刚指定的配置项和数据显示图表。  
    myChart.setOption(option);
}

addLoadEvent(DrawParallel);
