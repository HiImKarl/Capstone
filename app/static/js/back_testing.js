$(function() {
    $('input[name="daterange"]').daterangepicker({
        "alwaysShowCalendars": true,
        "autoUpdateInput": false,
        "opens": "center",
        "locale": {
            "cancelLabel": 'Clear'
        }
    }),
    $('input[name="daterange"]').on('apply.daterangepicker', function(ev, picker) {
        $(this).val(picker.startDate.format('MM/DD/YYYY') + ' - ' + picker.endDate.format('MM/DD/YYYY'));
    });
  
    $('input[name="daterange"]').on('cancel.daterangepicker', function(ev, picker) {
        $(this).val('');
    });
});

function backtest(){

    if (confirm("Are you sure you want to backtest?")){
        var ctx = document.getElementById("myChart");
        var msft = [109.57, 106.87, 106.94, 104.97, 107.28, 108.29, 104.62, 101.71, 103.11, 103.07];
        var fb = [144.96, 141.15, 142.16, 144.22, 143.85, 139.53, 131.55, 132.43, 134.82, 131.72];
        var twtr = [34.08, 32.01, 32.49, 32.91, 33.15, 33.67, 31.98, 31.06, 31.61, 31.21];
        var nvda = [205.67, 189.54, 199.31, 197.19, 202.39, 164.39, 144.7, 149.08, 144.71, 145];
        ctx.style.backgroundColor = 'white';
        function sumArray(a, b) {
            var c = [];
            for (var i = 0; i < Math.max(a.length, b.length); i++) {
              c.push((a[i] || 0) + (b[i] || 0));
            }
            return c;
        }
        var portfolio = [];
        for (var i = 0; i < msft.length; i++){
            portfolio.push(msft[i]+fb[i]+twtr[i]+nvda[i]);
        };
        var myChart = new Chart(ctx, {
            type: 'line',
            data: {
              labels: ['11/10/2018', '11/12/2018', '11/13/2018', '11/14/2018', '11/15/2018', '11/16/2018', '11/17/2018', '11/18/2018', '11/19/2018', '11/20/2018'],
              datasets: [{ 
                  data: msft,
                  label: "MSFT",
                  borderColor: "#3e95cd",
                  fill: false
                }, { 
                  data:fb,
                  label: "FB",
                  borderColor: "#8e5ea2",
                  fill: false
                }, { 
                  data: twtr,
                  label: "TWTR",
                  borderColor: "#3cba9f",
                  fill: false
                }, { 
                  data: nvda,
                  label: "NVDA",
                  borderColor: "#e8c3b9",
                  fill: false
                }, { 
                  data: portfolio,
                  label: "Portfolio",
                  borderColor: "#c45850",
                  fill: false
                }
              ]
            },
            options: {
                defaultFontSize: 14,
                scales: {
                    yAxes: [{
                      scaleLabel: {
                        display: true,
                        labelString: 'Date',
                        fontSize: 16
                      }
                    }],
                    xAxes: [{
                        scaleLabel: {
                          display: true,
                          labelString: 'Value in $(USD)',
                          fontSize: 16
                        }
                      }]
                  },
              title: {
                display: true,
                text: 'Value over time of Portfolio and individual Assets',
                fontSize: 16
              }
            }
          });
    } else{
        pass
    };
};