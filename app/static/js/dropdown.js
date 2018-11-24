
var dropdown = [];
var seen = {};
var curritems = [];
var currList = []

function myFunction() {
    document.getElementById("myDropdown").classList.toggle("show");
}

function populate(items) {
    if (!document.getElementById('myInput').value){
        document.getElementById("myDropdown").innerHTML = '';
        return
    };
    curritems = items;
    dropdown = '';
    dropdown += "<ul class = 'list-group'>";
    items.sort();
    items.forEach(function(item){
        if (!seen.hasOwnProperty(item)){
            dropdown += "<li class = 'list-group list-group-item hover' onClick = \"addStock('"+item.toString()+"')\">" + item + '</li>';
        }
    });
    dropdown += '</ul>';
    var argsString = Array.prototype.join.call(dropdown, "");
    document.getElementById("myDropdown").innerHTML = argsString;
};

function filterFunction(items) {
    populate(items);
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
    var hello = "<div class = 'stock' ><span class='delete'>×</span><h2>" + item + "</h2><h1> '...' </h1><h3> % </h3></div>";
    currList += hello;
    seen[item] = '';
    var argsString = Array.prototype.join.call(currList, "");
    document.getElementById("portfolio").innerHTML = argsString;
    populate(curritems);
}

function removeStock(item){

};