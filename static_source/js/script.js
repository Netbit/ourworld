
$(document).ready(function(){
    $('.point').click(function() {
    	$('.search-path').css('display','none');
    	$('.search-place').css('display','block');
    	$('.box').css('width', '332px');
    	$('#p').focus();
	});
    
    $('.path').click(function() {
    	$('.search-place').css('display','none');
    	$('.search-path').css('display', 'block');
    	$('.box').css('width', '570px');
    	$('#a').focus();
	});
    
    $('.swap').click(function() {
    	var temp = $('#a').val();
    	$('#a').val($('#b').val());
    	$('#b').val(temp);
    });
});