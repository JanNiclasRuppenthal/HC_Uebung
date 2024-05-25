Sie haben auch die Moeglichkeit eine .jar ueber Maven zu erstellen:
mvn clean package


Nach diesem Befehl werden zwei .jar-Dateien im Ordner target erstellt:
Fourier-jar-with-dependencies.jar               -> Datei fuer die Fourieranalyse
Analyzing-jar-with-dependencies.jar             -> Datei, die nach der Fourieranalyse die Hauptfrequenzen berechnet.



Wenn sie die Fourieranalyse ausfuerhen moechten, dann verwenden Sie bitte die folgende Zeile:
java -jar <Pfad zur .jar-Datei in target> <Pfad zur .wav-Datei> <Blockgroesse>

Falls Sie eine spezifische Fourier-Funktion verwenden moechten:

java -jar <Pfad zur Fourier .jar-Datei in target> <Pfad zur .wav-Datei> <Blockgroesse> <Funktion>




Wenn Sie die Datei fuer die Hauptfrequenzen ausfuehren moechten, dann verwenden Sie den folgenden Befehl:
java -jar <Pfad zur Analyzing .jar-Datei in target>