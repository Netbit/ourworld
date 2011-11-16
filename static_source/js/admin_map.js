function initialize() {
	var address;

	address = "Ho Chi Minh City";
	geocoder = new google.maps.Geocoder();
	bounds = new google.maps.LatLngBounds();
	geocoder.geocode({
		'address' : address
	}, function(results, status) {
		if (status == google.maps.GeocoderStatus.OK) {
			var myOptions = {
				zoom : 20,
				center : results[0].geometry.location,
				mapTypeId : google.maps.MapTypeId.ROADMAP
			};
			map = new google.maps.Map(document.getElementById("my_map"),
					myOptions);
		} else {
			alert("Geocode was not successful for the following reason: "
					+ status);
		}
	});
}

$(document).ready(function() {
	$('#id_name').css('width', '400px');
	$('#id_name_vi').css('width', '400px');
	$('#id_name_en').css('width', '400px');
	$('#id_unsigned_name').css('width', '400px');
	
	$('#id_description_detail_vi').css('width', '610px');
	$('#id_description_detail_en').css('width', '610px');
	$('#id_description_other_vi').css('width', '610px');
	$('#id_description_other_en').css('width', '610px');
	$('#id_location').css('width', '400px');
	$('#id_location').attr('readonly', true);
	
	
	$('.location').append("<div style='width: 550px; height:400px' id='my_map'></div>");
	initialize();
});