var myTable = $('#view_table');
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
                    strHtml = "<select class='ss' ><option value='normal' >normal</option><option value='DOS' selected='selected'>DOS</option><option value='PROBE'>PROBE</option><option value='U2R'>U2R</option><option value='R2L'>R2L</option></select>";
                }
                else if (value == "PROBE") {
                    strHtml = "<select class='ss' ><option value='normal' >normal</option><option value='DOS'>DOS</option><option value='PROBE' selected='selected'>PROBE</option><option value='U2R'>U2R</option><option value='R2L'>R2L</option></select>";
                }
                else if (value == "U2R") {
                    strHtml = "<select class='ss' ><option value='normal' >normal</option><option value='DOS'>DOS</option><option value='PROBE'>PROBE</option><option value='U2R' selected='selected'>U2R</option><option value='R2L'>R2L</option></select>";
                }
                else if (value == "R2L") {
                    strHtml = "<select class='ss' ><option value='normal' >normal</option><option value='DOS'>DOS</option><option value='PROBE'>PROBE</option><option value='U2R'>U2R</option><option value='R2L' selected='selected'>R2L</option></select>";
                }
                else
                    strHtml = "<select class='ss' onchange='Change($(this))'><option value='normal' selected='selected'>normal</option><option value='DOS'>DOS</option><option value='PROBE'>PROBE</option><option value='U2R'>U2R</option><option value='R2L'>R2L</option></select>";
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

function Change(obj) {
    console.log("lalala");
    var indexSelected = obj.parent().parent()[0].rowIndex - 1;
    var valueSelected = obj.children('option:selected').val();
    console.log(indexSelected,valueSelected);
    myTable.bootstrapTable('updateCell', {
        index: indexSelected,
        field: 'class',
        value: valueSelected
    })
}

