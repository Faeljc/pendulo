from machine import ADC, Pin, UART
from time import sleep

# Configuração do ADC no pino GPIO27
pot = ADC(Pin(27))

# Configuração da UART
uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))

# Calibração
adc_min = 11100
adc_max = 16700

# Mapeia os valores do ADC para graus
def map_value(value, in_min, in_max, out_min, out_max):
    return int((value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

# Parâmetros
threshold = 5600
alpha = 0.2  # Quanto menor, mais suave

# Valor inicial
adc_raw = pot.read_u16()
filtered_value = adc_raw  # inicia com o primeiro valor lido

while True:
    adc_raw = pot.read_u16()

    # Filtro passa-baixa exponencial
    filtered_value = int(alpha * adc_raw + (1 - alpha) * filtered_value)

    # Outlier check (opcional, pode comentar se estiver muito suave)
    if abs(filtered_value - adc_raw) > threshold:
        print(f"Ignorando outlier: {adc_raw}")
        continue

    # Mapeia e limita
    angle = map_value(filtered_value, adc_min, adc_max, -90, 90)
    angle = max(-90, min(90, angle))

    # UART e debug
    uart.write(f"Ângulo: {angle} graus\n")
    print(angle)

    sleep(0.1)

