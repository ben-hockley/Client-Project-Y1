document.addEventListener("DOMContentLoaded", updateQuizMoods())

function updateQuizMoods() {
    newRoute = "/updateQuizDisplay"
    $.ajax({type:'GET', url:newRoute, success: function appendInfo(result) {
        result = JSON.parse(result);
        for (let i=0; i < Object.keys(result).length; i++) {
        row = "<section class='newBox' id='" + i + "'><section class='quizName'><p>" + result[i][0] + "</p></section><section class='quizCode'><p>" + result[i][1] + "</section>"
        $("#quizzes").append(row);
        document.getElementById(i).addEventListener("click", function() {
            user = window.location.pathname.split("/").pop();
            newRoute = "/displayQuizCode/" + result[i][0] + "/" + result[i][1] + "/" + user;
            window.location = newRoute;
        })
    }
    }});
}