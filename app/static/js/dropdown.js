
var curr_selected = [];
var stock_data = {};
var seen = {};
var how_many = {};

// #stock data is our stock-> prices map
function myFunction() {
    document.getElementById("myDropdown").classList.toggle("show");
}

function populate() {
    if (!document.getElementById('myInput').value){
        document.getElementById("myDropdown").innerHTML = '';
        return
    };

    dropdown = '';
    dropdown += "<ul class = 'list-group'>";
    for (var ticker in stock_data) {
        if (stock_data.hasOwnProperty(ticker)) {

            if (!seen.hasOwnProperty(ticker)){
                dropdown += "<li class = 'list-group list-group-item hover' onClick = 'addStock(\""+ticker.toString()+"\")'>" + ticker + '</li>';
            }
        }
    }
    
    dropdown += '</ul>';
    var argsString = Array.prototype.join.call(dropdown, "");

    document.getElementById("myDropdown").innerHTML = argsString;
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
        to_show.push("<div class = 'stock' ><span class='close' onClick = \"removeStock('"+curr_selected[i].toString()+"')\">X</span><h2>" + curr_selected[i] + "</h2>$ " + stock_data[curr_selected[i]]["price"] + "</br><input type='text' placeholder = '# shares' onKeyUp= 'updateAmount(this, \""+curr_selected[i].toString()+"\")'></div>" );    
    };

    var argsString = Array.prototype.join.call(to_show, "");
    document.getElementById("portfolio").innerHTML = argsString;
    filterFunction();
}

function removeStock(item){
    var idx = curr_selected.indexOf(item);
    curr_selected.splice(idx, 1);
    delete seen[item];
    var to_show = []
    for (var i = 0; i < curr_selected.length; i++){
        to_show.push("<div class = 'stock' ><span class='close' onClick = \"removeStock('"+curr_selected[i].toString()+"')\">X</span><h2>" + curr_selected[i] + "</h2>$" + stock_data[curr_selected[i]]["price"] + "</br><input type='text' placeholder = '# shares' onKeyUp= 'updateAmount(this, \""+curr_selected[i].toString()+"\")'></div>" );
    }
    var argsString = Array.prototype.join.call(to_show, "");
    document.getElementById("portfolio").innerHTML = argsString;
    filterFunction();
};

function reset(){
    if (confirm('Are you sure you want to rest your current Portfolio?')) {
        seen = {};
        curr_selected = [];
        document.getElementById("portfolio").innerHTML = '';
        document.getElementById("myDropdown").innerHTML = '';
    } else {
        pass
    }
};

function submit(){
    alert("Successfully submitted and saved portfolio!");
}