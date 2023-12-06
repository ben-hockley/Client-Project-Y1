const DATA = document.getElementById("DATA");
var data = DATA.textContent;
data = data.replace(/'/g, '"');
data = data.replace(/\(/g, '[').replace(/\)/g, ']');
data = JSON.parse(data);
var questionNumber = 0;
var points = 0;
var answers = [];
var count = '';
var timer = document.getElementById("TIMER")
Setup()
function Setup(){
    if(questionNumber<data.length){
        const answerSection = document.getElementById("AnswerSection");
        var num = 0;
        var questions = [];
        for (let i = 0; i < (data[questionNumber])[1].length; i++){
            questions.push((data[questionNumber])[1][i]);
        }
        
        for (let i = 0; i < (data[questionNumber])[2].length; i++){
            questions.push((data[questionNumber])[2][i]);
        }
        var numbers=[];
        for (let i = 0; i < questions.length; i++) {
            const element = questions[i];
            numbers.push(i);
        }
        for (let i = 0; i < questions.length; i++) {
            const X = numbers[Math.floor(Math.random() * numbers.length)]
            numbers = numbers.filter(function(element) {return element !== X;});
            const element = questions[X];
            num++;
            var answerButton = document.createElement("button");
            answerButton.type="button";
            answerButton.id="answer"+num;
            answerButton.textContent=(element);
            answerButton.setAttribute("onclick", "isItCorrect(event)");
            answerSection.appendChild(answerButton);
        }
        const questionNumberElement = document.getElementById("QuestionNumber");
        questionNumberElement.textContent="Q"+(questionNumber+1);
        const question = document.getElementById("Question");
        question.textContent= (data[questionNumber])[0];
    }
    else{
        const answerSection = document.getElementById("AnswerSection");
        const questionNumberElement = document.getElementById("QuestionNumber");
        questionNumberElement.textContent="Quiz";
        const question = document.getElementById("Question");
        question.textContent= "You scored "+points+" out of "+data.length+" points";
        const Submit = document.createElement("button");
        Submit.type = "submit"
        Submit.textContent="Submit score";
        const point = document.getElementById("POINTS")
        point.value=points;
        answerSection.appendChild(Submit);
    }
}
function isItCorrect(event) {
    const answerSection = document.getElementById("AnswerSection");
    while (answerSection.childNodes.length>0) {
        const element = answerSection.childNodes[0];    
        answerSection.removeChild(element);
    };
    answers.push(event.target.textContent);
    correct = data[questionNumber][1]
    var rewarded=false
    correct.forEach(answer => {
        if(answers[answers.length-1]==answer){
            if(!rewarded){
                points++; 
                rewarded=true           
            }
        }
    });
    questionNumber++;
    Setup();
}