// function userCheck(e) {
//     var username = document.forms["loginForm"]["username"].value;
//     var password = document.forms["loginForm"]["password"].value;
//     params = 'username='+username+'&password='+password;
    
//     var xhttp = new XMLHttpRequest();
//     xhttp.open("POST", '/logonFunction', true);
//     xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
//     xhttp. onreadystatechange = function() {
//         if (xhttp.readyState === 4 && xhttp.status === 200) {
//             console.log(xhttp.responseText);
//             document.getElementById("errorMessage").innerHTML = xhttp.responseText;
//         } else {
//             console.error(xhttp.statusText);
//         }
//     };
        
//     xhttp.send(params);
//     return false;
// }
