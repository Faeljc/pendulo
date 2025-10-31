#Plano inclinado por: Rafael Carvalho
from machine import Pin
import utime

TRIG = Pin(2, Pin.OUT)
ECHO = Pin(3, Pin.IN)

def medir_distancia():
    TRIG.low()
    utime.sleep_us(2)
    TRIG.high()
    utime.sleep_us(10)
    TRIG.low()

    while ECHO.value() == 0:
        inicio = utime.ticks_us()
    while ECHO.value() == 1:
        fim = utime.ticks_us()

    duracao = utime.ticks_diff(fim, inicio)
    distancia = (duracao / 2) / 29.1
    return distancia

# Fator de suavização: 0 < alpha < 1
alpha = 0.2
distancia_filtrada = medir_distancia()

while True:
    dist = medir_distancia()
    distancia_filtrada = alpha * dist + (1 - alpha) * distancia_filtrada
    
    #print("Distância filtrada: {:.2f} cm".format(distancia_filtrada))
    print("{:.2f}".format(distancia_filtrada))
    utime.sleep(0.05)
