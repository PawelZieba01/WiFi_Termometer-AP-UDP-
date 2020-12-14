import socket

import machine
from machine import Pin

import network

from time import sleep

import onewire
import ds18x20



#definicje wiadomości msg
msg_ds_error = "Nie wykryto czujnika temperatury"
msg_remote_error = "Nie podłączono urządzenia Wi-Fi"
msg_remote_connected = "Połączenie udane"
msg_remote_waiting = "Oczekiwanie na podłączenie urządzenia Wi-Fi"


#konfiguracja AP
ap_ip = "192.168.2.1"
ap_mask = "255.255.255.0"
ap_gate = "192.168.2.1"
ap_dns = "8.8.8.8"
ap_ssid = "Termometr WI-FI"

#konfiguracja zdalnego urządzenia
remote_adr = "192.168.2.2"
reomote_port = 20001



#utworzenie socketu UDP
UDPClientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#WLAN
ap = network.WLAN(network.AP_IF)

#RTC
rtc = machine.RTC()

#DS18B20
ds_pin = machine.Pin(15)
ds = ds18x20.DS18X20(onewire.OneWire(ds_pin))



#inicjalizacja WLAN
ap.active(True)
ap.ifconfig((ap_ip, ap_mask, ap_gate, ap_dns))
ap.config(essid = ap_ssid)

#inicjalizacja pinu LED
led = Pin(2, Pin.OUT)



#oczekiwanie na podłączenie urządzenia Wi-Fi
print(msg_remote_waiting)
while ap.isconnected() == False:
    led.value(1)
    sleep(0.2)
    led.value(0)
    sleep(0.2)
    print(".", end =" ")
    
print("")
print(msg_remote_connected)

print("AP CONFIG:  ", end =" ")
print(ap.ifconfig())



led.value(1)
sleep(5)
led.value(0)
sleep(0.1)
led.value(1)
sleep(0.1)
led.value(0)
sleep(0.1)
led.value(1)
sleep(0.1)
led.value(0)
sleep(0.1)
led.value(1)
sleep(0.1)
led.value(0)
sleep(0.1)
led.value(1)
sleep(0.1)
led.value(0)
sleep(0.1)
led.value(1)
sleep(0.1)
led.value(0)





#skan urzadzeń 1-wire
roms = ds.scan()
print('Znaleziono urządzenie 1-wire: ', roms)

#ustawienie rozdzielczości czujnika temp na 12 bit 
if roms:
    ds.write_scratch(roms[0], b'\x00\x00\x7f')


#konfiguracja RTC
rtc.datetime((2014, 5, 1, 4, 0, 0, 0, 0))


while 1:
    
    #skan i kontrola obecności  urządzeń 1-wire
    roms = ds.scan()
    
    if len(roms) > 0:
        ds_ok = True
    else:
        ds_ok = False
        
    
    
    #sprawdzenie czy urządzenie Wi-Fi jest podłączone
    if ap.isconnected():
        
        #rozkaz pomiaru temperatury + kontrola obecności  urządzenia 1-wire
        try:
            ds.convert_temp()
        except:
            ds_ok = False
            
                
        #jeżeli wykryto czujnik temperatury to mrugaj co 1s, w przeciwnym razie świeć cały czas (LED)
        if ds_ok == True:    
            led.value(0)
            sleep(0.5)
            led.value(1)
            sleep(0.5)
        else:
            led.value(1)
            sleep(1)
        
        
        #odczytanie temperatury z czujnika + kontrola obecności  urządzenia 1-wire
        try:
            temp = round(ds.read_temp(roms[0]), 1)
        except:
            ds_ok = False
            
            
            
            
            
            
        #pobranie i konwersja wizualna czasu 3 > 03 ...
        hours = rtc.datetime()[4]
        minutes = rtc.datetime()[5]
        seconds = rtc.datetime()[6]
        
        if hours < 10:
            hours = "0" + str(hours)
        else:
            hours = str(hours)
            
            
        if minutes < 10:
            minutes = "0" + str(minutes)
        else:
            minutes = str(minutes)
            
            
        if seconds < 10:
            seconds = "0" + str(seconds)
        else:
            seconds = str(seconds)
            
             
        time = hours + ":" + minutes + ":" + seconds    
        
            
            
            
            
            
        
        #jeżeli pomiar się wykonał - czujnik temperatury jest podłączony
        if ds_ok == True:
     
            #przygotowanie wiadomości do wysłania 
            temp_msg = time + "     Temperatura:   " + str(temp)
            
            
            print (temp_msg)
     
     
            #wyślij jeżeli jest podłączone urządzenie Wi-Fi
            if ap.isconnected():
                UDPClientSocket.sendto(temp_msg, (remote_adr, reomote_port))

            
        else:
             #informacja o braku czujnika temperatury
             print(time + "     " + msg_ds_error)
             
             #wyślij jeżeli jest podłączone urządzenie Wi-Fi
             if ap.isconnected():
                 UDPClientSocket.sendto(time + "     " + msg_ds_error, (remote_adr, reomote_port))
             
                 
        
        
        
        
    else:
        #informacja o braku podłączonego urządzenia Wi-Fi
        print(msg_remote_error)
        
        led.value(1)
        sleep(0.2)
        led.value(0)
        sleep(0.2)
