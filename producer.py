import time
import paho.mqtt.client as mqtt
import json


print("Conectando ao MQTT Broker...")
mqtt_client = mqtt.Client()
mqtt_client.connect('localhost', 1883)

#Como foi tratado bastante sobre o caso do COVID-19, a ideia no código seria para ter o controle da quantidade de pessoas
#em um ambiente, visto que temos restrição no número de pessoas em certos lugares fechados.
#com isso o programa incrementa (quando alguém entra pela porta) e decrementa (quando sai pela porta), e quando o valor
# for menor ou igual a 0, informa que não há cliente no ambiente.

from pynput import keyboard

count = 0

def on_press(key):  # The function that's called when a key is pressed
    global count

    if key == keyboard.Key.enter:
        count += 1
        print(count)
        mensagem = {
            'qts': 'pessoa(s)',
            'total': count
        }
        mqtt_client.publish('in242', json.dumps(mensagem))
    elif key == keyboard.Key.space:
        count -= 1
        print(count)
        mensagem = {
            'qts': 'pessoa(s)',
            'total': count
        }
        mqtt_client.publish('in242', json.dumps(mensagem))

    if count <= 0:
        print('Nenhum cliente no estabelecimento!')
        mensagem = {
          'qts': 'Nenhum cliente no estabelecimento!'
        }
        mqtt_client.publish('in242', json.dumps(mensagem))

def main():
    with keyboard.Listener(on_press=on_press) as listener:  # Setup the listener
         listener.join()                                     # Join the thread to the main thread

if __name__ == '__main__':
    main()

