#####################################################################################
# Placa de aquisiçao para o experimento do Pêndulo 1x canal ADC 12bits
# Autor: Leandro Teixeira, Herlon Dionatam, Ana Clara Santos, Iris Moreno, Rafael Carvalho
#####################################################################################

# Setup da Raspberry Pi Pico
from machine import freq, Pin, ADC
from time import sleep_ms as delay
import time
machine.freq(240000000)

#######################################################################################

##    Função para medir o tempo de uma instrução.

#     start = time.ticks_ms()
#     end = time.ticks_ms()
#     print("Elapsed time:", end, start)
#     print("Elapsed time during the whole program in seconds:", end - start)


#######################################################################################

ax_filtrado = 0 # valorr da média móvel
alfa = 0.9 # 0 < alfa < 1
amplitude = 0 # variavel para controle da abertura angular do pêndulo
sensor = ADC(Pin(26)) # definição do pino analogico onde será colocado o sensor
ax_filtrado = sensor.read_u16() # Leitura inicial do potenciometro

# Função do filtro passa-baixa para retirar o ruido do sinal
def filtro_passa_baixa(valor_previo, novo_valor):
    return alfa * valor_previo + (1 - alfa) * novo_valor

def leitura():
    global ax_novo, ax_filtrado
    while True:
        ax_novo = sensor.read_u16()
        ax_filtrado = filtro_passa_baixa(ax_filtrado, ax_novo)
        print("valor filtrado: ", ax_filtrado, "valor bruto", ax_novo)
        time.sleep(1/50)
        
# Função de leitura do potenciometro pela interface gráfica
def LA0():
    soma = 0
    global ax_novo, ax_filtrado
    for i in range(500):
        soma = soma + sensor.read_u16()   
    ax_novo = int(soma/500)
    ax_filtrado = filtro_passa_baixa(ax_filtrado, ax_novo)
    print(f'#{int(ax_filtrado)}#')
