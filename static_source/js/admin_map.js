var marker = null;
var map;

function initialize() {
	var address;
	var location;
	var pos;
	
	address = "Ho Chi Minh City";
	geocoder = new google.maps.Geocoder();
	bounds = new google.maps.LatLngBounds();
	geocoder.geocode({
		'address' : address
	}, function(results, status) {
		if (status == google.maps.GeocoderStatus.OK) {
			var myOptions = {
				zoom : 16,
				center : results[0].geometry.location,
				mapTypeId : google.maps.MapTypeId.ROADMAP
			};
			map = new google.maps.Map(document.getElementById("my_map"),
					myOptions);
			location = document.getElementById('id_location').value;
	
			if ("" != location) {
				if (null != marker) {
					marker.setMap(null);
				}
				location = location.replace("(","[");
				location = location.replace(")","]");
				location = eval(location);
				pos = new google.maps.LatLng(location[0], location[1]);
				map.setCenter(pos);
				marker = new google.maps.Marker({
					map : map,
					draggable:true,
					position : pos,
				});	
				google.maps.event.addListener(marker, 'drag', function() {	
					document.getElementById('id_location').value = "(" + marker.position.Pa + "," + marker.position.Qa + ")";
				});	
			}			
		} else {
			alert("Geocode was not successful for the following reason: "
					+ status);
		}
	});
}

function search_place()
{
	var address;
	
	address  = document.getElementById('id_number_or_alley').value + " "
			   + $("#id_street option:selected").text() + ", "
			   + $("#id_ward option:selected").text() + ", "
			   + $("#id_district option:selected").text() + ", Ho Chi Minh" ;
	if (null != marker) {
		marker.setMap(null);
	}
	geocoder = new google.maps.Geocoder();
	geocoder.geocode({
		'address' : address
	}, function(results, status) {
		if (status == google.maps.GeocoderStatus.OK) {
			map.setCenter(results[0].geometry.location);
			document.getElementById('id_location').value = "(" + results[0].geometry.location.Pa + "," + results[0].geometry.location.Qa + ")";
			marker = new google.maps.Marker({
				map : map,
    			draggable:true,
				position : results[0].geometry.location,
				address : results[0].formatted_address
			});
			google.maps.event.addListener(marker, 'drag', function() {	
				document.getElementById('id_location').value = "(" + marker.position.Pa + "," + marker.position.Qa + ")";
			});
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
	$('.location').append("<input type='button' value='search' onclick='search_place()'/>");
	initialize();
});

