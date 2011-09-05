/*
 * Son Tieu test commit 
 */

var map;

function initialize() {
	var address;
	var geocoder;

	address = "Ho Chi Minh City";
	geocoder = new google.maps.Geocoder();
	geocoder.geocode({
		'address' : address
	}, function(results, status) {
		if (status == google.maps.GeocoderStatus.OK) {
			var myOptions = {
				zoom : 13,
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

function search_place(address) {
	var geocoder;

	geocoder = new google.maps.Geocoder();
	geocoder.geocode({
		'address' : address
	}, function(results, status) {
		if (status == google.maps.GeocoderStatus.OK) {
			map.setCenter(results[0].geometry.location);
			var marker = new google.maps.Marker({
				map : map,
				position : results[0].geometry.location
			});
		} else {
			alert("Geocode was not successful for the following reason: "
					+ status);
		}
	});
}

function showSteps(directionResult) {
	// For each step, place a marker, and add the text to the marker's
	// info window. Also attach the marker to an array so we
	// can keep track of it and remove it when calculating new
	// routes.
	var myRoute = directionResult.routes[0].legs[0];

	for ( var i = 0; i < myRoute.steps.length; i++) {
		var marker = new google.maps.Marker({
			position : myRoute.steps[i].start_point,
			map : map
		});
		attachInstructionText(marker, myRoute.steps[i].instructions);
		markerArray[i] = marker;
	}
}

function attachInstructionText(marker, text) {
	google.maps.event.addListener(marker, 'click', function() {
		stepDisplay.setContent(text);
		stepDisplay.open(map, marker);
	});
}

$(document).ready(function() {
	initialize();

	$('#search_place').click(function() {
		var address;

		address = document.getElementById("p").value;
		search_place(address);
	});

	$('#search_path').click(function() {
		var start = document.getElementById("a").value;
		var end = document.getElementById("b").value;
		var request = {
			origin : start,
			destination : end,
			travelMode : google.maps.TravelMode.DRIVING
		};
		var directionsService = new google.maps.DirectionsService();
		var directionsDisplay = new google.maps.DirectionsRenderer();
		directionsDisplay.setMap(map);

		directionsService.route(request, function(result, status) {
			if (status == google.maps.DirectionsStatus.OK) {
				directionsDisplay.setDirections(result);
				showSteps(result);
			}
		});
	});

	$('.point').click(function() {
		$('.search-path').css('display', 'none');
		$('.search-place').css('display', 'block');
		$('.box').css('width', '332px');
	});

	$('.path').click(function() {
		$('.search-place').css('display', 'none');
		$('.search-path').css('display', 'block');
		$('.box').css('width', '570px');
	});

	$('.swap').click(function() {
		var temp = $('#a').val();
		$('#a').val($('#b').val());
		$('#b').val(temp);
	});

	$("#p").autocomplete("lookup/", {
		autoFill : false,
		max : 15,
		multiple : true,
		scroll : true,
		multipleSeparator : " "
	});

	$("#a").autocomplete("lookup/", {
		autoFill : false,
		max : 15,
		multiple : true,
		scroll : true,
		multipleSeparator : " "
	});

	$("#b").autocomplete("lookup/", {
		autoFill : false,
		max : 15,
		multiple : true,
		scroll : true,
		multipleSeparator : " "
	});

	$('.language').change(function() {
		try {
			var obj = document.getElementById('lang');
			var value = obj.options(obj.selectedIndex).value;
			window.open('?lang=' + value, '_self', false);
		} catch (e) {
			alert(e);
		}
	});
});
