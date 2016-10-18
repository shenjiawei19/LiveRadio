$(function(){
    $('#search_monitor').on('click',function() {
        var day = $("#day").val();
        alert(day);
        var name = $("#name").val();
        alert(name);
            $.get("", {
                "day": day
                }, function (data) {
                    alert(data.name);
            });
    })

});