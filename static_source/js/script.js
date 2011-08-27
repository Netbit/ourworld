
$(document).ready(function(){
    $('.point').click(function() {
    	$('.search-path').css('display','none');
    	$('.search-place').css('display','block');
    	$('.box').css('width', '332px');
	});
    
    $('.path').click(function() {
    	$('.search-place').css('display','none');
    	$('.search-path').css('display', 'block');
    	$('.box').css('width', '570px');
	});
    
    $('.swap').click(function() {
    	var temp = $('#a').val();
    	$('#a').val($('#b').val());
    	$('#b').val(temp);
    });
    
    $("#p").autocomplete("lookup/", { 
    	autoFill: true,
        max: 10,
    });
    
    $("#a").autocomplete("lookup/", { 
    	autoFill: true,
        max: 10,
    });
    
    $("#b").autocomplete("lookup/", { 
    	autoFill: true,
        max: 10,
    });
});