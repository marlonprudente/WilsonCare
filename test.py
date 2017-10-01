#import the library
from pyA20.gpio import gpio
from pyA20.gpio import port
from time import sleep
import pyrebase
from datetime import datetime

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
gpio.setcfg(port.PA7, gpio.OUTPUT)
gpio.setcfg(port.PA8, gpio.INPUT)


def main():
   data = datetime.now()
   print data
   teste = db.child("pacientes/oZuB8VfohicfwT5unXiV7H8Mkpy2/remedios/").get()
   for lista in teste.each():
      pathH = ("pacientes/oZuB8VfohicfwT5unXiV7H8Mkpy2/remedios/") + str(lista.key()) + ("/horario")
      pathD = ("pacientes/oZuB8VfohicfwT5unXiV7H8Mkpy2/remedios/") + str(lista.key()) + ("/doses")
      pathI = ("pacientes/oZuB8VfohicfwT5unXiV7H8Mkpy2/remedios/") + str(lista.key()) + ("/intervalo")
      hora = db.child(pathH).get()
      doses = db.child(pathD).get()
      intervalo = db.child(pathI).get()
      print ("\nDoses: ") + doses.val() + ("/ Horario: ") + hora.val() + ("/ Intervalo: ") + intervalo.val()
   sleep(2)
#   print  data.strftime("%Y-%m-%d-%H-%M-%S")
 #  sleep(2)
#now we do something (light up the LED)
while True:
   main()
#   if gpio.input(port.PA8):
#      gpio.output(port.PA7, gpio.HIGH)
     #db.child("Data1").push("botao_ligado", user['idToken'])
#      sleep(2)
#   gpio.output(port.PA7, gpio.LOW)
