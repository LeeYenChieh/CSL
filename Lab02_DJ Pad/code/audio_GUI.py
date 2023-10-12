import serial
import time
import sys
import pygame
import tkinter as tk
 
COM_PORT = '/dev/cu.usbmodem142101'  # 請自行修改序列埠名稱
BAUD_RATES = 9600
ser = serial.Serial(COM_PORT, BAUD_RATES)
if ser.is_open is True:
    print("Serial port is open!")
music_state = False
volume = 0.3
window = tk.Tk()
window.title('Lab 2')
window.geometry('500x300')
canvas = tk.Canvas(window, bg='white', height=200, width=500)
LOOP_ACTIVE = True

def updateCanvas():
    canvas.delete("all")
    if music_state is True:
        canvas.create_rectangle(242,90,248,110, fill="white", outline='black')
        canvas.create_rectangle(252,90,258,110, fill="white", outline='black')
    else:
        canvas.create_polygon([240,90, 240,110, 260, 100], fill="white", outline='black')
    for i in range(int(volume * 10)):
        canvas.create_rectangle(100 + i*30, 178, 125 + i*30 , 181, fill="white", outline='black')
    canvas.pack()
    window.update()

try:
    file=r'/Users/naonao/Desktop/Avicii-WithoutYou-Instrumental.mp3' # 播放音樂的路徑
    pygame.mixer.init()
    track = pygame.mixer.music.load(file)
    pygame.mixer.music.play()
    pygame.mixer.music.pause()
    
    while LOOP_ACTIVE:
        while ser.in_waiting:
            res = ser.read_until().decode()
            if res == "b\n":
                music_state = not music_state
                if music_state:
                    pygame.mixer.music.unpause()
                else:
                    pygame.mixer.music.pause()
                updateCanvas()
            if res == "v\n":
                v = int(ser.read_until().decode()) / 1024
                pygame.mixer.music.set_volume(v)
                volume = v
                updateCanvas()
        
 
except KeyboardInterrupt:
    ser.close()
    print('exit')

