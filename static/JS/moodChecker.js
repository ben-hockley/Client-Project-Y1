var slider = document.getElementById("moodSlider");
var emoji = document.getElementById("emoji");
let emojiList = ["&#128545","&#128544","&#128546","&#128577","&#128528","&#128578","&#128512","&#129321","&#129322"];
slider.oninput=function() {
    emoji.innerHTML = emojiList[slider.value];
}