function checkLength() {
    let input = document.getElementById("userInputForm").value;
    if (input.length > 4000) {
        alert("Your input is too long!");
        return false;
    }
}


function startVoiceAssistant() {
    document.getElementById("headerText").style.color = "green";
    eel.startVoice();
}


async function startText(resp) {
    let result = await eel.startText(resp)();
    let conversation = document.getElementById("conversation");
    let newDiv = document.createElement("div");
    newDiv.setAttribute("class", "aiText");
    newDiv.innerHTML = result;
    conversation.appendChild(newDiv);
}

function submitForm(e) {
    e.preventDefault();

    let myform = document.getElementById("userInputForm");

    let formData = new FormData(myform);

    console.log("form data ", formData);

    fetch("https://show.ratufa.io/json", {
            method: "POST",
            body: formData,
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('network returns error');
            }
            return response.json();
        })
        .then((resp) => {
            console.log("resp from server ", resp);
            myform.reset();
            let formText = formData.get("userInputForm");
            let conversation = document.getElementById("conversation");
            let newDiv = document.createElement("div");
            newDiv.setAttribute("class", "userText");
            newDiv.innerHTML = resp['FormData']['command'];
            conversation.appendChild(newDiv);
            startText(resp);
        })
        .catch((error) => {
            // Handle error
            console.log("error ", error);
        });
}

let myform = document.getElementById("userInputForm");
myform.addEventListener("submit", submitForm);