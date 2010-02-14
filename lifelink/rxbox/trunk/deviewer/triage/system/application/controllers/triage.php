<?php
    class Triage extends Controller {
        function Triage()
        {
            parent::Controller();
        }
        function index()
        {
            $data['title'] = "Domain Expert's Window";
            $data['extraHeadContent'] =
                array(
                    '<script type="text/javascript" src="' . base_url() . 'public/js/flot/jquery.js"></script>',
                    '<script type="text/javascript" src="' . base_url() . 'public/js/flot/jquery.flot.js"></script>',
                    '<script type="text/javascript" src="' . base_url() . 'public/js/rxboxplotstat.js"></script>',
                    '<link rel="stylesheet" type="text/css" href="' . base_url() . 'public/css/triageviewer.css"></link>'
                 );
            $this->load->view('triage/deview', $data);
        }
        function session($q='')
        {
            $data['title'] = "Domain Expert's Window";
            $data['extraHeadContent'] =
                array(
                    '<script type="text/javascript" src="' . base_url() . 'public/js/flot/jquery.js"></script>',
                    '<script type="text/javascript" src="' . base_url() . 'public/js/flot/jquery.flot.js"></script>',
                    '<link rel="stylesheet" type="text/css" href="' . base_url() . 'public/css/triageviewer.css"></link>',
                    '<script type="text/javascript">
$(document).ready(function() {
    arr = previous = ecg = new Array();
    var alldata = [ { data: ecg } ];
    var options = { lines: { show: true, fill: false, fillColor: "rgba(255, 255, 255, 0.8)", lineWidth: 1 },
                    points: { show: false },
                    shadowSize: 0,
                    grid: {
                            borderWidth: 1,
                            color: "rgba(255,0,0, 0.5)",
                            tickColor: "rgba(255,0,0, 0.5)",
                          },
                    xaxis: {
                            min: 0,
                            max: 500,
                            tickSize: 100,
                            minTickSize: 0.2
                    },
                    yaxis: {
                            min: -1,
                            max: 2,
                            tickSize: 0.2,
                            minTickSize: 0.1
                    },
                    colors: [ "#000000"]
                  };
    
    $.getJSON("' . base_url() . 'public/edf_data.php", { q: "' . $q . '"},
            function(data){ ecg = data; }
    );

    alldata = [{ data: ecg }]
    plot = $.plot($("#placeholder"), alldata, options);
});
</script>'
                 );
            $this->load->view('triage/deview', $data);
        }
    }
        
?>
