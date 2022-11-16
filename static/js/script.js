
var button = document.getElementById("btn")

// first event triggered is fade out
button.addEventListener("click",
    function(){fadeout();})

function fadeout() {
    button.style.animation = "fade-out 0.2s forwards";}

button.addEventListener("click",
    function(){setTimeout(function(){clickBehavior()}, 150);})

function clickBehavior() {
    window.location='/jado';}


// function put_object(obj) {
//     // obj is a Proxy
//     var activity = obj.get("a");
//     document.getElementById("activity").innerHTML = activity;
//     }