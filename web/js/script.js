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