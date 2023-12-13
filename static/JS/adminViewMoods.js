document.addEventListener("DOMContentLoaded", updateQuizMoods())
const interval = setInterval(updateQuizMoods, 5000);
function updateQuizMoods() {
    let emojiList = ["&#128545","&#128544","&#128546","&#128577","&#128528","&#128578","&#128512","&#129321","&#129322"];
    user = window.location.pathname.split("/").pop();
    newRoute = "/updateQuizMoodAdmin/" + user;
    $.ajax({type:'GET', url:newRoute, success: function appendInfo(result) {
        result = JSON.parse(result);
        $("#adminQuizMoods").html("");
        $("#adminQuizMoods").append("<tr><td>Quiz Title</td><td>Username</td><td>Mood Before</td><td>Mood After</td></tr>")
        for (let i=0; i < Object.keys(result).length; i++) {
            row = "<tr><td class='form-text'><section class='vertical-center'>" + result[i][0] + "</section></td><td class='form-text'><section class='vertical-center'>" + result[i][1] + "</section></td><td class='emoji'><section class='vertical-center'>" + emojiList[result[i][2]] + "</section></td><td class='emoji'><section class='vertical-center'>" + emojiList[result[i][3]] + "</section></td></tr>";
            $("#adminQuizMoods").append(row);
    }
    }});
}