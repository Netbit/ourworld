
$(document).ready(function(){

  	var address; 
  	var geocoder;
  	var map;
  	
  	//$("body").load(function(){
		address = "Hồ Chí Minh";
	 	geocoder = new google.maps.Geocoder();
		geocoder.geocode({'address': address}, function(results, status) {
	      	if (status == google.maps.GeocoderStatus.OK) {
	      		var myOptions = {
	     							zoom: 13,
	      							center: results[0].geometry.location,
	      							mapTypeId: google.maps.MapTypeId.ROADMAP
	    	  					};
	      		map = new google.maps.Map(document.getElementById("my_map"), myOptions);
	      	} else {
	        	alert("Geocode was not successful for the following reason: " + status);
	      	}
    	});
  	//});
	

	
  	$('#search_place').click(function() {
	    address = document.getElementById("p").value;
	    geocoder.geocode({'address': address}, function(results, status) {
	    	if (status == google.maps.GeocoderStatus.OK) {
	    		map.setCenter(results[0].geometry.location);
	    		var marker = new google.maps.Marker({
	    							map: map,
	    							position: results.geometry.location
	    							});
	    		
	    	} else {
	    		alert("Geocode was not successful for the following reason: " + status);
	    	}   
	    });
	});

  	
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
});