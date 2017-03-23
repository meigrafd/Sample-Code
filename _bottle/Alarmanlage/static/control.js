if (typeof(String.prototype.strip) === "undefined") {
    String.prototype.strip = function() {
        return String(this).replace(/^\s+|\s+$/g, '');
    };
}

function isset(strVariableName) { 
    try { 
        eval( strVariableName );
    } catch( err ) { 
        if ( err instanceof ReferenceError ) 
            return false;
    }
    return true;
}

function sleep(millis, callback) {
    setTimeout(function() { callback(); } , millis);
}

//source of: http://www.html5tutorial.info/html5-range.php
function printValue(sliderID, textbox) {
    var x = document.getElementById(textbox);
    var y = document.getElementById(sliderID);
    x.value = y.value;
}

//----------------------------------------------------------------


var telemetryTimer;
$(document).ready(function() {
    // start Main Timers
    telemetryTimer = setTimeout(get_telemetry, 1000);
});


function get_telemetry() {
    $.getJSON("/data/")
    .fail(function() {
        console.log("Error processing get_telemetry");
        clearTimeout(telemetryTimer);
    })
    .done(function(data) {
        $.each(data, function(id,val) {
            if (document.getElementById(id) !== null) {
            
                if (id == "ARMED") {
                    document.getElementById(id).innerHTML = val;
                } else if (id == "MOTION") {
                    document.getElementById(id).value = val;
                
                } else {
                    document.getElementById(id).innerHTML = val;
                }
            
            }
        })
        telemetryTimer = setTimeout(get_telemetry, 2000);
    });
}
