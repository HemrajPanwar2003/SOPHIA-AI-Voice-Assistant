$(document).ready(function() {
    $('.text').textillate({
        loop:true,
        sync:true,
        in:{
           effect:"bounceIn",
        },
        out:{
           effect:"bounceOut",
        },
      });


    var siriWave = new SiriWave({
    container: document.getElementById("siri-container"),
    width: 800,
    height: 200,
    style:"ios9",
    amplitude:"1",
    speed:"0.2",
    autostart:true
    });

      $('.siri-message').textillate({
        loop:true,
        sync:true,
        in:{
           effect:"fadeInUp",
           sync:true,
        },
        out:{
           effect:"fadeOutUp",
           sync:true,
        },
       });

   $("#micBtn").click(function(){
      $("#Ovel").attr("hidden", true);
      $("#SiriWave").attr("hidden", false);
      eel.playClickSound();
      eel.allCommands()();

   });

   function doc_keyUp(e) {

    // Check Ctrl + J (Windows/Linux) or Cmd + J (Mac)
    if ((e.key === 'j' || e.key === 'J') && (e.ctrlKey || e.metaKey)) {

        eel.playAssistantSound();

        $("#Oval").attr("hidden", true);
        $("#SiriWave").attr("hidden", false);

        eel.allCommands();  // ✅ fixed
    }
}

document.addEventListener('keyup', doc_keyUp, false);

$(document).ready(function () {

    // 🔹 Play Assistant
    function PlayAssistant(message) {
        message = message.trim();

        if (message === "") return;

        // Show user message instantly (optional but recommended)
        senderText(message);

        // UI changes
        $("#Oval").attr("hidden", true);
        $("#SiriWave").attr("hidden", false);

        // Send to Python backend
        eel.allCommands(message);

        // Clear input
        $("#chatbox").val("");

        // Reset buttons properly
        ShowHideButton("");

        // Prevent spam clicking
        $("#SendBtn").prop("disabled", true);
        setTimeout(() => {
            $("#SendBtn").prop("disabled", false);
        }, 500);
    }


    // 🔹 Toggle Mic / Send button
    function ShowHideButton(message) {
        message = message.trim();

        if (message.length === 0) {
            $("#MicBtn").attr("hidden", false);
            $("#SendBtn").attr("hidden", true);
        } else {
            $("#MicBtn").attr("hidden", true);
            $("#SendBtn").attr("hidden", false);
        }
    }


    // 🔹 Input typing (better than keyup)
    $("#chatbox").on("input", function () {
        ShowHideButton($(this).val());
    });


    // 🔹 Send button click
    $("#SendBtn").on("click", function () {
        PlayAssistant($("#chatbox").val());
    });


    // 🔹 Enter key (modern + fixed)
    $("#chatbox").on("keydown", function (e) {
        if (e.key === "Enter") {
            e.preventDefault(); // 🚫 stop newline
            PlayAssistant($(this).val());
        }
    });

});

});