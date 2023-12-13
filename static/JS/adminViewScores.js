document.addEventListener("DOMContentLoaded", updateQuizScores())
const interval = setInterval(updateQuizScores, 5000);
function updateQuizScores() {
    user = window.location.pathname.split("/").pop();
    quizCode = window.location.pathname.split("/").slice(-2)[0];
    newRoute = "/updateAdminScores/" + quizCode + "/" + user;
    $.ajax({type:'GET', url:newRoute, success: function appendInfo(result) {
        result = JSON.parse(result);
        // $("#table-data").html("");
        data = $("#table-data");
        data.html("");
        for (let i=0; i < Object.keys(result).length; i++) {
            row = "<tr><td class='form-text username'><section class='vertical-center'>" + result[i][0] + "</section></td><td class='emoji score'><section class='vertical-center'>" + result[i][1] + "</section></td><td class='emoji max-points'><section class='vertical-center'>" + result[i][2] + "</section></td></tr>";
            data.append(row);
    } $("#score-table").append(data);
    }});
}