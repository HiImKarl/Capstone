
var curr_selected = [];
var seen = {};
var how_many = {};
var stock_data = {};

$.getJSON('/api/assets', function(data) {
    let tickers = data['tickers'];
    let prices = data['prices'];
    for (let i = 0; i < tickers.length; ++i) {
        stock_data[tickers[i]] = {"price": prices[i]}
        how_many[tickers[i]] = 0;
    };
});

// #stock data is our stock-> prices map
function myFunction() {
    document.getElementById("myDropdown").classList.toggle("show");
}

function populate() {
    if (!document.getElementById('myInput').value){
        document.getElementById("myDropdown").innerHTML = '';
        return
    };

    dropdown = "<ul class = 'list-group'>";
    var middle = [];
    for (var ticker in stock_data) {
        if (stock_data.hasOwnProperty(ticker)) {
            if (!seen.hasOwnProperty(ticker)){
                middle.push("<li class = 'list-group list-group-item hover' onClick = 'addStock(\""+ticker.toString()+"\")'>" + ticker + '</li>');
            }
        }
    }
    
    middle.sort()
    argsString = dropdown + middle.join('') + '</ul>';
    document.getElementById("myDropdown").innerHTML =argsString;
};

function filterFunction() {
    populate();
    var input, filter, ul, li, a, i;
    input = document.getElementById("myInput");
    filter = input.value.toUpperCase();
    div = document.getElementById("myDropdown");
    a = div.getElementsByTagName("li");
    for (i = 0; i < a.length; i++) {
        if (a[i].innerHTML.toUpperCase().indexOf(filter) > -1) {
            a[i].style.display = "";
        } else {
            a[i].style.display = "none";
        }
    }
}

function addStock(item) {
    curr_selected.push(item);
    seen[item] = '';
    var to_show = []
    for (var i = 0; i < curr_selected.length; i++){
        if (how_many[curr_selected[i]] == 0 ){
            to_show.push("<div class = 'stock' ><span class='close' onClick = \"removeStock('"+curr_selected[i].toString()+"')\">X</span><h2>" + curr_selected[i] + "</h2>$ " + stock_data[curr_selected[i]]["price"] + "</br><input type='number' placeholder = '# shares' onKeyUp= 'updateAmount(this.value, \""+curr_selected[i].toString()+"\")'></div>" );    
        } else {
            to_show.push("<div class = 'stock' ><span class='close' onClick = \"removeStock('"+curr_selected[i].toString()+"')\">X</span><h2>" + curr_selected[i] + "</h2>$ " + stock_data[curr_selected[i]]["price"] + "</br><input type='number' value = '"+ how_many[curr_selected[i]] + "' placeholder = '# shares' onKeyUp= 'updateAmount(this.value, \""+curr_selected[i].toString()+"\")'></div>" );
        }
    };
    to_show.sort();
    var argsString = Array.prototype.join.call(to_show, "");
    document.getElementById("portfolio").innerHTML = argsString;
    filterFunction();
}

function removeStock(item){
    var idx = curr_selected.indexOf(item);
    curr_selected.splice(idx, 1);
    delete seen[item];
    how_many[item] = 0;
    var to_show = []
    for (var i = 0; i < curr_selected.length; i++){
        if (how_many[curr_selected[i]] == 0 ){
            to_show.push("<div class = 'stock' ><span class='close' onClick = \"removeStock('"+curr_selected[i].toString()+"')\">X</span><h2>" + curr_selected[i] + "</h2>$" + stock_data[curr_selected[i]]["price"] + "</br><input type='number' placeholder = '# shares' onKeyUp= 'updateAmount(this.value, \""+curr_selected[i].toString()+"\")'></div>" );
        } else {
            to_show.push("<div class = 'stock' ><span class='close' onClick = \"removeStock('"+curr_selected[i].toString()+"')\">X</span><h2>" + curr_selected[i] + "</h2>$" + stock_data[curr_selected[i]]["price"] + "</br><input type='number' value = '"+ how_many[curr_selected[i]] + "' placeholder = '# shares' onKeyUp= 'updateAmount(this.value, \""+curr_selected[i].toString()+"\")'></div>" );
        }
    }
    to_show.sort();
    var argsString = Array.prototype.join.call(to_show, "");
    document.getElementById("portfolio").innerHTML = argsString;
    filterFunction();
};

function updateAmount(value, ticker){
    how_many[ticker] = parseFloat(value);
}

function reset(){
    if (confirm('Are you sure you want to reset your current Portfolio?')) {
        seen = {};
        curr_selected = [];
        for (ticker in how_many){
            how_many[ticker] = 0;
        }
        document.getElementById("portfolio").innerHTML = '';
        document.getElementById("myDropdown").innerHTML = '';
    } else {
        pass
    }
}

function submit() {
    $.ajax("/set_portfolio", {
        data: JSON.stringify(how_many),
        contentType: 'application/json',
        type: 'post',
        dataType: 'json',
        async: true,
    });
}

