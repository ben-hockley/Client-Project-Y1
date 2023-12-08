let isFunctionRunning = false;


setInterval(function () {
  if (!isFunctionRunning) {
    getMessages();
  } else {
    console.log("Function is still running, skipping this interval.");
  }
}, 1000);


function getMessages(){
    isFunctionRunning = true;
    user = window.location.pathname.split("/").pop()
    quizID = window.location.pathname.slice(0,window.location.pathname.length-user.length-1).split("/").pop()
    newRoute = "/getMessages/" + quizID + "/" + user
    var xhttp = new XMLHttpRequest();
    xhttp.open("GET",newRoute,true);
    xhttp.setRequestHeader("Content-type","application/x-www-form-urlencoded");
    xhttp.onreadystatechange = function() {
        if (xhttp.readyState === 4) {
            if (xhttp.status === 200) {
                var data = xhttp.responseText;
                data = data.replace(/'/g, '"');
                data = data.replace(/\(/g, '[').replace(/\)/g, ']');
                data = JSON.parse(data);
                messageArea = document.getElementById("Messages")
                console.log(messageArea.childNodes[0])
                while (parent.firstChild) {
                    parent.removeChild(parent.firstChild);
                }
                data.forEach(messages => {
                    var date = messages[0];
                    var Time = messages[1];
                    var Username = messages[2];
                    var Message = messages[3];
                    const d = new Date();
                    var dates = d.getDate() + "/" + d.getMonth() + "/" + d.getFullYear()
                    if(date!=dates){
                        Time = date + " at " + Time  
                    }
                    if(NoSpace(Username)==user){
                        const area = document.createElement("div");
                        area.className="right";
                        const name = document.createElement("span");
                        name.className="name";
                        name.textContent=Username
                        const message = document.createElement("p");
                        message.textContent = Message
                        const time = document.createElement("span");
                        time.className="time-right"
                        time.textContent=Time
                        area.appendChild(name);
                        area.appendChild(message);
                        area.appendChild(time);
                        messageArea.appendChild(area);
                    }
                    else{
                        const area = document.createElement("div");
                        area.className="left";
                        const name = document.createElement("span");
                        name.className="name";
                        name.textContent="Username"
                        const message = document.createElement("p");
                        message.textContent = Message
                        const time = document.createElement("span");
                        time.className="time-left"
                        time.textContent=Time
                        area.appendChild(name);
                        area.appendChild(message);
                        area.appendChild(time);
                        messageArea.appendChild(area);
                    }
                });

            } else {
                console.error(xhttp.statusText);
            }
        }
    };
    xhttp.send();
    isFunctionRunning = false;
}
function sendMessage(){
    const message = document.getElementById("sendMessage").value;
    user = window.location.pathname.split("/").pop();
    quizID = window.location.pathname.slice(0,window.location.pathname.length-user.length-1).split("/").pop();
    newRoute = "/sendMessages/" + quizID + "/" + user + "/" + message;
    var xhttp = new XMLHttpRequest();
    xhttp.open("GET",newRoute,true);
    xhttp.setRequestHeader("Content-type","application/x-www-form-urlencoded");
    xhttp.onreadystatechange = function() {
        if (xhttp.readyState === 4) {
            if (xhttp.status === 200) {
                var text = xhttp.responseText;
                console.log(text);

            } else {
                console.error(xhttp.statusText);
            }
        }
    };
    xhttp.send();
    getMessages();
}
function NoSpace(string){
    var newString = "";
    string.split("").forEach(char => {
        if(char == " "){
            newString+="%20";
        }
        else{
            newString+=char;
        }
    });
    return newString;
}