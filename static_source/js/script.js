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
var media = "/static/";

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
						contentString += "<span class='place_name'>" + data.results.name + "</span>" + 
						 "<span style='float: right'><img onclick=\"revertStyles(); return false;\" id=\"font-large\" alt=\"" + gettext("Default") + "\" title=\"" + gettext("Default") + "\" src=\"" + media + "images/font_default.jpg\">" + 
						 "<img onclick=\"changeFontSize(-1); return false;\" id=\"font-small\" alt=\"" + gettext("Zoom out") + "\" title=\"" + gettext("Zoom out") + "\" src=\"" + media + "images/font_small.jpg\">" +
						 "<img onclick=\"changeFontSize(1); return false;\" id=\"font-large\" alt=\"" + gettext("Zoom in") + "\" title=\"" + gettext("Zoom in") + "\" src=\"" + media + "images/font_large.jpg\"></span><br>" +
						 "<span class='place_address'>" + marker.address + "</span><br>" +
						 "<span id='content' class='place_details'>" + data.results.details + "</span><br>" +
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

		for ( var i = 0; i < origins.length; i++) {
			var results = response.rows[i].elements;
			for ( var j = 0; j < results.length; j++) {
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

function deleteOverlays() {
	directionsDisplay.setMap(null);
	if (markersArray) {
		for (i in markersArray) {
			markersArray[i].setMap(null);
		}
		markersArray.length = 0;
	}	
}

$(document).ready(function() {
	
	$('#load').hide();

	$("#slider_left").easySlider({
		auto: true, 
		continuous: true,
		prevId: 		'prevBtn_left',
		nextId: 		'nextBtn_left',
		firstId: 		'firstBtn_left',
		lastId: 		'lastBtn_left'
	});
	
	$("#slider_right").easySlider({
		auto: true, 
		continuous: true,
		prevId: 		'prevBtn_right',
		nextId: 		'nextBtn_right',
		firstId: 		'firstBtn_right',
		lastId: 		'lastBtn_right'
	});
	
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

		directionsService.route(request, function(result, status) {
			if (status == google.maps.DirectionsStatus.OK) {
				directionsDisplay.setDirections(result);
				directionsDisplay.setMap(map);				
				calculateDistances(start, end);
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
		$('.box-search').css('width', '580px');
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

function set_location(id, address, location, icon) {
	var pos = new google.maps.LatLng(location[0], location[1]);
	var marker = new google.maps.Marker({
		map : map,
		id: id,
		address : address,
		position : pos,
		icon: icon,
		zIndex: Math.round(pos.lat()*-100000)<<5
	});
	google.maps.event.addListener(marker, 'click', function() {
		var contentString = "";
		$.getJSON("/info/" + marker.id + "/?address=" + address, function(data) {
			if (data.results.hasOwnProperty('details')) {
				contentString += "<div>";
				
				if (data.results.image != "") {
					contentString += "<img style='float: left' height='100' src='" + data.results.image + "'>";				
				}
				contentString += "<span class='place_name'>" + data.results.name + "</span>" + 
					 "<span style='float: right'><img onclick=\"revertStyles(); return false;\" id=\"font-large\" alt=\"" + gettext("Default") + "\" title=\"" + gettext("Default") + "\" src=\"" + media + "images/font_default.jpg\">" + 
					 "<img onclick=\"changeFontSize(-1); return false;\" id=\"font-small\" alt=\"" + gettext("Zoom out") + "\" title=\"" + gettext("Zoom out") + "\" src=\"" + media + "images/font_small.jpg\">" +
					 "<img onclick=\"changeFontSize(1); return false;\" id=\"font-large\" alt=\"" + gettext("Zoom in") + "\" title=\"" + gettext("Zoom in") + "\" src=\"" + media + "images/font_large.jpg\"></span><br>" +
					 "<span class='place_address'>" + marker.address + "</span><br>" +
					 "<span id='content' class='place_details'>" + data.results.details + "</span><br>" +
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
    		var loc = null;
    		for (var i = 0; i < data.results.length; i++) {
    			if (data.results[i].location.length == 0) {
					search_place(data.results[i].id, data.results[i].address);
    			} else {
    				set_location(data.results[i].id, data.results[i].address, data.results[i].location, data.results[i].icon);
    				loc = data.results[i].location;
    			}    			
    		}
    		$('#load').hide();
    		if (loc) {
    			var lat = new google.maps.LatLng(loc[0],loc[1]);
    			map.setCenter(lat);
    		}    		
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
    		var loc = null;
    		for (var i = 0; i < data.results.length; i++) {
    			if (data.results[i].location.length == 0) {
					search_place(data.results[i].id, data.results[i].address);
    			} else {
    				set_location(data.results[i].id, data.results[i].address, data.results[i].location, data.results[i].icon);
    				loc = data.results[i].location;
    			}
    		}
    		$('#load').hide();
    		if (loc) {
    			var lat = new google.maps.LatLng(loc[0],loc[1]);
    			map.setCenter(lat);
    		}    	},                                                                        	error : function(e) {         
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
			var loc = null;
    		for (var i = 0; i < data.results.length; i++) {
    			if (data.results[i].location.length == 0) {
					search_place(data.results[i].id, data.results[i].address);
    			} else {
    				set_location(data.results[i].id, data.results[i].address, data.results[i].location, data.results[i].icon);
    				loc = data.results[i].location;
    			}
    		}
    		$('#load').hide();
    		if (loc) {
    			var lat = new google.maps.LatLng(loc[0],loc[1]);
    			map.setCenter(lat);
    		}
		},
		error : function(e) {
			$('#load').hide();
			alert(gettext("Couldn't get the data!"));
		}
	});
}

function showTooltip(id, msg) {
	$("#" + id).tooltip({ 
	    bodyHandler: function() { 
	        return "<span>" + msg + "</span>"; 
	    }, 
	    showURL: false 
	});
}

function killEnter(evt) {
	if(evt.keyCode == 13 || evt.which == 13) {
		return false;
	}
	return true;
}