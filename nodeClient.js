const WebSocket = require('ws');

//Cria um novo webSocket com a url e porta que será feita a comunicação
const ws = new WebSocket("ws://localhost:3000");

//Abre uma conexão
ws.on('open', () => {
    console.log("Connected");
});

//Fecha a conexão caso seja perdida por algum motivo
ws.on('close', () => {
    console.log("Disconnected");
});

//Recebe a mensagem e imprime no terminal
ws.on("message", (message) => {
    console.log(`Received: ${message}`);
});

//Envia a mensagem no intervalo de 1000 milesegundos
setInterval(() => {
    ws.send("Hello");
}, 1000);