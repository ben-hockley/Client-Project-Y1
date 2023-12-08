var slider = document.getElementById("moodSlider");
var emoji = document.getElementById("emoji");
let emojiList = ["&#128549","&#128577","&#128528","&#128578","&#128512"];
slider.oninput=function() {
    emoji.innerHTML = emojiList[slider.value];
}