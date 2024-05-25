Um alle Dependencies zu installieren, benutzen Sie bitte: mvn install


Um die beiden Programm auszufuehren, benutzen sie bitte einer der beiden folgenden Befehle:

mvn clean compile exec:java@Fourier


oder


mvn clean compile exec:java@Analyzing


Sie haben auch die Moeglichkeit eine .jar ueber Maven zu erstellen:
mvn clean compile assembly:single

Wenn sie die .jar-Datei ausfuerhen moechten, dann verwenden Sie bitte die folgende Zeile:
java -jar <Pfad\zu\.jar-Datei> <Pfad zur .wav-Datei> <Blockgroesse>