----------------------------------------------------------------------------------------------------------------------


Dies ist die Abgabe des Projekts von Jan Niclas Ruppenthal (Matrikelnummer: 1481198) zur Veranstaltung "Heterogenous Computing".


----------------------------------------------------------------------------------------------------------------------


Der Ergebnisbericht befindet sich in der PDF "HC_Projekt_Ruppenthal.pdf". In diesem Bericht erklaere ich die Funktionsweise, den Aufbau, aufgetretene Probleme und moegliche Verbesserungen meiner Remote-Wetterstation.


----------------------------------------------------------------------------------------------------------------------


Wenn man das Proejkt selbst verwenden moechte, dann muss man noch die folgende Datei wifi_configuration.py in 'wifi' hinzufuegen. Dabei muss der Inhalt der Datei folgendermassen aussehen:

    ssid = 'SSID_NAME'
    password = 'ROUTER_PASSWORD'
    server_ip = 'IP-ADRESSE DER AUSSENSTATION'


----------------------------------------------------------------------------------------------------------------------

Hier beschreiben, dass die Datei Pico_ePaper.py von Waveshare ist (https://github.com/waveshareteam/Pico_ePaper_Code/blob/main/python/Pico_ePaper-2.9.py)

Meine Implementierung der Remote-Wetterstation besteht aus vier Teilen:
    - Der Ordner 'indoor' enthaelt die Dateien, die von der Innentation verwendet werden.
    - Der Ordner 'outdoor' enthaelt die Datei, die von der Aussenstation verwendet wird.
    - Das Verzeichnis 'util' besteht aus Dateien, die von beiden Stationen genutzt werden.
    - Der letzte Teil 'wifi' ist fuer den Verbindungsaufbau, die Integration der Webseite und der Implementierung der HTTP-Requests zustaendig.

Betrachten wir nun im folgendem die einzelnen Dateien und ihre Funktionsweisen. 

Im Ordner 'indoor' befindet sich die Hauptdatei main.py. In dieser Datei befindet sich die Funktionsweise der Innenstation. Hier werden die Sensoren sowie das ePaper Display initialisiert. Zusaetzlich wird eine Verbindung zum Router aufgebaut, damit man uber eine IP-Adresse auf die Wetterstation zugreifen kann. Innerhalb der while-True-Schleife werden alle zehn Minuten ueberprueft, ob sich das Datum geaendert hat, sowie Daten von den Sensoren Station und der Sensoren der Aussenstation gelesen. Falls sich die Werte geaendert haben, dann werden die neuen Daten auf das ePaper Display geschrieben. Zudem wird jede 0.1 Sekunde ueberprueft, ob ein Client auf den Webserver zugreifen moechte. Falls dies der Fall ist, wird die Webseite, die in wifi/web_server.py definiert ist, an den Client gesendet. 
Der Ordner 'indoor' enthaelt auch den Ordner 'display', der fuer die Konfiguration des ePaper Displays zustaendig ist. In config_display.py wird das Display konfigueriert. Hierbei werden auch die diversen Werten auf dem Display aktualisiert. Die Datei Pico_ePaper.py ist die Implementierung der Klassen und Methoden fuer genau dieses Display. Dabei ist diese Datei eine angepasste Version von von Waveshare (https://github.com/waveshareteam/Pico_ePaper_Code/blob/main/python/Pico_ePaper-2.9.py), denn ich habe zwei print-Statements aus dem Quellcode entfernt. 

Das Verzeichnis 'outdoor' besteht nur aus der Hauptdatei main.py, die auf der Aussenstation gestartet wird. Hierbei ist die Vorhensweise aehnlich zur main.py in 'indoor'. Zuerst werden alle Sensoren initialisiert sowie eine Verbindung zum Internet aufgebaut. Danach werden erneut alle zehn Minuten die Daten von den Sensoren gelesen und gespeichert. Des Weiteren wird auch hier alle 0.1 Sekunden ueberprueft, ob ein Client auf den Webserver zugreifen moechte. Der gesendete HTML-Code befindet sich auch in wifi/web_server.py.

Im Ordner 'util' befindet sich die Datei config_date.py, die verschiedene Funktionen zur Datum-Initialisierung bereitstellt. Dabei nutzt der Raspberry Pi Pico W das Network Time Protocol (NTP), um ueber das Internet die aktuelle Uhrzeit und das Datum zu beziehen. Zudem enthaelt die Datei auch eine Funktion, die die erste Ziffer der Minute zurueckgibt. Damit kann in allen main.py-Dateien getestet werden, ob schon zehn Minuten vergangen sind. Des Weiteren gibt es auch noch die Datei measurements.py in 'util'. Hier werden Funktionen zur Initialisierung und Messungen von den Sensoren definiert.

In 'wifi' besteht aus drei Dateien, die fuer die Wifi-Integration der Remote Wetterstation verantwortlich sind. Die Datei http_request.py wird nur von der Innenstation verwendet. Hierbei werden ueber GET-Requests die Daten der Sensoren der Aussenstation ueber HTTP angefordert. Der Verbindungsaufbau zum Router wird in web_server.py realisiert. Hierbei werden auch die Webseiten der jeweilgen Stationen definiert. Die letzte Datei wifi_configuration.py, welche nicht auf GitHub hochgeladen wurde, enthaelt die SSID, das Passwort meines Routers und die IP-Adresse der Aussenstation.

----------------------------------------------------------------------------------------------------------------------


Meine Loesungen zur ersten Uebung befinden sich im Branch Uebung01.
Meine Loesungen zur zweiten Uebung befinden sich im Branch Uebung02.


----------------------------------------------------------------------------------------------------------------------