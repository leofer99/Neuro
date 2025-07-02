import socket
import time
from threading import Timer
import socket
import time
from threading import Timer
#from Control import *
#from  Ultrasonic import *
#from  Buzzer import *
#from  Servo import *

# Create object
#control = Control()
#ultra = Ultrasonic()
#buzz = Buzzer()
#servo = Servo()
number=-1

#define variables
uppie=2
downie=-2
uppie2=20
downie2=-20

#control.speed = 5
#buzz.run("0")


def receive_data():
    #s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #s.bind(('', 5001))
    #s.listen(5)
    #print('Server is now running.')
    #conn, addr = s.accept()
    #print("Connected by", addr)

    #return conn

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 65432)
    server_socket.bind(server_address)
    server_socket.listen(1)
    conn, addr = server_socket.accept()

    return conn


def test_distance():
      pode_sair = 0 #não pode andar
      time_beg= time.time()
      distance = ultra.getDistance()
      if distance <=5: #se algo estiver a menos de 5 centímetros do cão durante mais de um segundo, altera o modo para unsafe
        time_unsafe = time.time()
        mode="unsafe"

        if (time.time()-time_unsafe>=1): #avisa user passados 2 segundos, se ainda não tiver a distância mínima
            print ("Distance less than 5 cm for over 1 sec")

      else:
        mode="safe"

      return mode


if __name__ == "__main__":
    mov_class=0
    conn=receive_data()

    while True:
        try:
            #reads data from socket
            data = conn.recv(1024)
            mov_class = data.decode("utf-8")

            distance = ultra.getDistance()

            mov_class=1
            print("mov_class: ", mov_class)
            mode="unsafe"

            if mode=="unsafe":

                if mov_class==0: #Rest
                    control.stop()

                if mov_class==1: #Nods Head (alternative to Forward, when its unsafe)
                    servo.setServoAngle(15,161) 
                    time.sleep(1)
                    servo.setServoAngle(15,19) 
                    time.sleep(1)
                    servo.setServoAngle(15,90)
                    print("Nod. Distance: ", distance)

                if mov_class==2: #Walk Backward
                    time_beg= time.time()
                    if (time.time() - time_beg)<=3: 
                        control.backWard()
                        print("backWard. Distance: ", distance)
                        control.stop()

                if mov_class==3: #Turn Left (alternativa: Raise Height)
                    time_beg= time.time()
                    if (time.time() - time_beg)<=3:
                        #control.turnLeft()
                        control.upAndDown(uppie)
                        print("Turn Left. Distance: ", distance)
                        control.stop()

                if mov_class==4: #Turn Right: (alternativa: Lower Height)
                    time_beg= time.time()
                    if (time.time() - time_beg)<=3:
                        #control.turnRight()
                        control.upAndDown(downie)
                        print("Turn Right. Distance: ", distance)
                        control.stop()


            if mode=="safe":
                if mov_class==0: #Rest
                    control.stop()

                if mov_class==1: #Walk Forward
                    time_beg= time.time()
                    if (time.time() - time_beg)<=3:
                        control.forWard() 
                        print("Walk Forward. Distance: ", distance)
                        control.stop()

                if mov_class==2: #Walk Backward
                    time_beg= time.time()
                    if (time.time() - time_beg)<=3:
                        control.backWard()
                        print("Walk Backward. Distance: ", distance)
                        control.stop()

                if mov_class==3: #Turn Left
                    time_beg= time.time()
                    if (time.time() - time_beg)<=3:
                        control.turnLeft()
                        #control.upAndDown(uppie2)
                        print("Turn Right. Distance: ", distance)
                        control.stop()

                if mov_class==4: #Turn Right
                    time_beg= time.time()
                    if (time.time() - time_beg)<=3:
                        control.turnRight()
                        #control.upAndDown(downie2)
                        print("Turn Left. Distance: ", distance)
                        control.stop()

        finally:
            conn.close()
            print(f"Connection closed")

