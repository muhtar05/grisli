$(document).ready(function () {
 
    var url = "ws://mkala05.ru/parser";
    var socket = new WebSocket(url);
    socket.onopen = function() {
           console.log("Соединение установлено.");
           socket.send('hello');
           
    };

    
    socket.onmessage = function(event){
        var data = JSON.parse(event.data);

        var resText = $("#result").text();
        var infoText = $("#info").text();
        resText +="<Дата " + data.time_url + ">: ";

        infoText += data.url + "- \n";
        if (data.success == true){
           resText += "Успех \n";
           infoText += "\t Title: " + data.title + " \n \t Encoding: " + data.encoding + "\n"; 
        }else {
          resText = "Ошибка \n";
          infoText +="";
        }

       $("#result").text(resText);
       $("#info").text(infoText);
    };
});
