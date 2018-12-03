var portfolio_data;
var stock_prices = {};
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
    "<div data-toggle='tooltip' title = '"+description+"' class=\"card bg-light mb-3\" style=\"max-width: 18rem; display: inline-block;\"><div class=\"card-header\">"+title+"</div><div class=\"card-body\"><h5 class=\"card-title\">"+info+"</h5><p class=\"card-text\"></p></div></div>"
    );
}

function generate_portfolio(){
    var return_value = parseFloat(document.getElementById("myPercent").value)/100;
    var assets = parseFloat(document.getElementById("exampleFormControlSelect1").value);
    let prices;
    $.getJSON('/api/assets', function(data) {
        let tickers = data['tickers'];
        prices = data['prices'];
        for (let i = 0; i < tickers.length; ++i) {
            stock_prices[tickers[i]] = prices[i];
        }
        })
    .done(function(){
    $.getJSON('/api/mvo?cardinality=' + assets.toString() + '&mu_goal=' + return_value.toString(), function(data) {
        portfolio_data = data;
    }).done(function() {
        var doc = document.getElementById("replace");
        doc.innerHTML = "<div class  = \"card-header bg-light\" style = \"height: 15px !important\"></div><h2 style = \"margin-top: 20px;\"class=\"card-title\">Generated Portfolio of Assets</h2><div style = \"display: flex !important;justify-content: center; box-shadow: 0 !important;margin-bottom: 15px !important; padding: 20px 0;\"><ul id = \"lol\" class = \"card bg-light mb-3 list-group\" style=\"margin-left: 10%; display: inline; width:40%; height:390px; overflow:hidden; overflow-y: scroll; text-align: left; border: 1px solid gray\"></ul><div style = \"width: 55%; height = 55%;\"><canvas id=\"doughnut-chart\" style = \"width:100% !important; height: 100% !important; margin-right: 0 !important;\" h></canvas></div></div><h2>Your Portfolio Stats</h2><div id = 'stats' style = 'display: block; align-items: center'></div><div class=\"card-footer text-muted\"></div</div>"
        
        let arr = ["<div class=\"card-header\">Ticker [Number of stock] (Asset Value $USD per stock)</div>"];
        for (let i = 0; i < portfolio_data['portfolio'].length; i++){
            
            let ticker = portfolio_data['tickers'][i];
            let amount = portfolio_data['portfolio'][i];
            arr.push("<li class=\"list-group-item\">"+ ticker + " [amount: " + amount+"] ($"+ (stock_prices[ticker]).toString()+")</li>" );
        };

        var args_String = arr.join('');
        document.getElementById('lol').innerHTML = args_String;
        doc.style = "padding: 20px 0 !important; margin-bottom: 0;"
        let stats = [];

        for (header in portfolio_data){
            switch (header){
                case "ret":
                    stats.push(card("Average Yearly Return of Portfolio", (portfolio_data[header]*100).toString() + "%", "The higher, the better. This tells you how much your portfolio is increasing in value every year."));
                    continue;
                case "sigma":
                    stats.push(card("Sigma of Portfolio", portfolio_data[header] + "%", "The standard deviation of this Portfolio. This is a rough average of how much you can deviate from the average return. The higher, the more risky and unpredictable the portfolio."));
                    continue;
                case "cvar":
                    stats.push(card("CVaR", (portfolio_data[header]).toString() + "%", "You have a 1% probability of losing this portion of your portfolio on average. The lower, the better."));
                    continue;
                case "sharpe_ratio":
                    stats.push(card("Sharpe Ratio", (portfolio_data[header]).toString(), "A measure that indicates the risk-adjusted rate of return. The higher the better"));
                    continue;
                case "var":
                    stats.push(card("VaR", (portfolio_data[header]).toString() + "%", "You have a 1% probability of losing at least this portion of your portfolio. The lower, the better."));
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
        labels = [];
        for (let i = 0; i < portfolio_data['tickers'].length; i++){
            if (portfolio_data['portfolio'][i]>0){
                labels.push(portfolio_data['tickers'][i]);
            } else {
                labels.push('['+portfolio_data['tickers'][i]+']');
            }
        }
        for (let i = 0; i < portfolio_data['portfolio'].length; i++){
            portfolio_data['portfolio'][i] *= stock_prices[portfolio_data['tickers'][i]];
        }
        new Chart(document.getElementById("doughnut-chart"), {
            type: 'doughnut',
            data: {
            labels: labels,
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
})
};
