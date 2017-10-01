#import the library
from pyA20.gpio import gpio
from pyA20.gpio import port
from time import sleep
from multiprocessing import Process
import pyrebase
import os
from datetime import datetime
#from WilsonCare import test

#initialize the gpio module
gpio.init()
config = {
  "apiKey": "AIzaSyBF8bgCiq0V0Br3bUuIg5wm5eENryVZ1ck",
  "authDomain": "wilsoncare-dad95.firebaseapp.com",
  "databaseURL": "https://wilsoncare-dad95.firebaseio.com/",
  "storageBucket": "wilsoncare-dad95.appspot.com"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
user = auth.sign_in_with_email_and_password("marlonmateuspr@gmail.com", "wilson2")
db = firebase.database()
#setup the port (same as raspberry pi's gpio.setup() function)
gpio.setcfg(port.PA7, gpio.OUTPUT) # LED ou Buzzer
gpio.setcfg(port.PA8, gpio.INPUT) # Botao Emergencia
gpio.setcfg(port.PA9, gpio.INPUT) # Sensor de Presenca
gpio.setcfg(port.PA10,gpio.INPUT) # Geladeira
gpio.setcfg(port.PG6, gpio.INPUT) # Botao remedio
gpio.setcfg(port.PG7, gpio.OUTPUT) # LED remedio

gpio.pullup(port.PA10, gpio.PULLUP) # Configurando Sensor geladeira (Precisa de borda de subida, para ativar)


#multiprocessing
def remedio():
   while True:
      horanow = datetime.now().strftime("%H:%M")
      remedios = db.child("pacientes/oZuB8VfohicfwT5unXiV7H8Mkpy2/remedios/").get()
      for lista in remedios.each():
         pathH = ("pacientes/oZuB8VfohicfwT5unXiV7H8Mkpy2/remedios/") + str(lista.key()) + ("/horario")
         pathD = ("pacientes/oZuB8VfohicfwT5unXiV7H8Mkpy2/remedios/") + str(lista.key()) + ("/doses")
         pathI = ("pacientes/oZuB8VfohicfwT5unXiV7H8Mkpy2/remedios/") + str(lista.key()) + ("/intervalo")
         hora = db.child(pathH).get()
         doses = db.child(pathD).get()
         intervalo = db.child(pathI).get()
         if(hora.val()==horanow):
            tomar = lista.key()
            if gpio.input(port.PG6):
               pathHtomar = ("pacientes/oZuB8VfohicfwT5unXiV7H8Mkpy2/remedios/") + str(tomar) + ("/horario")
               pathDtomar = ("pacientes/oZuB8VfohicfwT5unXiV7H8Mkpy2/remedios/") + str(tomar) + ("/doses")
               hora = db.child(pathHtomar).get()
               doses = db.child(pathDtomar).get()
               db.child(pathHtomar).update(hora.val() + timedelta(hours=intervalo.val()))
               db.child(pathDtomar).update(doses.val() - 1)

         sleep(1)

#Thread de panico
def panico():
   while True:
      hora = datetime.now().strftime("%H:%M")
      data = datetime.now().strftime("%d/%m/%Y")
      if gpio.input(port.PA8):
         panico = {"acionador": "Botao", "hora": hora, "data": data}
         db.child("pacientes/oZuB8VfohicfwT5unXiV7H8Mkpy2/panico").push(panico)
         print panico
         sleep(1)

Process(target=remedio).start()
Process(target=panico).start()

#Funcao principal
def main():
   data = datetime.now().strftime("%d/%m/%Y")
   hora = datetime.now().strftime("%H:%M")
   if gpio.input(port.PA10) or gpio.input(port.PA9):
      if gpio.input(port.PA10):
         geladeira = {"sensor": "Geladeira", "hora": hora, "data": data}
         db.child("pacientes/oZuB8VfohicfwT5unXiV7H8Mkpy2/sensores").push(geladeira)
         print geladeira
      if gpio.input(port.PA9):
         quarto = {"sensor": "Quarto", "hora": hora, "data": data}
         db.child("pacientes/oZuB8VfohicfwT5unXiV7H8Mkpy2/sensores").push(quarto)
         print quarto
      gpio.output(port.PA7, gpio.HIGH)
      sleep(2)
   gpio.output(port.PA7, gpio.LOW)

print "Iniciando Wilson...\n"
#Atualizar horario
os.system("sudo ntpd ntp.on.br")

#Iniciar Wilson
print "Wilson: Hello World!"
while True:
   main()
