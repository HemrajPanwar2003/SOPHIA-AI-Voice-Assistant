$(Document).ready(function(){
    //Display speak Message
    eel.expose(DisplayMessage)
    function DisplayMessage(message){
        
        $(".siri-message li:first").text(message);
        $('.siri-message').textillate('start');

    }

    //Display hood
    eel.expose(ShowHood)
    function ShowHood(){
       $("#Ovel").attr("hidden", false);
       $("#SiriWave").attr("hidden", true);
    }

eel.expose(senderText)
function senderText(message) {
    const chatBox = document.getElementById("chat-canvas-body");

    if (!message || message.trim() === "") return;

    const msgDiv = document.createElement("div");
    msgDiv.className = "message sender_message";
    msgDiv.textContent = message; // ✅ safe (prevents HTML injection)

    chatBox.appendChild(msgDiv);

    // Auto scroll
    chatBox.scrollTop = chatBox.scrollHeight;
}


eel.expose(receiverText)
function receiverText(message) {
    const chatBox = document.getElementById("chat-canvas-body");

    if (!message || message.trim() === "") return;

    const msgDiv = document.createElement("div");
    msgDiv.className = "message receiver_message";
    msgDiv.textContent = message;

    chatBox.appendChild(msgDiv);

    // Auto scroll
    chatBox.scrollTop = chatBox.scrollHeight;
}


});