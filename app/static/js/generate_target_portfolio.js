var portfolio_data;

$(window).on('load', function(){
    let field = document.getElementById("exampleFormControlSelect1");
    let res = '';
    for (let i = 1; i <= 40; i++){
        if (i != 5){
            res += '<option>'+i.toString()+'</option>';
        }
        else{
            res += '<option selected = \'selected\'>'+i.toString()+'</option>';
        }
    };
    field.innerHTML = res;
});

function getRandomColor() {
    var letters = '0123456789ABCDEF';
    var color = '#';
    for (var i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
}

function card(title, info, description){
    return (
"<div class=\"card bg-light mb-3\" style=\"max-width: 18rem; display: inline-block;\"><div class=\"card-header\">"+title+"</div><div class=\"card-body\"><h5 class=\"card-title\">"+info+"</h5><p class=\"card-text\">"+description+"</p></div></div>"
    );
}

function generate_portfolio(){
    console.log('generating');
    var return_value = parseFloat(document.getElementById("myPercent").value)/100;
    var assets = parseFloat(document.getElementById("exampleFormControlSelect1").value);
    $.getJSON('/api/mvo?cardinality=' + assets.toString() + '&mu_goal=' + return_value.toString(), function(data) {
        portfolio_data = data;
    }).done(function() {
        var doc = document.getElementById("replace");
        doc.innerHTML = "<div class  = \"card-header bg-light\" style = \"height: 15px !important\"></div><h3 style = \"margin-top: 20px;\"class=\"card-title\">Generated Portfolio of Assets</h3><div style = \"display: flex !important;justify-content: center; box-shadow: 0 !important;margin-bottom: 15px !important; padding: 20px 0;\"><ul id = \"lol\" class = \"card bg-light mb-3 list-group\" style=\"margin-left: 10%; display: inline; width:40%; height:390px; overflow:hidden; overflow-y: scroll; text-align: left; border: 1px solid gray\"></ul><div style = \"width: 55%; height = 55%;\"><canvas id=\"doughnut-chart\" style = \"width:100% !important; height: 100% !important; margin-right: 0 !important;\" h></canvas></div></div><div id = 'stats' style = 'display: block; align-items: center'></div><div class=\"card-footer text-muted\"></div</div>"
        
        let arr = ["<div class=\"card-header\">Ticker in Portfolio: Number of Asset</div>"];
        for (let i = 0; i < portfolio_data['portfolio'].length; i++){
            arr.push("<li class=\"list-group-item\">"+ portfolio_data['tickers'][i].toString() + " (amount: " + portfolio_data['portfolio'][i].toString()+")</li>" );
        };

        var args_String = arr.join('');
        document.getElementById('lol').innerHTML = args_String;
        doc.style = "padding: 20px 0 !important; margin-bottom: 0;"
        let stats = [];
        for (header in portfolio_data){
            console.log(header);
            switch (header){
                case "ret":
                    stats.push(card("Average Weekly Return of Portfolio", (portfolio_data[header]*100).toString() + "%", "The higher, the better. This tells you how much your portfolio is increasing/decreasing every week."));
                    continue;
                case "sigma":
                    console.log('wtf');
                    stats.push(card("Sigma of Portfolio", portfolio_data[header] + "%", "The standard deviation of this Portfolio. The higher, the more risky and unpredictable the portfolio."));
                    continue;
                default:
                    continue;
            }
        }
        document.getElementById('stats').innerHTML = stats.join('');
        doc.style = "width: 70%; margin: 0 auto; padding: 20px 0; "
        var colors = ["#3e95cd", "#8e5ea2","#3cba9f","#e8c3b9","#c45850"];
        for (let i = 5; i < arr.length; i++){
            colors.push(getRandomColor());
        }
        new Chart(document.getElementById("doughnut-chart"), {
            type: 'doughnut',
            data: {
            labels: portfolio_data['tickers'],
            datasets: [
                {
                label: "Value $(USD)",
                backgroundColor: colors.slice(0, portfolio_data['tickers'].length),
                data: portfolio_data['portfolio']
                }
            ]
            },
            options: {
                responsive: false,
                title: {
                    display: true,
                    text: 'Distribution of Assets in your Portfolio'
                },
                legend: {
                    display: true,
                    labels: {
                        fontSize: 8,
                        boxWidth: 20
                    }
                }
            }
        });
    })
};
