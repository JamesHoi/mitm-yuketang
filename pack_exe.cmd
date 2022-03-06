pyinstaller -F --add-data=listener.py;. --add-data=cacert.pem;certifi --exclude-module PyQt5 main.py
pyinstaller -F --exclude-module PyQt5 gen_cert.py