
	function getRandomSize(min, max) {
	  return Math.round(Math.random() * (max - min) + min);
}
if (window.location.href === "/"){
window.onload=function(){

var allImages = "";


	$.ajax({
		url:"/shops",
		success:function(data){
			var width,height,shops=data.shops,name;
for (var i = 0; i < shops.length; i++) {
	  width = getRandomSize(200, 400);
	  height = getRandomSize(200, 400);
	  name=shops[i].name;
	  allImages += '<img src="/uploads/'+shops[i].pic+'" style="width:' + width + 'px;height:' + height + 'px;" alt="'+name+'">';
		}
		}
	});


photos.innerHTML = allImages
}
}
