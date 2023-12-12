document.addEventListener("DOMContentLoaded", updateQuizMoods())

function updateQuizMoods() {
    user = window.location.pathname.split("/").pop();
    newRoute = "/updateScores/" + user;
    $.ajax({type:'GET', url:newRoute, success: function appendInfo(result) {
        result = JSON.parse(result);
        for (let i=0; i < Object.keys(result).length; i++) {
            row = "<tr><td class='form-text'><section class='vertical-center'>" + result[i][0] + "</section></td><td class='emoji'><section class='vertical-center'>" + result[i][1] + "</section></td><td class='emoji'><section class='vertical-center'>" + result[i][2] + "</section></td></tr>";
            $("#quizScores").append(row);
    }
    }});
}