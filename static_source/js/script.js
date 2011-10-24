var map;
var markersArray = [];
var destinationIcon = "http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=D|FF0000|000000";
var originIcon = "http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=O|FFFF00|000000";
var geocoder;
var bounds;
var kind_person;
var kind_construction;
var index_kind_person;
var index_kind_construction;

kind_person       		= new Array();
kind_construction 		= new Array();
index_kind_person 		= 0;
index_kind_construction = 0;

function initialize() {
	var address;
	var district;

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

	district = document.getElementById('district');
	district_filter(district.options[district.selectedIndex].value);
}

function search_place(id, address) {

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
				id : id,
				address : results[0].formatted_address
			});
			markersArray.push(marker);
			google.maps.event.addListener(marker, 'click', function() {
				var contentString = "";
				$.getJSON("/info/" + marker.id + "/?address=" + address, function(data) {
					if (data.results.hasOwnProperty('details')) {
						contentString += "<div>";
						if (data.results.image != "") {
							contentString += "<img style='float: left' height='100' src='" + data.results.image + "'>";				
						}
						contentString += "<span class='place_name'>" + data.results.name + "</span><br>" +
										 "<span class='place_address'>" + marker.address + "</span><br>" +
										 "<span class='place_details'>" + data.results.details + "</span><br>" +
										 "<span><a class='more' onclick = \"window.open('/details/" + data.results.id + "/','mywindow','menubar=1,resizable=1,scrollbars=1,width=650,height=550')\">" + gettext("Details...") + "</a></span></div>";
						infowindow = new google.maps.InfoWindow({
							content : contentString
						});
						infowindow.open(map, marker);
					}					
				});				
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
				outputDiv.innerHTML += "<b>" + gettext("From") + "</b>: "
						+ origins[i] + "<br>" + "<b>" + gettext("To")
						+ "</b>: " + destinations[j] + "<br>" + "<b>"
						+ gettext("Distance") + "</b>: "
						+ results[j].distance.text + "<br>" + "<b>"
						+ gettext("Time") + "</b>: " + results[j].duration.text
						+ " " + gettext("(by car)");
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
				icon : icon,
				zIndex: Math.ceil(Math.random()*1111)
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

	get_kind_of_person_construction()
	//add_image_slider(kind_person, "left_slider");
	
	try {
		$("#lang").msDropDown();
		$("#lang_msdd").css('width', '120px');
		$("#lang_child").css('width', '118px');
		if (navigator.userAgent.indexOf("Firefox") != -1 || navigator.userAgent.indexOf("MSIE") != -1) {
			$(".dd").css('top', '0px');
		}
		
	} catch(e) {
		alert(e.message);
	}
	
	initialize();

	$('#search_place').click(function() {
		var address;
		deleteOverlays();
		address = document.getElementById("p").value;
		search_place(0, address);
	});

	$('#search_path').click(function() {
		deleteOverlays();
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

	$('#hidden-popup').click(function() {
		$('#box').fadeOut('slow').hide();
		$('#show-box').show();
	});

	$('#show-popup').click(function() {
		$('#show-box').hide();
		$('#box').fadeIn('slow').show();
	});
	
	$('#district').change(function() {
		var district;
		var id_district;
		try {
			district 	= document.getElementById('district');
			id_district = district.options[district.selectedIndex].value;
			district_filter(id_district);
		} catch (e) {
		}
	});	
});

function changedLanguage(value) {
	window.open('?lang=' + value, '_self', false);
}

function kind_construction_filter(id) {	
	$.ajax({                                                                  
		url : "/filter/kind_construction/?id1=" + id, 
    	success : function(data) {
    		deleteOverlays();
    		for (var i = 0; i < data.results.length; i++) {
    			search_place(data.results[i].id, data.results[i].address);
    		}
    	},                                                                    
    	error : function(e) {  
    		alert(gettext("Couldn't get the data!"));                                                 
    	}                                                                     
    });   
}

function kind_person_filter(id) {	
	$.ajax({                                                                  
		url : "/filter/kind_person/?id1=" + id, 
    	success : function(data) {
    		deleteOverlays();
    		for (var i = 0; i < data.results.length; i++) {
    			search_place(data.results[i].id, data.results[i].address);
    		}    	},                                                                        	error : function(e) {                                                     		alert(gettext("Couldn't get the data!"));                                                     	}                                                                         });   
}

function district_filter(id_district) {
	$.ajax({
		url : "/filter/district/?id_district=" + id_district,
		success : function(data) {
			deleteOverlays();
    		for (var i = 0; i < data.results.length; i++) {
    			search_place(data.results[i].id, data.results[i].address);
    		}
		},
		error : function(e) {
			alert(gettext("Couldn't get the data!"));
		}
	});
}

function add_image_slider(images, id_div) {
	var i;
	var dv;   //Define a tag <div>
	var span; //Define a tag <span>
	var a;    //Define a tag <a>
	var img;  //Define a tag <img>
	
	dv = document.getElementById(id_div);
	
	//Add button prev
	for (i = 0; i < images.length; i++) {
		span           = document.createElement("span");
		span.className = "icon";
		
		a 			   = document.createElement("a");
		a.onclick 	   = "kind_construction_filter(" + images[i].id + ")";
		
		img            = document.createElement("img");
		img.id 		   = images[i].id
		img.title	   = images[i].name;
		img.height     = 32 
		img.alt 	   = images[i].name;
		img.src 	   = "/static/" + images[i].image;
		
		a.appendChild(img);
		span.appendChild(a);
		dv.appendChild(span);
	}
	//Add button next

}

function get_kind_of_person_construction() {
	$.ajax({
		url : "/get/person_construction/",
		success : function(data) {
			var i;
    		for (i = 0; i < data.kind_person.length; i++) {
    			kind_person.push(data.kind_person[i]);
    		}
    		
    		for (i = 0; i < data.kind_construction.length; i++) {
    			kind_construction.push(data.kind_construction[i]);
    		}
    		
    		add_image_slider(kind_person, "left_slider");
		},
		error : function(e) {
			alert(gettext("Couldn't get the data of kind of person and construction!"));
		}
	});
}
