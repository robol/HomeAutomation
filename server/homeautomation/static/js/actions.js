function setStatus(client_name, message) {
    el = document.getElementById("statusBox-" + client_name);
    el.innerHTML = message;
}

function triggerAction(client_name, action) {    
    setStatus(client_name, "Performing action: " + action + " ... ");

    // Obtain the parameters, if any
    params = {};
    inputs = $("input[id^=parameter-" + action);
    $(inputs).each(function (i, field) {
	parameter_data = field.id.split("-");
	pname = parameter_data[2];
	ptype = parameter_data[3];

	if (field.value != "") {
	    if (ptype == "string") {
		params[pname] = field.value;
	    }
	    else if (ptype == "integer") {
		params[pname] = parseInt(field.value);
	    }
	}
    });

    console.log(params);
    
    $.ajax('/client/' + client_name + '/action/' + action, {
	success: function (data) {
	    setStatus(client_name, data["status"])
	},
	dataType: 'json',
	method: "POST",
	data: JSON.stringify(params),
	contentType: 'application/json'
    });
}

function loadStatus(client_name) {
    setStatus(client_name, "Loading status ... ");
    
    $.ajax('/client/' + client_name + '/status', {
	dataType: 'json',
	success: function (data) {
	    setStatus(client_name, data["status"]);
	}
    });
}

function loadShortStatus(client_name) {
    setStatus(client_name, "loading status ... ");
    
    $.ajax('/client/' + client_name + '/status', {
	dataType: 'json',
	success: function (data) {
	    setStatus(client_name, data["status"]);
	}
    });

}
