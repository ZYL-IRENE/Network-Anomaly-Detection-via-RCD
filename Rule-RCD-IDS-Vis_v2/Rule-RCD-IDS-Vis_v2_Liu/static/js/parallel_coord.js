$(function (){
    var myChart = echarts.init(document.getElementById('parallel_coord'));
    var rawdata=[];

    var option = {
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
            rawdata.push(tmpdata);
        }  
        
        myChart.setOption({
            series: {
                type: 'parallel',
                lineStyle: {
                    width: 0.5
                },
                data: rawdata
            }
        });
    });

    myChart.setOption(option);
});
