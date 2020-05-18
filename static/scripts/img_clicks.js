function coords($img,e){
    var currentClickPosX = e.pageX - $img.offset().left;
      var currentClickPosY = e.pageY - $img.offset().top;

      var currentWidth = $img.width();
      var currentHeight = $img.height();

      var naturalWidth = {{ img_scale[0] }};
      var naturalHeight = {{ img_scale[1] }};

      var naturalClickPosX = ((naturalWidth / currentWidth) * currentClickPosX).toFixed(0);
    var naturalClickPosY = (naturalHeight-(naturalHeight / currentHeight) * currentClickPosY).toFixed(0);
    return naturalClickPosX + "," + naturalClickPosY;
}
$(".hilbert").on("dblclick", function(e){
    var $img = $(this);
    window.location = "./{{page_name}}?"+coords($img,e);
})
$(".hilbert").on("click",function(e){
    var $img = $(this);
    console.log("poop")
    $img.find('span').text(coords($img,e));
})