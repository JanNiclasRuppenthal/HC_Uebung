Fuer das Java-Programm habe ich das Build-Tool Maven verwendet. Das macht die Sache fuer die Kompilierung einfacher. Um nun das Programm zu starten, muss man JAR-Dateien erstellen:
mvn clean package

Nach diesem Befehl werden zwei JAR-Dateien im Ordner target erstellt:
Fourier-jar-with-dependencies.jar           -> Datei fuer die Fourieranalyse
Analyzing-jar-with-dependencies.jar         -> Datei, die nach der Fourieranalyse die Hauptfrequenzen berechnet.


Die erste Datei kann die Fourieranalyse starten. Hierzu benoetigt man den folgenden Befehl:
java -jar .\target\Fourier-jar-with-dependencies.jar ..\resources\<Name der WAV-Datei> <Blockgroesse>


Wenn man nun eine spezifische Funktion fuer die Fourieranalyse verwenden moechte, dann muss man einen weiteren Parameter uebergeben:
java -jar .\target\Fourier-jar-with-dependencies.jar ..\resources\<Name der WAV-Datei> <Blockgroesse> <Funktion>

Hierbei gibt es zwei weitere Varianten, die man fuer den Parameter Funktion verwenden kann:
    -dft
    -rec_fft

Wenn kein Parameter fuer Funktion uebergeben wird, dann wird die implementierte FFT von org.apache.commons.math3.transform.FastFourierTransformer verwendet.



Die Datei Analyzing.java bzw. die JAR-Datei Analyzing-jar-with-dependencies.jar kann verwendet werden, um die Hauptfrequenzen ausgeben zu lassen. Um nun diese Datei zu starten, muss man den folgenden Befehl verwenden:
java -jar .\target\Analyzing-jar-with-dependencies.jar