from machine import ADC, Pin, UART
from time import sleep

# Configuração do ADC no pino GPIO26
pot = ADC(Pin(27))  # Terminal central do potenciômetro conectado ao GPIO26

# Configuração da UART (porta serial)
uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))  # Ajuste os pinos conforme necessário

# Calibração inicial (ajuste conforme os valores medidos)
adc_min = 11100    # Valor do ADC no ponto mais à esquerda
adc_max = 16700    # Valor do ADC no ponto mais à direita

# Mapeia os valores do ADC para graus
#Calcula os valores do adc e retorna um valor inteiro aproximado
def map_value(value, in_min, in_max, out_min, out_max):
    return int((value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

# Parâmetro para outliers
threshold = 5600  # Diferença aceitável do valor anterior

previous_value = pot.read_u16()  # Valor inicial

while True:
    # Lê o valor do ADC do potenciômetro
    adc_value = pot.read_u16()
    
    # Verifica se o valor está dentro do limite de variação
    if abs(adc_value - previous_value) > threshold:
        # Ignora o valor se for um outlier
        print(f"Ignorando outlier: {adc_value}")
        continue
    
    # Atualiza o valor anterior
    previous_value = adc_value
    
    # Converte o valor para a faixa de -90 a +90 graus
    angle = map_value(adc_value, adc_min, adc_max, -90, 90)
    
    # Limita o valor para evitar extrapolações fora da faixa
    angle = max(-90, min(90, angle))
    
    # Envia os dados via UART (como string formatada)
    uart.write(f"Ângulo: {angle} graus\n")
    
    # Debug no terminal
    #print(f"Valor ADC: {adc_value}, Ângulo: {angle} graus")
    
    print(angle)
    # Pausa para estabilizar a leitura
    sleep(0.1)
