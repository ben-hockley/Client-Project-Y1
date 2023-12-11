document.addEventListener("DOMContentLoaded", getDetails())
document.getElementById("navbar-logo").addEventListener("click", function() {
    user = window.location.pathname.split("/").pop();
    newRoute = "/home/" + user;
    window.location = newRoute;
}); //links navbar logo back to home; keeps user signed in.
document.getElementById("account-details").addEventListener("click", function() {
    user = window.location.pathname.split("/").pop();
    var text="";
    newRoute = "/checkGuest/" + user;
    var xhttp = new XMLHttpRequest();
    xhttp.open("GET",newRoute,true);
    xhttp.setRequestHeader("Content-type","application/x-www-form-urlencoded");
    xhttp.onreadystatechange = function() {
        if (xhttp.readyState === 4) {
            if (xhttp.status === 200) {
                text = String(xhttp.responseText);
                if (text=="F"){
                    newRoute = "/accountDetails/" + user;
                    window.location = newRoute;
                }
            }
        }
    };
    xhttp.send();

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
                    document.getElementById("user-display").innerHTML = "";
                } else {
                    jsonTuple = JSON.parse(text);
                    let userDetails = jsonTuple[0] + " " + jsonTuple[1];
                    document.getElementById("displayUser").innerHTML = userDetails;
                    let mood = jsonTuple[3];
                    document.getElementById("displayMood").innerHTML = mood;
                }
            } else {
                console.error(xhttp.statusText);
            }
        }
    };
    xhttp.send();
}
// Event Listener to take you to the Create Quiz page throught the NavBar
document.getElementById("create-quiz").addEventListener('click', function() {
    user = window.location.pathname.split("/").pop();
    newRoute = "/createQuiz/" + user;
    window.location = newRoute;
})
// Event Listener to take you to the Avalible Quizzes page throught the NavBar
document.getElementById("available-quizzes").addEventListener('click', function() {
    user = window.location.pathname.split("/").pop();
    newRoute = "/displayQuizzes/" + user;
    window.location = newRoute;
})

