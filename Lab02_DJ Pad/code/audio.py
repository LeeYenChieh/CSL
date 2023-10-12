import serial
import time
import sys
import pygame
 
COM_PORT = '/dev/cu.usbmodem142101'  # 請自行修改序列埠名稱
BAUD_RATES = 9600
ser = serial.Serial(COM_PORT, BAUD_RATES)
if ser.is_open is True:
    print("Serial port is open!")
music_state = 0

try:
    file=r'/Users/naonao/Desktop/Avicii-WithoutYou-Instrumental.mp3' # 播放音樂的路徑
    pygame.mixer.init()
    track = pygame.mixer.music.load(file)
    pygame.mixer.music.play()
    pygame.mixer.music.pause()
    
    while True:
        while ser.in_waiting:
            res = ser.read_until().decode()
            if res == "b\n":
                music_state = not music_state
                if music_state:
                    pygame.mixer.music.unpause()
                else:
                    pygame.mixer.music.pause()
            if res == "v\n":
                v = int(ser.read_until().decode()) / 1024
                pygame.mixer.music.set_volume(v)
 
except KeyboardInterrupt:
    ser.close()
    print('exit')

