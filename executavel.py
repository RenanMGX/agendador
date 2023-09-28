import subprocess
import schedule
from time import sleep
import json
import datetime

class eventos():
    def __init__(self,nome, event):
        self.nome = nome
        self.event = event

    def iniciar(self):
        try:
            subprocess.Popen(self.event, shell=True)
            self.informar()
        except Exception as error:
            print(f"{datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')} - Não foi possivel executar o programa '{self.nome}' pelo motivo: {error}")

        
    def informar(self):
        print(f"{datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')} - O programa '{self.nome}' foi executado!")


def config_json():
    while True:
        try:
            with open("agenda.json", "r")as arqui:
                data = json.load(arqui)
                return data
        except:
            default = [{"nome":"nome do script","hora" : "09:00", "modo": "diario", "script": "caminho do script"},
                       {"nome":"nome do script","hora" : "12:00", "modo": "diario", "script": "caminho do script"},
                    ]
            with open("agenda.json", "w")as arqui:
                json.dump(default, arqui)


if __name__ == "__main__":

    data = config_json()
    for event in data:
        evento = eventos(event["nome"], event["script"])

        if event["modo"] == "segunda":
            schedule.every().monday.at(event["hora"]).do(evento.iniciar)
        if event["modo"] == "terça":
            schedule.every().tuesday.at(event["hora"]).do(evento.iniciar)
        if event["modo"] == "quarta":
            schedule.every().wednesday.at(event["hora"]).do(evento.iniciar)
        if event["modo"] == "quinta":
            schedule.every().thursday.at(event["hora"]).do(evento.iniciar)
        if event["modo"] == "sexta":
            schedule.every().friday.at(event["hora"]).do(evento.iniciar)
        if event["modo"] == "sabado":
            schedule.every().saturday.at(event["hora"]).do(evento.iniciar)
        if event["modo"] == "domingo":
            schedule.every().sunday.at(event["hora"]).do(evento.iniciar)
        else:
            schedule.every().day.at(event["hora"]).do(evento.iniciar)
        

    print(f"{datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')} - O Script de agendamento foi Iniciado!")
    while True:
        schedule.run_pending()
        minuto = datetime.datetime.now().strftime("%M%S")
        if (minuto == "3000") or (minuto == "0000"):
            print(f"{datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')} - O Script de agendamento está em execução normalmente")
        sleep(1)
