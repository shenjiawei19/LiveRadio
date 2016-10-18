$(function(){
    $('#add_radio').on('click',function() {
        var title = $("#ra_title").val();
        var description = $("#ra_des").val();
        var channel = $("#ra_cha").val();
        var start_time = $("#ra_start").val();
        var finish_time =$("#ra_finish").val();
            $.get("add_radio", {
                "title": title,
                "description": description,
                "channel": channel,
                "start_time": start_time,
                "finish_time": finish_time
                }, function (data) {
                    if (typeof(data.error) == "undefined") {
                        $('#myRadio').modal('hide');
                    }
                    else if (data != '') {
                        var error_message = data.error;
                        $("#Error").html(error_message);
                }
            });
    })
    
});
