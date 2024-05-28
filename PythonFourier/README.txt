Bevor das Skript main.py gestartet werden kann, muss man zuerst alle Bibliotheken herunterladen. Hierfuer kann man den folgenden Befehl verwenden:
pip install -r requirements.txt

Danach werden alle verwendeten Bibliotheken installiert. Ich hoffe, dass dies reibungslos funktioniert, da ich auf dem altem Raspberry Pi Probleme wegen der Installation hatte. Aber auf Linux Mint funktionierte die Installation reibungslos.


Um nun das Skript fuer die Fourieranalyse zu starten, muss man den folgenden Befehl verwenden:
python main.py ..\resources\<Name der WAV-Datei> <Blockgroesse>

oder 

python3 main.py ..\resources\<Name der WAV-Datei> <Blockgroesse>





Falls Sie die Fehlermeldung "ImportError: libopenblas.so.0: cannot open shared object file or directory" bekommen, dann muessen sie diese Bibliothek installieren:
sudo apt-get install libopenblas-dev






Die Datei plotting.py erstellt Diagramme zu den Hauptfrequenzen, die in verschiedene TXT-Dateien geschrieben werden. Dazu muss man zuerst eine Fourieranalyse durchgefuehrt haben. Die Datei kann folgendermassen gestartet werden:
python plotting.py oder python3 plotting.py 

Die letzte Datei plotting_memory.py erstellt Diagramme zum gemessenem Speicherbedarf. Die Diagramme koennen auch nur nach einer Fourieranalyse generiert werden. Mit dem folgendem Befehl kann das Skript gestartet werden:
python plotting_memory.py oder python3 plotting_memory.py 