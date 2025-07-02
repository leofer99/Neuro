import socket
#import keyboard
import logging
import numpy as np
#import joblib
import time
#from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds
#from brainflow.data_filter import DataFilter

""""
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 65432)
s.connect(server_address)
"""
    
# Conexão com raspberry pi
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.connect(("raspberrypi", 5001))
    print("Connected to Raspberry Pi")
except Exception as e:
    print(f"Failed to connect: {e}")
    exit(1)

"""
#Brainflow acquisition:
board_id = BoardIds.CYTON_DAISY_BOARD.value
BoardShim.enable_dev_board_logger()
logging.basicConfig(level=logging.DEBUG) # Ativa as mensagens log do brainflow para fazer debug
params = BrainFlowInputParams()
params.serial_port = 'COM4' # Porta COM do BT dongle no PC
channel_labels = ['C3','CP3','P3','PO3','P7','PO7','Fz','Cz','CPz','Pz','C4','CP4','P4','PO4','P8','PO8']
"""

def generate_prediction():
    pred = 3
    #message = input("Select command (0-Start, 1-Stop, 2-Left, 3-Right, 4-EXIT): ")

    #for i in range(1,6):
    
    return pred
    
def start():

    BoardShim.enable_dev_board_logger()
    logging.basicConfig(level=logging.DEBUG) # Ativa as mensagens log do brainflow para fazer debug

    try:  
        print("\nBoard description: \n")
        print(BoardShim.get_board_descr(board_id))
        board = BoardShim(board_id, params) # Inicialização da board
        board.prepare_session()

        board.start_stream(4500) # O parâmetro corresponde ao tamanho do Buffer. O valor é o default do brainflow
        
        eeg_channels = BoardShim.get_eeg_channels(board_id) # O brainflow adquire dados de várias coisas correspondentes a cada coluna de dados mas apenas 8/16 delas correspondem aos dados do EEG
        sampling_rate = BoardShim.get_sampling_rate(board_id)
        eeg_channels = eeg_channels[0:len(channel_labels)]

    except BaseException:
        logging.warning('Exception', exc_info=True)

    finally:
        logging.info('End')
    if board.is_prepared():
        logging.info('Releasing session')
        board.release_session()  



def main():
    pred=0
    
    while True:
        try:
            pred = generate_prediction()
            print("Message sent to Raspberry Pi: ", pred)
            message = str(pred)
            s.send(message.encode("utf-8"))
            time.sleep(4)           
            # Sleep to avoid tight loop

        except KeyboardInterrupt:
            print("Interrupted by user")
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            break
    s.close()
    print("Socket closed")





if __name__ == "__main__":
    main()

