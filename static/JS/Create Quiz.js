var number = -1;
const thingy = document.getElementById("Fancy");
thingy.click();
function AddAnswer(event){
    const sect = event.target.parentNode.parentNode;
    const parent=sect.parentNode;
    const number = parent.childNodes[1].childNodes[3].name[0];
    const node = sect.childElementCount+2;
    const num = 4;
    if (node<18){
        const inp = document.createElement("input");
        inp.id=number+"Answer"+String((node)/num);
        inp.name=number+"Answer"+String((node)/num);
        inp.className="Answer";
        inp.type="text";
        const p = document.createElement("span")
        p.textContent="Answer " + String((node)/num) + " ";
        const inp2 = document.createElement("input");
        inp2.id=number+"Is"+String((node)/num);
        inp2.name=number+"Is"+String((node)/num);
        inp2.className="Not";
        inp2.type="checkbox";
        inp2.textContent="F";
        inp2.setAttribute("onclick", "On(event)");
        sect.appendChild(p);
        sect.appendChild(inp);
        sect.appendChild(inp2);
        sect.appendChild(document.createElement("br"));
    }
}
function TakeAnswer(event){    
    const section = document.createElement("section");
    const sect = event.target.parentNode.parentNode;
    const node = sect.childElementCount+3
    if (node>16){
        for (let i = 0; i < 4; i++){
            sect.removeChild(sect.lastChild);
        }
    }
}
function Hide(event){
    const BTN = event.target;
    const parent = BTN.parentNode.parentNode;
    const parent2 = parent.childNodes[1];   
    if(parent2.className=="Hide"){
        parent2.className = "Answers";
        BTN.textContent="v";
    }
    else{
        parent2.className="Hide";
        BTN.textContent=">";
    }     
}
function AddQuestion(event){
    number++;
    const sect = event.target.parentNode;
    const imp1= document.createElement("section"); imp1.className="Question";
    sect.appendChild(imp1);
    const sect2 = sect.childNodes[sect.childElementCount+1];
    const imp2= document.createElement("button"); imp2.type="button"; imp2.setAttribute("onclick","Hide(event)"); imp2.id="bland";imp2.textContent="v";
    const imp3= document.createElement("input"); imp3.name=number+"Question"; imp3.type="text"; imp3.id="Question";
    const imp4= document.createElement("section"); imp4.className="Answers"; imp4.id="Answers";
    const imp0= document.createElement("section"); imp0.className="Inputs"; imp0.id="Inputs";
    const imp5= document.createElement("button"); imp5.type="button"; imp5.setAttribute("onclick","Delete(event)"); imp5.id="bland";imp5.textContent="X";
    sect2.appendChild(imp0)
    sect2.appendChild(imp4);
    sect2.appendChild(document.createElement("span"))
    const sect4 = sect2.childNodes[sect2.childElementCount-3];
    sect4.appendChild(imp2);
    sect4.appendChild(imp3);
    sect4.appendChild(imp5);
    const sect3 = sect2.childNodes[sect2.childElementCount-2];
    const imp6=document.createElement("button"); imp6.type="button"; imp6.setAttribute("onclick", "AddAnswer(event);"); imp6.id="bland"; imp6.textContent="+";
    const imp7=document.createElement("button"); imp7.type="button"; imp7.setAttribute("onclick", "TakeAnswer(event);"); imp7.id="bland"; imp7.textContent="-";
    const inp3=document.createElement("section"); inp3.className="AddTake"; inp3.id="AddTake";
    sect3.appendChild(inp3);
    const sect5 = sect3.childNodes[sect3.childElementCount-1];
    sect5.appendChild(imp6);
    sect5.appendChild(imp7);
    const imp8=document.createElement("br");
    const imp9=document.createElement("span"); imp9.textContent="Answer 1 ";
    const imp10=document.createElement("input"); imp10.name=number+"Answer1"; imp10.type="text"; imp10.className="Answer"; imp10.id="Answer1";
    const inp1 = document.createElement("input"); inp1.setAttribute("onclick", "On(event)"); inp1.id=number+"Is1"; inp1.name=number+"Is1"; inp1.className="Not"; inp1.type="checkbox";inp1.textContent="F";
    const imp11=document.createElement("br");
    const imp12=document.createElement("span"); imp12.textContent="Answer 2 ";
    const imp13=document.createElement("input"); imp13.name=number+"Answer2"; imp13.type="text"; imp13.className="Answer"; imp13.id="Answer2";
    const inp0 = document.createElement("input"); inp0.setAttribute("onclick", "On(event)"); inp0.id=number+"Is2"; inp0.name=number+"Is2";  inp0.className="Not"; inp0.type="checkbox"; inp0.textContent="F";
    const imp14=document.createElement("br");
    sect3.appendChild(imp8);
    sect3.appendChild(imp9);
    sect3.appendChild(imp10);
    sect3.appendChild(inp1);
    sect3.appendChild(imp11);
    sect3.appendChild(imp12);
    sect3.appendChild(imp13);
    sect3.appendChild(inp0);
    sect3.appendChild(imp14);
    TestForBlank(sect);
}            
function Delete(event){
    const parent = event.target.parentNode.parentNode;
    const parent2 = parent.parentNode;
    parent2.removeChild(parent);
    TestForBlank(parent2);
}
function TestForBlank(parent2){
    const nodes = parent2.childNodes.length
    const Submit = document.getElementById("SubmitSect");
    const btn = Submit.childNodes[Submit.childNodes.length-2];
    if(nodes < 9){
        btn.id="Nothing"
        btn.type="button"
    }
    else{
        btn.id="Fancy"
        btn.type="Submit"
    }
}
function On(event){
    if(event.target.className=="Not"){
        event.target.className="is";
        event.target.textContent="T";
    }
    else if(event.target.className="is"){
        event.target.className="Not";
        event.target.textContent="F";
    }
}