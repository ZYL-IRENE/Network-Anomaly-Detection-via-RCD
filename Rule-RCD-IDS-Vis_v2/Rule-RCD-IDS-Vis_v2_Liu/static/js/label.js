window.οnlοad=function () {
    var center = [];

    $.get('/centerArray').done(function (data) {
        center = data;

        for (var i=0;i<center.length;i++) {
            var text=window.prompt("Group "+i.toString()+"'s center data point is point "+(center[i]+1).toString()+
                                    "\nThis group's type is:\n(Please select one from normal,DOS,PROBE,U2R,R2L)","normal");
            if (text!=null && text!="") {
                $.post(
                    "/labelArray",
                    {label: text}
                );
            }   
        } 
    });
}