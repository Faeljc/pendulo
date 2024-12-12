const WebSocket = require('ws');
const { SerialPort } = require('serialport');
const { ReadlineParser } = require('@serialport/parser-readline');

// Configura a porta serial
const port = new SerialPort({
    path: 'COM3', // Substitua pela sua porta
    baudRate: 9600, // Taxa de transmissão
});

// Configura o parser para ler linha a linha
const parser = port.pipe(new ReadlineParser({ delimiter: '\n' }));

// Lida com erros de conexão
port.on('error', (err) => {
    console.error('Erro na porta serial:', err.message);
});

//Cria uma nova conexão e um servidor é inicializado na porta 3000
const WebSocketServer = new WebSocket.Server({
    port: 3000,
});

//Inicia a conexão que imprime a mensagem 'Recebido' casoa  mensagem seja 'Hello' envia 'World'
WebSocketServer.on('connection', (socket) => {
    socket.on("message", (msg) => {
        console.log('Recebido: ', msg.toString());

        // Evento para quando os dados são recebidos
        parser.on('data', (result) => {
            console.log(result)
            const data = {
                timestamp: new Date().toISOString(),
                value: result.trim() // Simulação de valor aleatório
            };
            socket.send(JSON.stringify(data));  // Envia os dados como JSON
        });

    });
});
