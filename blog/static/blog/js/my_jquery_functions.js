
    $("#publish").unbind('click').click(function(){
        var title = $("#title")[0].value;
        var classify = $("#classify")[0].value;
        var keywords = $("#keywords")[0].value;
        var article = $("#article")[0].value;
        $.post("publish_article", {title, classify, keywords, article}, function (data) {
            if(data.status == "right"){
            }
            else{
            }
        })
    })
});




