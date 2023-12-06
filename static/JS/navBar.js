document.addEventListener("DOMContentLoaded", getDetails())
document.getElementById("logoText").addEventListener("click", function() {
    user = window.location.pathname.split("/").pop();
    newRoute = "/home/" + user;
    window.location = newRoute;
});
document.getElementById("navbar-logo").addEventListener("click", function() {
    user = window.location.pathname.split("/").pop();
    newRoute = "/home/" + user;
    window.location = newRoute;
}); //links navbar logo back to home; keeps user signed in.
document.getElementById("accountDetails").addEventListener("click", function() {
    user = window.location.pathname.split("/").pop();
    if (CheckGuest()==false){
        newRoute = "/accountDetails/" + user;
        window.location = newRoute;
    }
})
document.getElementById("moodChecker").addEventListener("click", function() {
    user = window.location.pathname.split("/").pop();
    newRoute = "/moodChecker/" + user;
    window.location = newRoute;
})

function getDetails() {
// Fills in the details in the HTML page with database info
    user = window.location.pathname.split("/").pop()
    newRoute = "/updateInfo/" + user
    var xhttp = new XMLHttpRequest();
    xhttp.open("GET",newRoute,true);
    xhttp.setRequestHeader("Content-type","application/x-www-form-urlencoded");
    xhttp.onreadystatechange = function() {
        if (xhttp.readyState === 4) {
            if (xhttp.status === 200) {
                var text = xhttp.responseText;
                if (text === "None") {
                    document.getElementById("userDisplay").innerHTML = "";
                } else {
                    jsonTuple = JSON.parse(text);
                    let userDetails = jsonTuple[0] + " " + jsonTuple[1];
                    document.getElementById("accountDetails").innerHTML = userDetails;
                    let mood = jsonTuple[3];
                    document.getElementById("moodChecker").innerHTML = mood;
                }
            } else {
                console.error(xhttp.statusText);
            }
        }
    };
    xhttp.send();
}

function CheckGuest(){
    user = window.location.pathname.split("/").pop()
    newRoute = "/checkGuest/" + user;
    var xhttp = new XMLHttpRequest();
    xhttp.open("GET",newRoute,true);
    xhttp.setRequestHeader("Content-type","application/x-www-form-urlencoded");
    xhttp.onreadystatechange = function() {
        if (xhttp.readyState === 4) {
            if (xhttp.status === 200) {
                var text = xhttp.responseText;
                console.log(text)
                if (text == "T"){
                    return true;
                }
                else{
                    return false;
                }
            } else {
                console.error(xhttp.statusText);
            }
        }
    };
    xhttp.send();
}