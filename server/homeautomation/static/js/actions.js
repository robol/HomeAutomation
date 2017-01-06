function setStatus(client_name, message) {
    el = document.getElementById("statusBox-" + client_name);
    el.innerHTML = message;
}

function triggerAction(client_name, action) {    
    setStatus(client_name, "Performing action: " + action + " ... ");
    
    $.ajax('/client/' + client_name + '/action/' + action, {
	success: function (data) {
	    loadStatus(client_name);
	}
    });
}

function loadStatus(client_name) {
    setStatus(client_name, "Loading status ... ");
    
    $.ajax('/client/' + client_name + '/status', {
	dataType: 'json',
	success: function (data) {
	    html = "<ul>";
	    
	    $(Object.keys(data)).each (function (i, el) {
		html += "<li><strong>" + el + "</strong>: " + data[el] + "</li>";
	    });

	    html += "</ul>";
	    setStatus(client_name, html);	 
	}
    });
}

function loadShortStatus(client_name) {
    setStatus(client_name, "loading status ... ");
    
    $.ajax('/client/' + client_name + '/status', {
	dataType: 'json',
	success: function (data) {
	    fields = [];
	    
	    $(Object.keys(data)).each (function (i, el) {
		if (el != "description") {
		    fields.push(el + ": " + data[el]);
		}			
	    });

	    setStatus(client_name, fields.join(", "));	 
	}
    });

}
