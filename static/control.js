var version = 2;
var max_network_checks = 6;
var network_checks = 0;
var finished_test;
var test_mode = true; //will get fake location info if can not find any for help testing

document.addEventListener('DOMContentLoaded',
			  function() {
			      start_function();
			  },
			  false);

function start_function(){
    $.ajax({url: "http://smartfan.net/get_status",
	    method: "GET",
	    success: handleStatus,
	    error: error_func,
	    dataType: 'json',
	    async: true
	   }
	  );
}

function hard_reset(){
    $.ajax({url: "http://smartfan.net/hard_reset",
	    method: "GET",
	    success: handleStatus,
	    error: error_func,
	    dataType: 'json',
	    async: true
	   }
	  );
}

function handleStatus(status){
    display_info(status['inside_temp'],'inside_temp');
    display_info(status['outside_temp'], 'outside_temp');
    display_info(status['mode'], 'mode');
    display_info(status['fan_state'], 'fan_state');
    display_text_area(status['lat'],'lat');
    display_text_area(status['lon'], 'lon');
    display_text_area(status['min_temp'], 'min_temp');
    display_text_area(status['temp_margin'], 'temp_margin');
    display_text_area(status['min_cycle_time'], 'min_cycle_time');
    set_button_status('connect', status['connect_button']);
    set_button_status('refresh', status['refresh_button']);
    set_button_status('set_location', status['set_location_button']);
    set_button_status('set_temperature_preferences', status['set_temperature_preferences_button']);
    set_button_status('turn_automatic_mode_on', status['turn_automatic_mode_on_button']);
    set_button_status('turn_fan_on', status['turn_fan_on_button']);
    set_button_status('turn_fan_off', status['turn_fan_off_button']);
    set_button_status('turn_off_network', status['turn_off_network_button']);
}

function display_info(message, element_id){
    var display = document.getElementById(element_id + '_display');
    display.innerHTML = message;
}

function display_text_area(message, element_id){
    var display = document.getElementById(element_id + '_text_box');
    console.log('set text area');
    console.log(message);
    display.value = message;
}

function set_button_status(element_id, button_info){
    //TODO still need a completed/active indicator
    var button = document.getElementById(element_id + '_button');
    var spinner = document.getElementById(element_id + '_spinner');
    button.disabled = button_info['disabled'];
    if(button_info['spinning']){
	turn_on_spinner(element_id);
    }else{
	turn_off_spinner(element_id);
    }
    if(button_info['active']){
	status.innerHTML = 'active';
	spinner.className = "glyphicon glyphicon-ok"
    }else{
	status.innerHTML = 'inactive';
	if(!button_info['spinning']){
	    spinner.className = ""
	}
    }
}

function turn_on_spinner(element_id){
    var button = document.getElementById(element_id + '_button');
    var spinner = document.getElementById(element_id + '_spinner');
    button.disabled = true;
    spinner.className = "fa fa-spinner fa-spin";
}

function turn_off_spinner(element_id){
    var spinner = document.getElementById(element_id + '_spinner');
    spinner.className = "";
}


function refresh(){
    turn_on_spinner('refresh');
    $.ajax({url: "http://smartfan.net/get_status",
	    method: "GET",
	    error: error_func,
	    async: true,
	    success: handleStatus,
	    dataType: 'json',
	   }
	  );
}

function turn_fan_on(){
    turn_on_spinner('turn_fan_on');
    $.ajax({url: "http://smartfan.net/turn_fan_on",
	    method: "GET",
	    error: error_func,
	    async: true,
	    success: handleStatus,
	    dataType: 'json',
	   }
	  );
}

function turn_fan_off(){
    turn_on_spinner('turn_fan_off');
    $.ajax({url: "http://smartfan.net/turn_fan_off",
	    method: "GET",
	    error: error_func,
	    async: true,
	    success: handleStatus,
	    dataType: 'json',
	   }
	  );
}

function turn_automatic_mode_on(){
    turn_on_spinner('turn_automatic_mode_on');
    $.ajax({url: "http://smartfan.net/turn_automatic_mode_on",
	    method: "GET",
	    error: error_func,
	    async: true,
	    success: handleStatus,
	    dataType: 'json',
	   }
	  );
}

function set_temperature_preferences(){
    turn_on_spinner('set_temperature_preferences');
    minimum_temp = document.getElementById("min_temp_text_box").value;
    temp_margin = document.getElementById("temp_margin_text_box").value;
    min_cycle_time = document.getElementById("min_cycle_time_text_box").value;
    $.ajax({url: "http://smartfan.net/set_temperature_preferences",
	    method: "POST",
	    data: { temp_margin: temp_margin, min_temp: minimum_temp, min_cycle_time:min_cycle_time},
	    async: true,
	    success: handleStatus,
	    dataType: 'json',
	   });
}

function set_location() {
    turn_on_spinner('set_location');
    lon = document.getElementById("lon_text_box").value;
    lat = document.getElementById("lat_text_box").value;
    if (lat === '' || lon=== '' ) {
	if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(set_position, errorPostion);
	} else {
	    alert('It seems your device does not support getting locations. Try entering them manually use another device to find your latitude and longitude by looking up your address at http://www.latlong.net/convert-address-to-lat-long.html');
	    turn_off_spinner('set_location');
	    var button = document.getElementById('set_location_button');
	    button.disabled = false;
	}
    }else{
	alert('using manual coordinates to set your location');
	upload_location(lat, lon);
    }
}

function set_position(position){
    var lat = position.coords.latitude;
    var lon = position.coords.longitude;
    upload_location(lat, lon);
}


function upload_location(lat, lon){
    $.ajax({url: "http://smartfan.net/set_location",
	    method: "POST",
	    data: { lat: lat, lon: lon},
	    async: true,
	    success: handleStatus,
	    dataType: 'json',
	   });
}

function errorPostion(error) {
    alert('It seems your device does not support getting locations. Try entering them manually use another device to find your latitude and longitude by looking up your address at http://www.latlong.net/convert-address-to-lat-long.html')
    turn_off_spinner('set_location');
    var button = document.getElementById('set_location_button');
    button.disabled = false;

    // var geo_display = document.getElementById("geo_display");
    // switch(error.code) {
    //     case error.PERMISSION_DENIED:
    //         geo_display.innerHTML = "You denied the request for you loction. Try again but accept it.";
    //         break;
    //     case error.POSITION_UNAVAILABLE:
    //         geo_display.innerHTML = "Location information is unavailable. Make sure to use a phone not a desktop computer for this";
    //         break;
    //     case error.TIMEOUT:
    //         geo_display.innerHTML = "The request to get user location timed out. Try again.";
    //         break;
    //     case error.UNKNOWN_ERROR:
    //         geo_display.innerHTML = "An unknown error occurred. Try again";
    //         break;
    // }
}

function connect() {
    turn_on_spinner('connect');
    network_checks = 0;
    network = document.getElementById("network").value;
    password = document.getElementById("password").value;
    finished_test = false;
    $.ajax({url: "http://smartfan.net/connect",
	    method: "POST",
	    data: { network_name: network, password: password },
	    success: wait_for_test_to_complete_helper,
	    error: error_func,
	    async: true,
	   });
}

function parse_test_complete(status_info){
    var connected = status_info['connect_button']['active'];
    //are we still even trying or did we totally fail
    var spinning = status_info['connect_button']['spinning'];
    console.log("in parse test complete");
    console.log(spinning);
    console.log(connected);
    console.log(finished_test);

    if(!finished_test){
	handleStatus(status_info);
	if(connected){
	    finished_test = true;
	    alert("Connection worked. Your fan can now get weather information over wifi")
	}else{
	    if(!spinning){
		finished_test = true
		alert('after many attempts still failed to connect make sure your network info is correct');
	    }
	}
    }
}

function error_func(obj, call_error, server_error){
    //TODO
    alert("error I see");
}

function wait_for_test_to_complete_helper(info){
    console.log("in wait");
    window.setTimeout(wait_for_test_to_complete, 10000);
}

function wait_for_test_to_complete(){
    network_checks = network_checks + 1;
    if(network_checks > max_network_checks){
	return;
    }
    console.log("asking for network status");
    $.ajax({url: "http://smartfan.net/network_status",
	    method: "GET",
	    success: parse_test_complete,
	    error: error_func,
	    async: true,
	    dataType: 'json',
	   }
	  );
    if(!finished_test){
	window.setTimeout(wait_for_test_to_complete, 5000);
    }
}
