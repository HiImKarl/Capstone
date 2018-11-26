var stock_data = {}
function on_load(user_id){
    console.log('loaded');
    $.getJSON('/api/portfolios?user_id' + user_id, function(data){
        let amounts = data['amount'];
        let tickers = data['ticker'];
        for (let i = 0; i < amounts.length; i++){
            stock_data[tickers[i]] = amounts[i];
        }
    });

    let list = [];
    for (ticker in stock_data){
        list.push("<li class = 'list-item'>"+ ticker + " (amount: " + stock_data[ticker]+")"+"</li>" )
    };
    console.log(list);
    let argsString = list.join('');
    let ul = document.getElementById('toadd');
    ul.innerHTML = argsString;

}
