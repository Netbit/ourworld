var map;
var markersArray = [];
var destinationIcon = "http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=D|FF0000|000000";
var originIcon = "http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=O|FFFF00|000000";
var geocoder;
var bounds;
var kind_person;
var kind_construction;
var start_image_person; //Start index to show images of kind of person
var end_image_person;   //End index to show images of kind of person
var start_image_con;	//Start index to show images of kind of construction
var end_image_con;		//End index to show images of kind of construction
var directionsService;
var directionsDisplay;

kind_person       	= new Array();
kind_construction 	= new Array();
start_image_person  = 0;
end_image_person    = 6;
start_image_con 	= 0;
end_image_con		= 6;

function initialize() {
	var address;
	var district;

	directionsService = new google.maps.DirectionsService();
	directionsDisplay = new google.maps.DirectionsRenderer();
	address = "Ho Chi Minh City";
	geocoder = new google.maps.Geocoder();
	bounds = new google.maps.LatLngBounds();
	geocoder.geocode({
		'address' : address
	}, function(results, status) {
		if (status == google.maps.GeocoderStatus.OK) {
			var myOptions = {
				zoom : 13,
				streetViewControl: true,
				panControl: true,
				overviewMapControl: true,
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
		//deleteOverlays();

		for ( var i = 0; i < origins.length; i++) {
			var results = response.rows[i].elements;
			//addMarker(origins[i], false);
			for ( var j = 0; j < results.length; j++) {
				//addMarker(destinations[j], true);
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

	geocoder.geocode({
		'address' : location
	}, function(results, status) {
		if (status == google.maps.GeocoderStatus.OK) {
			bounds.extend(results[0].geometry.location);
			map.fitBounds(bounds);
			var marker = new google.maps.Marker({
				map : map,
				position : results[0].geometry.location,
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
	
	$('#load').hide();
	get_kind_of_person_construction();
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
//		var directionsService = new google.maps.DirectionsService();
//		var directionsDisplay = new google.maps.DirectionsRenderer();
		directionsDisplay.setMap(map);

		directionsService.route(request, function(result, status) {
			if (status == google.maps.DirectionsStatus.OK) {
				directionsDisplay.setDirections(result);
				calculateDistances(start, end);
				//showSteps(result);
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

function set_location(id, address, location) {
	var pos = new google.maps.LatLng(location[0], location[1]);
	var marker = new google.maps.Marker({
		map : map,
		id: id,
		address : address,
		position : pos,
		zIndex: Math.ceil(Math.random()*1111)
	});
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
	markersArray.push(marker);
}

function kind_construction_filter(id) {		
	$.ajax({                                                                  
		url : "/filter/kind_construction/?id1=" + id + "&district_id=" + $('#district').val(),
		beforeSend : function() {
			deleteOverlays();
			$('#load').show();			
		},
    	success : function(data) {    		
    		for (var i = 0; i < data.results.length; i++) {
    			if (data.results[i].location.length == 0) {
					search_place(data.results[i].id, data.results[i].address);
    			} else {
    				set_location(data.results[i].id, data.results[i].address, data.results[i].location);
    			}    			
    		}
    		$('#load').hide();
    	},                                                                    
    	error : function(e) { 
    		$('#load').hide();
    		alert(gettext("Couldn't get the data!"));                                                 
    	}                                                                     
    });   
}

function kind_person_filter(id) {	
	$.ajax({                                                                  
		url : "/filter/kind_person/?id1=" + id  + "&district_id=" + $('#district').val(), 
		beforeSend : function() {
			deleteOverlays();
			$('#load').show();			
		},
    	success : function(data) {    		
    		for (var i = 0; i < data.results.length; i++) {
    			if (data.results[i].location.length == 0) {
					search_place(data.results[i].id, data.results[i].address);
    			} else {
    				set_location(data.results[i].id, data.results[i].address, data.results[i].location);
    			}
    		}
    		$('#load').hide();    	},                                                                        	error : function(e) {         
    		$('#load').hide();    		alert(gettext("Couldn't get the data!"));                                                     	}                                                                         });   
}

function district_filter(id_district) {
	$.ajax({
		url : "/filter/district/?id_district=" + id_district,
		beforeSend : function() {
			deleteOverlays();
			$('#load').show();						
		},
		success : function(data) {			
    		for (var i = 0; i < data.results.length; i++) {
    			if (data.results[i].location.length == 0) {
					search_place(data.results[i].id, data.results[i].address);
    			} else {
    				set_location(data.results[i].id, data.results[i].address, data.results[i].location);
    			}
    		}
    		$('#load').hide();
		},
		error : function(e) {
			$('#load').hide();
			alert(gettext("Couldn't get the data!"));
		}
	});
}

function create_image_list(images, start, end, id_div)
{
	var htmlString;
	htmlString = "";
	do {
		if ("left" == id_div) {
			htmlString += create_element(images[start].name, images[start].id, images[start].image, 
											"kind_person_filter", "left");
		} else {
			htmlString += create_element(images[start].name, images[start].id, images[start].image, 
											"kind_construction_filter", "right");
		}		
		start++;
	}while (start < end)
	
	return htmlString;
}

function create_element(name, id, image, func, id_div)
{
	var htmlString;
	htmlString = "<span class='icon'>";
	if ("left" == id_div) {
		htmlString += "<a onclick=" + func + "('" + id + "')>"
					  + "<img id='p" + id + "'";
	} else if ("right" == id_div) {
		htmlString += "<a onclick=" + func + "('" + id + "')>"
					  + "<img id='p" + id + "'";	
	} else {
		htmlString += "<a onclick=" + func + "('" + id + "')>"
			  + "<img id='" + id + "'";
	}
	htmlString += " title='" + name + "'"  
				   + " height='32'" 
				   + " alt='" + name + "'" 
				   + " src='" + image + "'>"
				   + "</img></a></span>";
	return htmlString;
}

function image_slider(id_button)
{		
	var htmlString = "";
	switch (id_button) {
	case "left_next_button":
		start_image_person++;
		end_image_person++;
		htmlString = create_element("Previous", "left_prev_button", "/static/images/left_prev_button.png", 
										"image_slider", null)
					+ create_image_list(kind_person, start_image_person, end_image_person, "left");  
		if (end_image_person < kind_person.length) {
			htmlString += create_element("Next", "left_next_button", "/static/images/left_next_button.png", 
										"image_slider", null);	
		}
		$('#left').html(htmlString);
		break;
	case "left_prev_button":
		start_image_person--;
		end_image_person--;
		if (0 < start_image_person) {
			htmlString = create_element("Previous", "left_prev_button", "/static/images/left_prev_button.png", 
										"image_slider", null);
		}
		htmlString += create_image_list(kind_person, start_image_person, end_image_person, "left")  
					+ create_element("Next", "left_next_button", "/static/images/left_next_button.png", 
										"image_slider", null);	
		$('#left').html(htmlString);
		break;
	case "right_next_button":
		start_image_con++;
		end_image_con++;
		htmlString = create_element("Previous", "right_prev_button", "/static/images/right_prev_button.png", 
										"image_slider", null)
					+ create_image_list(kind_construction, start_image_con, end_image_con, "right");  
		if (end_image_con < kind_construction.length) {
			htmlString += create_element("Next", "right_next_button", "/static/images/right_next_button.png", 
										"image_slider", null);	
		}
		$('#right').html(htmlString);
		break;
	case "right_prev_button":
		start_image_con--;
		end_image_con--;
		if (0 < start_image_con) {
			htmlString = create_element("Previous", "right_prev_button", "/static/images/right_prev_button.png", 
										"image_slider", null);
		}
		htmlString += create_image_list(kind_construction, start_image_con, end_image_con, "left")  
					+ create_element("Next", "right_next_button", "/static/images/right_next_button.png", 
										"image_slider", null);	
		$('#right').html(htmlString);
		break;
	}
}

function disable_button(id_button)
{
	var img;
	img = document.getElementById(id_button);
	img.display  = "none";
}


function get_kind_of_person_construction()
{
	$.ajax({
		url : "/get/person_construction/",
		success : function(data) {
			var i;
			var htmlString;
			htmlString = "";
    		for (i = 0; i < data.kind_person.length; i++) {
    			kind_person.push(data.kind_person[i]);
    		}
    		
    		for (i = 0; i < data.kind_construction.length; i++) {
    			kind_construction.push(data.kind_construction[i]);
    		}	
    		
    		if (end_image_person > kind_person.length) {
    			end_image_person = kind_person.length;
    		}
 			htmlString = create_image_list(kind_person, start_image_person, end_image_person, "left");
 			if (kind_person.length > end_image_person) {
 				htmlString += create_element("Next", "left_next_button", "/static/images/left_next_button.png", 
 											"image_slider", null);
 			}   				
 			$('#left').html(htmlString);
 			
 			if (end_image_con > kind_construction.length) {
    			end_image_person = kind_construction.length;
    		}
 			htmlString = create_image_list(kind_construction, start_image_con, end_image_con, "right");
 			if (kind_construction.length > end_image_con) {
 				htmlString += create_element("Next", "right_next_button", "/static/images/right_next_button.png", 
											"image_slider", null);	
 			}  	
 			
 			$('#right').html(htmlString);
		},
		error : function(e) {
			alert(gettext("Couldn't get the data of kind of person and construction!"));
		}
	});
}

