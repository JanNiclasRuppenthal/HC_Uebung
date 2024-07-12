Bevor man ueberhaupt ein Python-Skript starten kann, muss man zuerst alle Bibliotheken installieren. Hierfuer kann man den folgenden Befehl verwenden:
pip install -r requirements.txt



Aufgabe 01:
Um nun das Skript fuer die sequentielle Fourieranalyse in (FFT\fft_seq.py) zu starten, muss man den folgenden Befehl verwenden:
python FFT\fft_seq.py <Pfad zur WAV-Datei> <Blockgroesse> <Versatz> <Schwellwert>

oder 

python3 FFT\fft_seq.py <Pfad zur WAV-Datei> <Blockgroesse> <Versatz> <Schwellwert>


Hierbei gibt es verschiedene Varianten, die man fuer die letzten drei Parameter verwenden kann:
    - Blockgroesse ist ein Integer, der zwischen 64 und 512 eingeschraenkt wird.
    - Versatz ist ein Integer, der zwischen 1 und Blockgroesse eingeschraenkt wird.
    - Schwellwert ist eine positive Fliesskommazahl



Aufgabe 02:
Um nun das Skript fuer die sequentielle Fourieranalyse in (Generate\WAV_Generator.py) zu starten, muss man den folgenden Befehl verwenden:
python Generate\WAV_Generator.py <Pfad zur WAV-Datei> <Blockgroesse> <Versatz> <Schwellwert>

oder 

python3 Generate\WAV_Generator.py <Pfad zur WAV-Datei> <Blockgroesse> <Versatz> <Schwellwert>


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
    - sine benoetigt genau eine Frequenz
    - add benoetigt eine Folge von Frequenzen
    - am benoetigt genau zwei Frequenzen
    - fm benoetigt auch zwei Frequenzen und einen Index
    - segmented braucht eine Folge von Frequenzen und eine Dauer fuer die Segmente 
    - envelope muss man nur eine Frequenz uebergeben
    - harmonics benoetigt eine Hauptfrequenz und eine natuerliche Zahl fuer die Harmonischen
    - triangle benoetigt nur eine Frequenz
    - rectangle benoetigt auch nur eine Frequenz 
    - chirp braucht wieder eine Frequenz 
    - noise muss man zwei Frequenzen uebergeben


Beispiele der Befehle, die auch fuer den Ergebnisbericht verwendet wurden:
sine.wav sine 1 44100 440
add.wav add 1 44100 400 800 1200
am.wav am 1 44100 440 600
fm.wav fm 1 44100 440 600 2
envelope.wav envelope 1 44100 440
harmonics.wav harmonics 1 44100 440 3
chirp.wav chirp 1 44100 400 1200
noise.wav noise 1 44100


Aufgabe 03:
Um nun das Skript fuer die parallele Fourieranalyse in (FFT\fft_par.py) auf der CPU zu starten, muss man den folgenden Befehl verwenden:
python FFT\fft_par.py <Dateiname> <Funktionsname> <Dauer in Sekunden> <Abtastrate> <Sonstige Parameter>

oder 

python3 FFT\fft_par.py <Dateiname> <Funktionsname> <Dauer in Sekunden> <Abtastrate> <Sonstige Parameter>


Die Parameter wurden schon bei der ersten Aufgabe beschrieben.



Aufgabe 04:
TODO



Sonstige Dateien:
Die Datei plotting.py erstellt Diagramme zu den Hauptfrequenzen, die in verschiedene TXT-Dateien geschrieben werden. Dazu muss man zuerst eine Fourieranalyse durchgefuehrt haben. Die Datei kann folgendermassen gestartet werden:
python Plot_Data\plotting.py oder python3 Plot_Data\plotting.py 