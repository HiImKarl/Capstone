//scoped variables for this
let curr_selected = [];
let seen = {};
let how_many = {};
let stock_data = {};
let views = {};
let views_map = {};
views_map[-2] = "<select style = 'margin-top: 10px'><option selected = \"selected\" value='-2'>Very Bullish</option><option value='-1'>Bullish</option><option value='0'>Neutral</option><option value='1'>Bearish</option><option value = '2'>Very Bearish </option></select>";
views_map[-1] = "<select style = 'margin-top: 10px'><option value='-2'>Very Bullish</option><option selected = \"selected\" value='-1'>Bullish</option><option  value='0'>Neutral</option><option value='1'>Bearish</option><option value = '2'>Very Bearish </option></select>";
views_map[0] = "<select style = 'margin-top: 10px'><option value='-2'>Very Bullish</option><option value='-1'>Bullish</option><option selected = \"selected\" value='0'>Neutral</option><option value='1'>Bearish</option><option value = '2'>Very Bearish </option></select>";
views_map[1] = "<select style = 'margin-top: 10px'><option value='-2'>Very Bullish</option><option value='-1'>Bullish</option><option value='0'>Neutral</option><option selected = \"selected\" value='1'>Bearish</option><option value = '2'>Very Bearish </option></select>";
views_map[2] = "<select style = 'margin-top: 10px'><option value='-2'>Very Bullish</option><option value='-1'>Bullish</option><option selected = \"selected\" value='0'>Neutral</option><option value='1'>Bearish</option><option value = '2' selected = \"selected\">Very Bearish </option></select>";

// map our views to: -2, -1, 0, -1, -2 views_map and then set the views to POST to server
function change_view(item, view){
    views[item] = parseInt(view);
}

document.onload = on_load(user_id);

function on_load(user_id){
    $.getJSON('/api/assets', function(data) {
        let tickers = data['tickers'];
        let prices = data['prices'];
        for (let i = 0; i < tickers.length; ++i) {
            stock_data[tickers[i]] = {"price": prices[i]};
            views[tickers[i]] = 0;
        }
    }).done(function() {
        let new_tickers = [];
        $.getJSON('/api/portfolios?user_id=' + user_id, function(data){
            let new_amounts = data['amount'];
            new_tickers = data['ticker'];
            for (let i = 0; i < new_amounts.length; i++){
                how_many[new_tickers[i]] = new_amounts[i];
                seen[new_tickers[i]] = '';
                curr_selected.push(new_tickers[i]);
            }
        }).done(function (){
            let to_show = [];
            for (let ticker in how_many){
                if (how_many[ticker] !== 0 ){
                    let views_select = [views_map[views[ticker]].slice(0, 7),' onchange = \"change_view( \''+ ticker + '\', this.options[this.selectedIndex].value)\"', views_map[views[ticker]].slice(7)].join('');
                    to_show.push("<div class = 'stock' ><span class='close' onClick = \"removeStock('"+ticker+"')\">X</span><h2>" + ticker + "</h2> <span style = 'color: green'> $" + stock_data[ticker]["price"] + "</span></br><input type='number' value = '"+ how_many[ticker] + "' placeholder = '# shares' onKeyUp= 'updateAmount(this.value, \""+ticker+"\")'>"+views_select+"</div>" );      
                }
            }

            to_show.sort();
            let argsString = Array.prototype.join.call(to_show, "");
            document.getElementById("portfolio").innerHTML = argsString;
        });
    });
}

// #stock data is our stock-> prices map
function myFunction() {
    document.getElementById("myDropdown").classList.toggle("show");
}

function populate() {
    if (!document.getElementById('myInput').value) {
        document.getElementById("myDropdown").innerHTML = '';
        return;
    }

    let dropdown = "<ul class = 'list-group'>";
    let middle = [];
    for (let ticker in stock_data) {
        if (stock_data.hasOwnProperty(ticker)) {
            if (!seen.hasOwnProperty(ticker)){
                middle.push("<li class = 'list-group list-group-item hover' style = 'width: 90% !important; margin: 0 auto;' onClick = 'addStock(\""+ticker.toString()+"\")'>" + ticker + '</li>');
            }
        }
    }
    
    middle.sort();
    let argsString = dropdown + middle.join('') + '</ul>';
    document.getElementById("myDropdown").innerHTML = argsString;
}

function filterFunction() {
    populate();
    let input, filter, ul, li, a, i;
    input = document.getElementById("myInput");
    filter = input.value.toUpperCase();
    let div = document.getElementById("myDropdown");
    a = div.getElementsByTagName("li");
    for (i = 0; i < a.length; i++) {
        if (a[i].innerHTML.toUpperCase().startsWith(filter)) {
            a[i].style.display = "";
        } else {
            a[i].style.display = "none";
        }
    }
}

function addStock(item) {
    curr_selected.push(item);
    seen[item] = '';
    let to_show = [];
    let views_select = [views_map[0].slice(0, 7),' onchange = \"change_view( \''+ item.toString() + '\', this.options[this.selectedIndex].value)\"', views_map[0].slice(7)].join('');
    for (let i = 0; i < curr_selected.length; i++) {
        if (how_many[curr_selected[i]] == 0) {
            to_show.push("<div class = 'stock' ><span class='close' onClick = \"removeStock('"+curr_selected[i].toString()+"')\">X</span><h2>" + curr_selected[i] + "</h2>$ " + stock_data[curr_selected[i]]["price"] + "</br><input type='number' placeholder = '# shares' onKeyUp= 'updateAmount(this.value, \""+curr_selected[i].toString()+"\")'>"+views_select+"</div>" );    
        } else {
            to_show.push("<div class = 'stock' ><span class='close' onClick = \"removeStock('"+curr_selected[i].toString()+"')\">X</span><h2>" + curr_selected[i] + "</h2>$ " + stock_data[curr_selected[i]]["price"] + "</br><input type='number' value = '"+ how_many[curr_selected[i]] + "' placeholder = '# shares' onKeyUp= 'updateAmount(this.value, \""+curr_selected[i].toString()+"\")'>"+views_select+"</div>" );
        }
    }

    to_show.sort();
    let argsString = Array.prototype.join.call(to_show, "");
    document.getElementById("portfolio").innerHTML = argsString;
    filterFunction();
}

function removeStock(item){
    let idx = curr_selected.indexOf(item);
    curr_selected.splice(idx, 1);
    delete seen[item];
    how_many[item] = 0;
    let to_show = [];
    let views_select = [views_map[0].slice(0, 7),' onchange = \"change_view( \''+ item.toString() + '\', this.options[this.selectedIndex].value)\"', views_map[0].slice(7)].join('');
    for (let i = 0; i < curr_selected.length; i++){
        if (how_many[curr_selected[i]] == 0 ){
            to_show.push("<div class = 'stock' ><span class='close' onClick = \"removeStock('"+curr_selected[i].toString()+"')\">X</span><h2>" + curr_selected[i] + "</h2>$" + stock_data[curr_selected[i]]["price"] + "</br><input type='number' placeholder = '# shares' onKeyUp= 'updateAmount(this.value, \""+curr_selected[i].toString()+"\")'>"+views_select+"</div>" );
        } else {
            to_show.push("<div class = 'stock' ><span class='close' onClick = \"removeStock('"+curr_selected[i].toString()+"')\">X</span><h2>" + curr_selected[i] + "</h2>$" + stock_data[curr_selected[i]]["price"] + "</br><input type='number' value = '"+ how_many[curr_selected[i]] + "' placeholder = '# shares' onKeyUp= 'updateAmount(this.value, \""+curr_selected[i].toString()+"\")'>"+views_select+"</div>" );
        }
    }
    to_show.sort();
    let argsString = Array.prototype.join.call(to_show, "");
    document.getElementById("portfolio").innerHTML = argsString;
    filterFunction();
}

function updateAmount(value, ticker){
    how_many[ticker] = parseFloat(value);
}

function reset() {
    seen = {};
    curr_selected = [];
    for (let ticker in how_many){
        how_many[ticker] = 0;
    }
    document.getElementById("portfolio").innerHTML = '';
    document.getElementById("myDropdown").innerHTML = '';
    submit();
}

function submit() {
    let post_data = {
        'how_many': how_many,
        'views': views
    };
    $.ajax("/set_portfolio", {
        data: JSON.stringify(post_data),
        contentType: 'application/json',
        type: 'post',
        dataType: 'json',
        async: true,
    }).done();
}

