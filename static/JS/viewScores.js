document.addEventListener("DOMContentLoaded", updateQuizMoods())

function updateQuizMoods() {
    user = window.location.pathname.split("/").pop();
    newRoute = "/updateScores/" + user;
    $.ajax({type:'GET', url:newRoute, success: function appendInfo(result) {
        result = JSON.parse(result);
        for (let i=0; i < Object.keys(result).length; i++) {
            row = "<tr><td class='form-text'>" + result[i][0] + "</td><td class='form-text'>" + result[i][1] + "</td><td class='form-text'>" + result[i][2] + "</td></tr>";
            $("#quizScores").append(row);
    }
    }});
}