const WebSocket = require('ws');
const { SerialPort } = require('serialport');
const { ReadlineParser } = require('@serialport/parser-readline');

// Cria uma nova conexão WebSocket e inicializa o servidor na porta 3000
const WebSocketServer = new WebSocket.Server({ port: 3000 });
console.log('Servidor WebSocket iniciado na porta 3000');

// Mapeia conexões WebSocket para portas seriais
const activeConnections = new Map();

// Lida com novas conexões WebSocket
WebSocketServer.on('connection', (socket) => {
    console.log('Novo cliente conectado.');

    let currentPort = null; // Para rastrear a porta serial ativa

    // Lida com mensagens recebidas do cliente
    socket.on("message", async (msg) => {
        try {
            const command = msg.toString().trim();
            console.log('Mensagem recebida:', command);

            // Verifica se a mensagem é um comando válido (neste caso, um caminho de porta serial)
            if (currentPort) {
                console.log('Fechando conexão serial existente...');
                await closePort(currentPort);
                currentPort = null;
            }

            // Configura uma nova porta serial
            currentPort = new SerialPort({
                path: command,
                baudRate: 9600,
                autoOpen: false, // Evita abrir automaticamente antes de validar
            });

            currentPort.open((err) => {
                if (err) {
                    const errorMsg = `Erro ao abrir a porta serial: ${err.message}`;
                    console.error(errorMsg);
                    socket.send(JSON.stringify({ status: 'erro', msg: errorMsg }));
                    currentPort = null;
                    return;
                }
                console.log(`Porta serial ${command} aberta com sucesso.`);
                socket.send(JSON.stringify({ status: 'sucesso', msg: `Conectado à porta ${command}` }));

                // Configura o parser para leitura de dados linha a linha
                const parser = currentPort.pipe(new ReadlineParser({ delimiter: '\n' }));

                // Envia dados recebidos da porta serial para o cliente
                parser.on('data', (result) => {
                    console.log('Dados recebidos da porta serial:', result.trim());
                    socket.send(JSON.stringify({
                        timestamp: new Date().toISOString(),
                        value: result.trim(),
                    }));
                });

                // Lida com erros da porta serial
                currentPort.on('error', (err) => {
                    const errorMsg = `Erro na porta serial: ${err.message}`;
                    console.error(errorMsg);
                    socket.send(JSON.stringify({ status: 'erro', msg: errorMsg }));
                });
            });
        } catch (err) {
            console.error('Erro ao processar mensagem:', err);
            socket.send(JSON.stringify({ status: 'erro', msg: 'Mensagem inválida ou erro interno.' }));
        }
    });

    // Lida com a desconexão do cliente
    socket.on('close', async () => {
        console.log('Cliente desconectado.');
        if (currentPort) {
            console.log('Fechando conexão serial...');
            await closePort(currentPort);
            currentPort = null;
        }
    });
});

// Função para fechar a porta serial com segurança
async function closePort(port) {
    return new Promise((resolve, reject) => {
        port.close((err) => {
            if (err) {
                console.error('Erro ao fechar a porta serial:', err.message);
                return reject(err);
            }
            console.log('Porta serial fechada com sucesso.');
            resolve();
        });
    });
}
