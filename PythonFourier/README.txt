Sie muessen die Packages aus requirements.txt installieren, damit Sie das Skriop ausfuehren koennen.

Verwenden Sie dazu den folgenden Befehl: pip install -r requirements. txt





Starten des Programms:


python main.py ..\resources\nicht_zu_laut_abspielen_sehr_kurz.wav 1024




Falls Sie die Fehlermeldung "ImportError: libopenblas.so.0: cannot open shared object file or directory" bekommen, dann muessen sie diese Bibliothek installieren:
sudo apt-get install libopenblas-dev