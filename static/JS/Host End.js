const DATA = document.getElementById("DATA");
var data = DATA.textContent;
data = data.replace(/'/g, '"');
data = data.replace(/\(/g, '[').replace(/\)/g, ']');
data = JSON.parse(data);
if (data.length!=0) {
    HideStuff();
    data = FindUserMaxSore(data);
    MakeChart(data);
}
function HideStuff(){
    const text = document.getElementById("TEXT");
    text.textContent="Scores";
    text.setAttribute("onclick", "Reload()")
    const Inputs = document.getElementById("Inputs");
    Inputs.childNodes.forEach(element => {
        if(element.id!=null){
            element.style.visibility="hidden";
        }
    });
}
function FindUserMaxSore(OldData){
    var data = [];
    OldData.forEach(element => {
        var found = false;
        data.forEach(element2 => {
            if(element[0] == element2[0])
            {
                found=true;
                if(element[1] > element2[1]){
                    element2[1] = element[1];
                }
            }
        });
        if(!found){
            data.push(element);
        }

    });
    return data
}

function MakeChart(data){
    var xValues = [];
    var yValues = [];
    var barColors = "white";
    data.forEach(element => {
        xValues.push(element[0]);
        yValues.push(element[1]);
    });
    new Chart("myChart", {
        type: "bar",
        data: {
            labels: xValues,
            datasets: [{
            backgroundColor: barColors,
            data: yValues
            }]
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true,
                        stepSize: 1,
                        suggestedMax: Math.ceil(Math.max(...yValues))
                    }
                }]
            },
            legend: {display:false}
        }
    });
}
function Reload(){
    location.href = 'http://127.0.0.1:5000/hostEnd?';
}