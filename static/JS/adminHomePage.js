function redirectCurrentMoods() {
    user = window.location.pathname.split("/").pop();
    console.log(user);
    newLink = "/GlobalMoodViewer/" + user;
    window.location.href = newLink;
};
function redirectQuizMoods() {
    user = window.location.pathname.split("/").pop();
    console.log(user);
    newLink = "/adminViewMoods/" + user;
    window.location.href = newLink;
};
function redirectQuizScores() {
    user = window.location.pathname.split("/").pop();
    console.log(user);
    newLink = "/adminViewQuizzes/" + user;
    window.location.href = newLink;
};