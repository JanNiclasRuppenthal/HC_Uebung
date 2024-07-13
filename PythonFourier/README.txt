Bevor man ueberhaupt ein Python-Skript starten kann, muss man zuerst alle Bibliotheken installieren. Hierfuer kann man den folgenden Befehl verwenden:
pip install -r requirements.txt


----------------------------------------------------------------------------------------------------------------------


Aufgabe 01:
Um nun das Skript fuer die sequenzielle Fourieranalyse in FFT\fft_seq.py zu starten, muss man den folgenden Befehl verwenden:
python FFT\fft_seq.py <Pfad zur WAV-Datei> <Blockgroesse> <Versatz> <Schwellwert>

oder 

python3 FFT\fft_seq.py <Pfad zur WAV-Datei> <Blockgroesse> <Versatz> <Schwellwert>


Hierbei gibt es verschiedene Varianten, die man fuer die letzten drei Parameter verwenden kann:
    - Blockgroesse ist ein Integer, der zwischen 64 und 512 eingeschraenkt wird.
    - Versatz ist ein Integer, der zwischen 1 und Blockgroesse eingeschraenkt wird.
    - Schwellwert ist eine positive Fliesskommazahl


----------------------------------------------------------------------------------------------------------------------


Aufgabe 02:
Um nun das Skript zur Generierung von Audiodateien in Generate\WAV_Generator.py zu starten, muss man den folgenden Befehl verwenden:
python Generate\WAV_Generator.py <Dateiname> <Funktionsname> <Dauer in Sekunden> <Abtastrate> <Sonstige Parameter>

oder 

python3 Generate\WAV_Generator.py <Dateiname> <Funktionsname> <Dauer in Sekunden> <Abtastrate> <Sonstige Parameter>


Fuer den Parameter Funktionsname gibt es verschiedene Optionen, die man auswaehlen kann:
    - sine 
    - add
    - am
    - fm 
    - segmented 
    - envelope
    - harmonics
    - triangle
    - rectangle 
    - chirp
    - noise

Jede der Funktionen benoetigt auch noch verschiedene Parameter, die man in <Sonstige Parameter> festlegen kann:
    - sine benoetigt genau eine Frequenz.
    - add benoetigt eine Folge von Frequenzen.
    - am benoetigt genau zwei Frequenzen.
    - fm benoetigt auch zwei Frequenzen und einen Index.
    - segmented braucht eine Folge von Frequenzen und eine Dauer fuer die einzelnen Segmenten.
    - envelope muss man nur eine Frequenz uebergeben.
    - harmonics benoetigt eine Hauptfrequenz und eine natuerliche Zahl fuer die Anzahl der Harmonischen.
    - triangle benoetigt nur eine Frequenz.
    - rectangle benoetigt auch nur eine Frequenz .
    - chirp muss man zwei Frequenzen uebergeben.
    - noise hat keine Parameter.


Beispiele der Befehle, die auch fuer den Bericht zu den Audiodateien verwendet wurden:
<Dateiname> sine 1 44100 440
<Dateiname> add 1 44100 400 800 1200
<Dateiname> am 1 44100 440 600
<Dateiname> fm 1 44100 440 600 2
<Dateinname> segmented 1 44100 10 1000 0.5
<Dateiname> envelope 1 44100 440
<Dateiname> harmonics 1 44100 440 3
<Dateiname> triangle 1 44100 440
<Dateiname> rectangle 1 44100 440
<Dateiname> chirp 1 44100 400 1200
<Dateiname> noise 1 44100 


----------------------------------------------------------------------------------------------------------------------


Aufgabe 03:
Um nun das Skript fuer die parallele Fourieranalyse in FFT\fft_par_multiprocess.py oder FFT\fft_par_threading.py auf der CPU zu starten, muss man den folgenden Befehl verwenden:
python <FFT\fft_par_multiprocess.py oder FFT\fft_par_threading.py> <Pfad zur WAV-Datei> <Blockgroesse> <Versatz> <Schwellwert> 

oder 

python3 <FFT\fft_par_multiprocess.py oder FFT\fft_par_threading.py> <Pfad zur WAV-Datei> <Blockgroesse> <Versatz> <Schwellwert> 

Die Parameter wurden bereits in der ersten Aufgabe beschrieben.


----------------------------------------------------------------------------------------------------------------------


Aufgabe 04:
Um nun das Skript fuer die parallele Fourieranalyse in FFT\fft_openCL.py auf der GPU zu starten, muss man den folgenden Befehl verwenden:
python FFT\fft_openCL.py <Pfad zur WAV-Datei> <Blockgroesse> <Versatz> <Schwellwert>

oder 

python3 FFT\fft_openCL.py <Pfad zur WAV-Datei> <Blockgroesse> <Versatz> <Schwellwert>

Die Parameter wurden bereits in der ersten Aufgabe beschrieben.


----------------------------------------------------------------------------------------------------------------------


Sonstige Dateien:
Die Datei plotting.py erstellt Diagramme zu den Hauptfrequenzen, die in verschiedene TXT-Dateien geschrieben werden. Dazu muss man zuerst eine Fourieranalyse durchgefuehrt haben. Die Datei kann folgendermassen gestartet werden:
python Plot_Data\plotting.py oder python3 Plot_Data\plotting.py 