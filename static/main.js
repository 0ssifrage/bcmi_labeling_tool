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
            type: "POST",
            url: "/update",
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
});
