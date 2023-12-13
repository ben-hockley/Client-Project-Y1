// Completing an AJAX request on page load
document.addEventListener("DOMContentLoaded", getDetails())
// Setting event listeners for each variable
document.getElementById("firstNameData").addEventListener("click", editFirstName);
document.getElementById("lastNameData").addEventListener("click", editLastName);
document.getElementById("usernameData").addEventListener("click", editUsername);

function editFirstName() {
    // Executes when the first name is clicked, creating a new form
    if(document.getElementById("firstForm")) {
        console.log("Form already open")
    }
    else {
    user = window.location.pathname.split("/").pop()
    newRoute = "/updateFirstname/" + user
    const labelForm = document.createElement("label")
    labelForm.innerHTML = "Enter new first name:";
    labelForm.setAttribute("for","newFirstname");
    const firstForm = document.createElement("form");
    const newFirst = document.createElement("input");
    const button = document.createElement("button");
    firstForm.id = "firstForm";
    newFirst.setAttribute("type","text");
    newFirst.id = "newFirstname";
    newFirst.setAttribute("name","newFirstname")
    button.setAttribute("type","submit");
    button.setAttribute("class","btn btn-success")
    button.innerHTML = "Change first name";
    firstForm.appendChild(labelForm);
    firstForm.appendChild(newFirst);
    firstForm.appendChild(button);
    document.getElementById("firstNameData").appendChild(firstForm);
    document.getElementById("firstForm").setAttribute("action",newRoute)
    document.getElementById("firstForm").setAttribute("method","post")
    }
}

function editUsername() {
    // Executes when the username is clicked, creating a new form
    if(document.getElementById("userForm")) {
        console.log("Form already open")
    }
    else {
    user = window.location.pathname.split("/").pop()
    newRoute = "/updateUsername/" + user
    const labelForm = document.createElement("label")
    labelForm.innerHTML = "Enter new username:";
    labelForm.setAttribute("for","newUsername");
    const firstForm = document.createElement("form");
    const newFirst = document.createElement("input");
    const button = document.createElement("button");
    firstForm.id = "userForm";
    newFirst.setAttribute("type","text");
    newFirst.id = "newUsername";
    newFirst.setAttribute("name","newUsername")
    button.setAttribute("type","submit");
    button.setAttribute("class","btn btn-success")
    button.innerHTML = "Change username";
    firstForm.appendChild(labelForm);
    firstForm.appendChild(newFirst);
    firstForm.appendChild(button);
    document.getElementById("usernameData").appendChild(firstForm);
    document.getElementById("userForm").setAttribute("action",newRoute)
    document.getElementById("userForm").setAttribute("method","post")
    }
}

function editLastName() {
    // Executes when the last name is clicked, creating a new form
    if(document.getElementById("lastForm")) {
        console.log("Form already open")
    }
    else {
    user = window.location.pathname.split("/").pop()
    newRoute = "/updateLastname/" + user
    const labelForm = document.createElement("label")
    labelForm.innerHTML = "Enter new last name:";
    labelForm.setAttribute("for","newLastname");
    const firstForm = document.createElement("form");
    const newFirst = document.createElement("input");
    const button = document.createElement("button");
    firstForm.id = "lastForm";
    newFirst.setAttribute("type","text");
    newFirst.id = "newLastname";
    newFirst.setAttribute("name","newLastname")
    button.setAttribute("type","submit");
    button.setAttribute("class","btn btn-success")
    button.innerHTML = "Change last name";
    firstForm.appendChild(labelForm);
    firstForm.appendChild(newFirst);
    firstForm.appendChild(button);
    document.getElementById("lastNameData").appendChild(firstForm);
    document.getElementById("lastForm").setAttribute("action",newRoute)
    document.getElementById("lastForm").setAttribute("method","post")
    }
}

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
                    document.getElementById("firstName").innerHTML = "Please sign in";
                } else {
                    jsonTuple = JSON.parse(text)
                    let firstname = jsonTuple[0]
                    let lastname = jsonTuple[1]
                    let username = jsonTuple[2]
                document.getElementById("firstName").innerHTML = firstname;
                document.getElementById("lastName").innerHTML = lastname;
                document.getElementById("username").innerHTML = username;
            }
            } else {
                console.error(xhttp.statusText);
            }
        }
    };
    xhttp.send();
}

function redirectScore() {
    user = window.location.pathname.split("/").pop();
    console.log(user);
    newRoute = "/myScores/" + user
    window.location.href = newRoute;
}
function redirectAdmin() {
    user = window.location.pathname.split("/").pop();
    console.log(user);
    newRoute = "/adminViewMoods/" + user;
    window.location.href = newRoute;
}
function redirectLogout() {
    window.location.href = "/"
}
//Ben's Code

function redirectHistory() {
    user = window.location.pathname.split("/").pop();
    console.log(user);
    newLink = "/viewMoods/" + user;
    window.location.href = newLink;
};