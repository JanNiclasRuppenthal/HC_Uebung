----------------------------------------------------------------------------------------------------------------------


Dies ist die Abgabe des Projekts von Jan Niclas Ruppenthal (Matrikelnummer: 1481198) zur Veranstaltung "Heterogenous Computing".


----------------------------------------------------------------------------------------------------------------------


Der Ergebnisbericht befindet sich in der PDF "HC_Projekt_Ruppenthal.pdf". In diesem Bericht erklaere ich den allgemeinen Aufbau, die Funktionsweise, aufgetretene Probleme und moegliche Verbesserungen meiner Remote-Wetterstation. Des Weiteren habe ich drei verschiedene Videos hinzugefuegt, die die Ladezeiten der Webseite auf drei Geraeten veranschaulichen soll. Hierbei laedt die Webseite das verwendete Framework PyScript, damit Graphen im Browser angezeigt werden koennen.  


----------------------------------------------------------------------------------------------------------------------


Wenn man das Projekt selbst verwenden moechte, dann muss man noch die Datei wifi_configuration.py in 'wifi' hinzufuegen. Dabei muss der Inhalt der Datei folgendermassen aussehen:

    ssid = 'SSID_NAME'
    password = 'ROUTER_PASSWORD'
    server_ip = 'IP-ADRESSE DER AUSSENSTATION'


----------------------------------------------------------------------------------------------------------------------

Meine Implementierung der Remote-Wetterstation besteht aus vier Teilen:
    - Der Ordner 'indoor' enthaelt die Dateien, die von der Innentation verwendet werden.
    - Der Ordner 'outdoor' enthaelt die Datei, die von der Aussenstation verwendet wird.
    - Das Verzeichnis 'util' besteht aus Dateien, die von beiden Stationen genutzt werden.
    - Der letzte Teil 'wifi' ist fuer den Verbindungsaufbau, die Integration der Webseite und der Verwendung der HTTP-Requests zustaendig.

Betrachten wir nun im Folgenden die einzelnen Dateien und ihre Funktionen. 

Im Ordner 'indoor' befindet sich die Hauptdatei main.py. In dieser Datei befindet sich die Funktionsweise der Innenstation. Hier werden die Sensoren sowie das E-Paper Display initialisiert. Zusaetzlich wird eine Verbindung zum Router aufgebaut, damit man uber eine IP-Adresse auf die Wetterstation zugreifen kann. Innerhalb der while-True-Schleife werden alle zehn Minuten eine Aenderung des Datums ueberprueft sowie Daten von den verbundenen Sensoren und den Sensoren der Aussenstation gelesen. Falls sich die Messwerte geaendert haben, dann werden diese auf das E-Paper Display geschrieben. Zudem wird jede Sekunde ueberprueft, ob ein Client auf den Webserver zugreifen moechte. Wenn dies der Fall ist, wird die Webseite, die in wifi/web_server.py definiert ist, an den Client gesendet. 
Das Verzeichnis 'indoor' enthaelt zudem den Ordner 'display', der fuer die Konfiguration des E-Paper Displays zustaendig ist. In config_display.py wird das Display konfigueriert. Hierbei werden auch die diversen Werten auf dem Display aktualisiert. Die Datei Pico_ePaper.py ist die Implementierung der Klassen und Methoden fuer genau dieses Display. Dabei ist sie eine angepasste Version der Originaldatei von Waveshare (https://github.com/waveshareteam/Pico_ePaper_Code/blob/main/python/Pico_ePaper-2.9.py), da ich zwei print-Statements aus dem Quellcode entfernt habe. 

Das Verzeichnis 'outdoor' besteht nur aus der Hauptdatei main.py, die auf der Aussenstation gestartet wird. Hierbei ist die Vorgehensweise aehnlich zur main.py in 'indoor'. Zuerst werden alle Sensoren initialisiert sowie eine Verbindung zum Internet aufgebaut. Danach werden erneut alle zehn Minuten die Daten von den Sensoren gelesen und gespeichert. Des Weiteren wird auch hier jede Sekunden ueberprueft, ob ein Client auf den Webserver zugreifen moechte. Der gesendete HTML-Code befindet sich in wifi/web_server.py.

Im Ordner 'util' befindet sich die Datei config_date.py, die verschiedene Funktionen zur Datum-Initialisierung bereitstellt. Dabei nutzt der Raspberry Pi Pico W das Network Time Protocol (NTP), um ueber das Internet die aktuelle Uhrzeit und das Datum zu beziehen. Zudem enthaelt die Datei auch eine Funktion, die die erste Ziffer der aktuellen Minute zurueckgibt. Damit kann in allen main-Dateien getestet werden, ob schon zehn Minuten vergangen sind. Des Weiteren gibt es auch noch die Datei measurements.py in 'util'. Hier werden die Funktionen zur Initialisierung und Messung der Sensoren definiert.

In 'wifi' befinden sich drei Dateien, die fuer die Wi-Fi Integration der Remote Wetterstation verantwortlich sind. Die Datei http_request.py wird nur von der Innenstation verwendet. Hierbei werden ueber GET-Requests die Sensordaten der Aussenstation ueber HTTP angefordert. Der Verbindungsaufbau zum Router wird in web_server.py realisiert. Hierbei werden auch die Webseiten der jeweilgen Stationen definiert. Die letzte Datei wifi_configuration.py, welche nicht auf GitHub hochgeladen wurde, enthaelt die SSID, das Passwort meines Routers und die IP-Adresse der Aussenstation.

----------------------------------------------------------------------------------------------------------------------


Meine Loesungen zur ersten Uebung befinden sich im Branch Uebung01.
Meine Loesungen zur zweiten Uebung befinden sich im Branch Uebung02.


----------------------------------------------------------------------------------------------------------------------