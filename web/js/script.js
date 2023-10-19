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


function startText(resp) {
    eel.startText(resp);
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
            startText(resp);
        })
        .catch((error) => {
            // Handle error
            console.log("error ", error);
        });
}

let myform = document.getElementById("userInputForm");
myform.addEventListener("submit", submitForm);