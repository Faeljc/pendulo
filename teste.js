const {SerialPort} = require('serialport');
const {ReadlineParser} = require('@serialport/parser-readline');

// Configure a porta serial
const port = new SerialPort({
    path: 'COM3', // Substitua pela sua porta
    baudRate: 9600, // Taxa de transmissão
  });

// Configura o parser para ler linha a linha
const parser = port.pipe(new ReadlineParser({ delimiter: '\n' }));

// Evento para quando os dados são recebidos
parser.on('data', (data) => {
  console.log('Dados recebidos:', data);
});

// Lida com erros de conexão
port.on('error', (err) => {
  console.error('Erro na porta serial:', err.message);
});
