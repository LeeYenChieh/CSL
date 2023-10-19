import serial
import time
import sys
import pygame
 
COM_PORT = 'COM3'
BAUD_RATES = 9600
ser = serial.Serial(COM_PORT, BAUD_RATES)
if ser.is_open is True:
    print("Serial port is open!")
music_state = 0
print("Start!")
try:
    file=r'Avicii-WithoutYou-Instrumental.mp3' # 播放音樂的路徑
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
                print(v)
                pygame.mixer.music.set_volume(v)
                if v < 0.2 and music_state and v > 0.000001:
                    pygame.mixer.music.pause()
                    music_state = not music_state
                    print('pause')
                elif v >= 0.2 and not music_state:
                    pygame.mixer.music.unpause()
                    music_state = not music_state
                    print('start')
 
except KeyboardInterrupt:
    ser.close()
    print('exit')

