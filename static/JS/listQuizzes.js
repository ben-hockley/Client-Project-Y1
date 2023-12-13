document.addEventListener("DOMContentLoaded", updateQuizMoods())

const checkbox = document.getElementById('Check')
checkbox.addEventListener('change', (event) => {
  if (event.currentTarget.checked) {
    newRoute = "/updateQuizDisplay/T"
    $.ajax({type:'GET', url:newRoute, success: function appendInfo(result) {
        result = JSON.parse(result);
        console.log(result)
        quizzes = document.getElementById("quizzes")
        while (quizzes.firstChild) {
            quizzes.removeChild(quizzes.lastChild);
        }
        for (let i=0; i < Object.keys(result).length; i++) {
            row = "<section class='new-box' id='" + i + "'><section class='quiz-name'><p>" + result[i][0] + "</p></section><section class='quiz-code'><p>" + result[i][1] + "</section>"
            $("#quizzes").append(row);
            document.getElementById(i).addEventListener("click", function() {
                user = window.location.pathname.split("/").pop();
                newRoute = "/hostEnd/"+result[i][1]+"/"+user;
                window.location = newRoute;
})}}});
} else {
    newRoute = "/updateQuizDisplay/F"
    $.ajax({type:'GET', url:newRoute, success: function appendInfo(result) {
        result = JSON.parse(result);
        console.log(result)
        quizzes = document.getElementById("quizzes")
        while (quizzes.firstChild) {
            quizzes.removeChild(quizzes.lastChild);
        }
        for (let i=0; i < Object.keys(result).length; i++) {
            row = "<section class='new-box' id='" + i + "'><section class='quiz-name'><p>" + result[i][0] + "</p></section><section class='quiz-code'><p>" + result[i][1] + "</section>"
            $("#quizzes").append(row);
            document.getElementById(i).addEventListener("click", function() {
                user = window.location.pathname.split("/").pop();
                newRoute = "/displayQuizCode/" + result[i][0] + "/" + result[i][1] + "/" + user;
                window.location = newRoute;
})}}})}});
function updateQuizMoods() {
    newRoute = "/updateQuizDisplay/F"
    $.ajax({type:'GET', url:newRoute, success: function appendInfo(result) {
        result = JSON.parse(result);
        for (let i=0; i < Object.keys(result).length; i++) {
        row = "<section class='new-box' id='" + i + "'><section class='quiz-name'><p>" + result[i][0] + "</p></section><section class='quiz-code'><p>" + result[i][1] + "</section>"
        $("#quizzes").append(row);
        document.getElementById(i).addEventListener("click", function() {
            user = window.location.pathname.split("/").pop();
            newRoute = "/displayQuizCode/" + result[i][0] + "/" + result[i][1] + "/" + user;
            window.location = newRoute;
        })
    }
    }});
}