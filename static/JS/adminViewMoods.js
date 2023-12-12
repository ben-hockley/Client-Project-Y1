document.addEventListener("DOMContentLoaded", updateQuizMoods())
const interval = setInterval(updateQuizMoods, 5000);
function updateQuizMoods() {
    let emojiList = ["&#128549","&#128577","&#128528","&#128578","&#128512"];
    user = window.location.pathname.split("/").pop();
    newRoute = "/updateQuizMoodAdmin/" + user;
    $.ajax({type:'GET', url:newRoute, success: function appendInfo(result) {
        result = JSON.parse(result);
        $("#adminQuizMoods").html("");
        $("#adminQuizMoods").append("<tr><td>Quiz Title</td><td>Username</td><td>Mood Before</td><td>Mood After</td></tr>")
        for (let i=0; i < Object.keys(result).length; i++) {
            row = "<tr><td class='form-text'>" + result[i][0] + "</td><td class='form-text'>" + result[i][1] + "</td><td class='emoji'>" + emojiList[result[i][2]] + "</td><td class='emoji'>" + emojiList[result[i][3]] + "</td></tr>";
            $("#adminQuizMoods").append(row);
    }
    }});
}