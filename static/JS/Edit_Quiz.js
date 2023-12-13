const DATA = document.getElementById("data");
var data = DATA.textContent;
data = data.replace(/'/g, '"');
data = data.replace(/\(/g, '[').replace(/\)/g, ']');
data = JSON.parse(data);
printData(data);
function printData (data){
    const parentNode=document.getElementById("Questions");
    data.forEach(element => {
        const Question = document.createElement("span");
        Question.textContent=element[1];
        console.log(Question.textContent)
        parentNode.appendChild(Question);
    });
}