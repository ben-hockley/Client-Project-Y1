document.addEventListener("DOMContentLoaded", updateQuizDisplay())

function updateQuizDisplay() {
    newRoute = "/updateQuizDisplay"
    $.ajax({type:'GET', url:newRoute, success: function appendInfo(result) {
        result = JSON.parse(result);
        for (let i=0; i < Object.keys(result).length; i++) {
        row = "<section class='new-box' id='" + i + "'><section class='quiz-name'><p>" + result[i][0] + "</p></section><section class='quiz-code'><p>" + result[i][1] + "</section>"
        $("#quizzes").append(row);
        document.getElementById(i).addEventListener("click", function() {
            user = window.location.pathname.split("/").pop();
            newRoute = "/adminViewScores/" + result[i][0] + "/" + result[i][1] + "/" + user;
            window.location = newRoute;
        })
    }
    }});
}