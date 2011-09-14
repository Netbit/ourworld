var map;
var markersArray = [];
var destinationIcon = "http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=D|FF0000|000000";
var originIcon = "http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=O|FFFF00|000000";
var geocoder;
var bounds;

function get_info_of_place(marker) {	
	$.ajax({
	  url: "/info/" + marker.id,
	  beforeSend: function() {
		  alert("before");
	  },
	  success: function(data){
	    alert(data);
	  },
	  error: function() {
		alert("Error");
	  }
	});
	
	var contentString = 'Hello';
	var infowindow = new google.maps.InfoWindow({
		content : contentString
	});
	return infowindow;
}

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

	var marker;
	var infowindow;

	geocoder.geocode({
		'address' : address
	}, function(results, status) {
		if (status == google.maps.GeocoderStatus.OK) {
			map.setCenter(results[0].geometry.location);
			marker = new google.maps.Marker({
				map : map,
				position : results[0].geometry.location,
				id: 1
			});
			google.maps.event.addListener(marker, 'click', function() {
				infowindow = get_info_of_place(marker);
				infowindow.open(map, marker);
			});
		} else {
			alert("Geocode was not successful for the following reason: "
					+ status);
		}
	});
	
	var length = "{{ length }}";
	var location = "{{ location }}";
	var con = document.document.getElementById("construction");
	var index;
	for (var i = 0; i < lenght; i++) {
		index = '' + i;
		con.add(new Option(location[i],index));
	}
					
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

function calculateDistances(origin, destination) {
	var service = new google.maps.DistanceMatrixService();
	service.getDistanceMatrix({
		origins : [ origin, ],
		destinations : [ destination, ],
		travelMode : google.maps.TravelMode.DRIVING,
		unitSystem : google.maps.UnitSystem.METRIC,
		avoidHighways : false,
		avoidTolls : false
	}, callback);
}

function callback(response, status) {
	if (status != google.maps.DistanceMatrixStatus.OK) {
		alert('Error was: ' + status);
	} else {
		var origins = response.originAddresses;
		var destinations = response.destinationAddresses;
		var outputDiv = document.getElementById('content');
		outputDiv.innerHTML = '';
		deleteOverlays();

		for ( var i = 0; i < origins.length; i++) {
			var results = response.rows[i].elements;
			addMarker(origins[i], false);
			for ( var j = 0; j < results.length; j++) {
				addMarker(destinations[j], true);
				outputDiv.innerHTML += "<b>" + gettext("From") + "</b>: " + origins[i] + "<br>" +
									   "<b>" + gettext("To") + "</b>: " + destinations[j] + "<br>" +
									   "<b>" + gettext("Distance") + "</b>: " + results[j].distance.text + "<br>" +
									   "<b>" + gettext("Time") + "</b>: " + results[j].duration.text + " " +
									   gettext("(by car)");
			}
			$('#box').fadeIn('slow').show();
			$('#show-box').hide();
		}
	}
}

function addMarker(location, isDestination) {
	var icon;
	if (isDestination) {
		icon = destinationIcon;
	} else {
		icon = originIcon;
	}
	geocoder.geocode({
		'address' : location
	}, function(results, status) {
		if (status == google.maps.GeocoderStatus.OK) {
			bounds.extend(results[0].geometry.location);
			map.fitBounds(bounds);
			var marker = new google.maps.Marker({
				map : map,
				position : results[0].geometry.location,
				icon : icon
			});
			markersArray.push(marker);
		} else {
			alert("Geocode was not successful for the following reason: "
					+ status);
		}
	});
}

function deleteOverlays() {
	if (markersArray) {
		for (i in markersArray) {
			markersArray[i].setMap(null);
		}
		markersArray.length = 0;
	}
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
				calculateDistances(start, end);
				showSteps(result);
			}
		});
	});

	$('.point').click(function() {
		$('.search-path').css('display', 'none');
		$('.search-place').css('display', 'block');
		$('.box-search').css('width', '332px');
	});

	$('.path').click(function() {
		$('.search-place').css('display', 'none');
		$('.search-path').css('display', 'block');
		$('.box-search').css('width', '570px');
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
			var value = obj.options[obj.selectedIndex].value;
			window.open('?lang=' + value, '_self', false);
		} catch (e) {
			alert(e);
		}
	});

	$('#hidden-popup').click(function() {
		$('#box').fadeOut('slow').hide();
		$('#show-box').show();
	});

	$('#show-popup').click(function() {
		$('#show-box').hide();
		$('#box').fadeIn('slow').show();
	});
});
