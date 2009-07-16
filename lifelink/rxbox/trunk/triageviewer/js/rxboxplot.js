$(document).ready(function() {
    arr = previous = ecg = new Array();
    var alldata = [ { data: ecg } ];
    var options = {
                lines: { show: true, fill: false, fillColor: "rgba(255, 255, 255, 0.8)", lineWidth: 1 },
                points: { show: false },
                shadowSize: 0,
                grid: {
                        borderWidth: 1,
                        color: "rgba(255,0,0, 0.5)",
                        tickColor: "rgba(255,0,0, 0.5)",
                },
                xaxis: {
                        min: 0,
                        max: 10,
                        tickSize: 0.2,
                        minTickSize: 0.2
                },
                yaxis: {
                        min: -2,
                        max: 2,
                        tickSize: 0.2,
                        minTickSize: 0.2
                },
                colors:  [ "#000000"]

        };

    plot = $.plot($("#placeholder"), alldata, options);

        var fetchtimer = setInterval(function() {
        	$.get("getdata.php", { session: "sessionxyz", time: "2pm" },
                	function(data){
                                ecg = data[0];
                        }, "json");

                var i = 0;
                arr = [];
	        var plottimer = setInterval(function(){
                	var nullarr = [null, null, null, null, null, null];
	        	arr = arr.concat(ecg.slice(i,i+19));

                        plot.setData([ { data: arr.concat(nullarr, previous.slice(i+20, previous.length)) } ]);
                        plot.draw();

                        i+=20;
                        if(i >= ecg.length) {
                               	previous = arr.slice();
                               	clearInterval(plottimer);
                        }
        	},1);
	}, 10000);
});

