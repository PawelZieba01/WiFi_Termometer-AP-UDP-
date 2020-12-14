# WiFi_Termometer-AP-UDP-
[ESP32] [Micropython]

Termometr Wi-Fi (UDP->TERMINAL)

Paweł Zięba 03.04.2020

ESP32 wysyła czas, liczony od startu nadawania i  temperaturę z czujnika ds18b20.
Wykrywanie braku czujnika 1-wire i podłączonego urządzenia Wi-Fi.
Praca w trybie ACCES POINT jako client.
Komunikacja przez UDP.

Po uruchomieniu dioda mruga co 0,4s - czeka na połączenie,
po udanym połączeniu z telefonem dioda świeci przez 5s po czym kilka razy mruga co 0,2s.
Następnie zaczyna wysyłać dane co 1s.

dioda mruga co 0,4s: oczekiwanie na podłączenie urządzenia Wi-Fi (remote)
dioda mruga co 1s: wysyłanie danych
dioda świeci cały czas: brak czujnika temperatury

dane AP:
SSID: Termometr Wi-Fi
HASŁO: <BRAK HASŁA>
IP: 192.168.2.1
maska: 255.255.255.0
brama: 192.168.2.1
dnd: 8.8.8.8

dane urządzenia (remote)
IP: 192.168.2.2  <-------------- TO MUSI BYĆ USTWAIONE KONIECZNIE!!!
maska: 255.255.255.0
brama: 192.168.2.1

PORT: 20001


Termometr wysyła dane na PORCIE 20001 na adres ip 192.168.2.2 !!!

Na urządzeniu zdalnym (smartfon, komputer) musi być zainstalowana aplikacja umożliwiająca uruchomienie serwera UDP ("server udp" w google aps)