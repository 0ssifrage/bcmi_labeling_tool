$(document).ready(function(){
    $('.attr').each(function(){
        $(this).children("[data-vid='"+$(this).attr("data-attrv")+"']").addClass("val-selected");
    });
    $(".image-label").hover(function(){
        $("#img-view").attr("src", "/image/" + $(this).attr("data-img"));
    });
    // $(".img-s").Jcrop();
    $(".val").click(function(){
        var img=$(this).closest(".image-label").attr("data-img");
        var attr_id=$(this).closest(".attr").attr("data-attrid");
        var v_id=0;
        var ths = this;
        if (!$(this).hasClass("val-selected"))
            v_id=$(ths).attr("data-vid");

        $.ajax({
            type:"POST",
            url:"/update",
            data:{"img":img,"attr_id":attr_id,"v_id":v_id}
        }).done(function(data){
            if ($(ths).hasClass("val-selected")){
                $(ths).removeClass("val-selected");
            }else{
                $(ths).siblings().each(function(){
                    $(this).removeClass("val-selected");
                });
                $(ths).addClass("val-selected");
            };
        });
    });
    $(".img-reg").each(function(){
        var t=$(this).parent().siblings(".reg");
        var btn=t.find(".reg-submit");
        var x1=btn.attr("data-x1");
        var y1=btn.attr("data-y1");
        var x2=btn.attr("data-x2");
        var y2=btn.attr("data-y2");

        var showCoords = function(c) {
            var s = "x1: "+c.x+", y1: "+c.y+", x2: "+c.x2+", y2: "+c.y2;
            t.find(".xy-show").val(s);
            // console.log(btn.attr("data-init"));
            var init = btn.attr("data-init");
            if (btn.attr("data-init") == 0) {
                btn.removeClass("btn-success");
                btn.addClass("btn-danger");
            } else {
                btn.attr("data-init", init-1);
            }
            btn.attr("data-x1", c.x);
            btn.attr("data-y1", c.y);
            btn.attr("data-x2", c.x2);
            btn.attr("data-y2", c.y2);
        };
        if (x2==0 && y2==0) {
            $(this).Jcrop({
                onChange: showCoords,
                onSelect: showCoords
            });
        } else {
            $(this).Jcrop({
                setSelect: [x1, y1, x2, y2],
                onChange: showCoords,
                onSelect: showCoords
            });
        }
    });
    $(".reg-submit").click(function(){
        var img=$(this).closest(".image-label").attr("data-img");
        var x1=$(this).attr("data-x1");
        var y1=$(this).attr("data-y1");
        var x2=$(this).attr("data-x2");
        var y2=$(this).attr("data-y2");
        var regid=$("#regid").attr("data-regid");
        $(this).removeClass("btn-danger");
        var ths = this;
        $.ajax({
            type:"POST",
            url:"/update_region",
            data:{"img":img,"x1":x1,"y1":y1,"x2":x2,"y2":y2,"regid":regid}
        }).done(function(data){
            $(ths).addClass("btn-success");
        });
    });
});
