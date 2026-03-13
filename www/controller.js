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

});