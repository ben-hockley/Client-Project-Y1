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
    button.innerHTML = "Change first name";
    firstForm.appendChild(labelForm);
    firstForm.appendChild(document.createElement("br"))
    firstForm.appendChild(newFirst);
    firstForm.appendChild(button);
    document.getElementById("firstNameData").appendChild(firstForm);
    document.getElementById("firstForm").setAttribute("action","/updateFirstname")
    document.getElementById("firstForm").setAttribute("method","post")
    }
}

function editUsername() {
    // Executes when the username is clicked, creating a new form
    if(document.getElementById("userForm")) {
        console.log("Form already open")
    }
    else {
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
    button.innerHTML = "Change username";
    firstForm.appendChild(labelForm);
    firstForm.appendChild(document.createElement("br"))
    firstForm.appendChild(newFirst);
    firstForm.appendChild(button);
    document.getElementById("usernameData").appendChild(firstForm);
    document.getElementById("userForm").setAttribute("action","/updateUsername")
    document.getElementById("userForm").setAttribute("method","post")
    }
}

function editLastName() {
    // Executes when the last name is clicked, creating a new form
    if(document.getElementById("lastForm")) {
        console.log("Form already open")
    }
    else {
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
    button.innerHTML = "Change last name";
    firstForm.appendChild(labelForm);
    firstForm.appendChild(document.createElement("br"))
    firstForm.appendChild(newFirst);
    firstForm.appendChild(button);
    document.getElementById("lastNameData").appendChild(firstForm);
    document.getElementById("lastForm").setAttribute("action","/updateLastname")
    document.getElementById("lastForm").setAttribute("method","post")
    }
}

function getDetails() {
    // Fills in the details in the HTML page with database info
    var xhttp = new XMLHttpRequest();
    xhttp.open("GET",'/updateInfo',true);
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