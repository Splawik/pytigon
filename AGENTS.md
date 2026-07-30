# Instrukcje Projektowe (Kilo Code)

Projekt Pytigon napisany jest głównie w python, korzysta z Django. Szablony django zostały zastąpione przez szablony .ihtml. Cechą harakterystyczną tych szablonów jest to, że bazują na wcięciach kodu i są kompilowane do szablonów django.

Projekt Pytigon składa się z kilku części:
1. pytigon_lib (wnętrze projektu pytigon-lib), biblioteki pomocnicze system
2. pytigon - główna część systemu pytigon
3. pytigon_gui - gui do systemu Pytigon (wnętrze projektu pytigon-gui)
4. pytigon_standard_prj - przykładowe projekty systemu Pytigon (wnętrze projektu pytigon-standard-prj)
5. doc - dokumentacja systemu Pytigon
6. frontend - frontend systemu Pytigon, głównie pliki .sass dla css oraz .py kompilowane za pomocą pscript do plików .js

# Uruchamianie i testy
Projekt pytigon nie korzysta bezpośrednio z interpretera Python ale za pośrednictwem programu ptig. Aby uruchomić jakiś przykładowy projekt z folderu pytigon_standard_prj/prj należy użyć polecenia:
ptig manage_[[nazwa_projektu]] runserver
Aby uruchomić python użyj:
ptig python [[parametry]]

Aby uruchomić testy użyj polecenia:
ptig -m pytest lub ptig @pytest (@ zastępuje -m)

Aby zarządzać projektem uruchom:
ptig manage_[[nazwa_projektu]] [[polecenie]] 
gdzie polecenie jest to samo jak przy wywołaniu python manage.py

Plik settings dla projektu znajduje się w folderze projektu pod nazwą: settings_app.py, np dla projektu schdevtools jest to:
pytigon_standard_prj/prj/schdevtools/settings_app.py


## Architektura i Zasady
* Projekty w folderze pytigon_standard_prj/prj mają swoje odpowiedniki w postaci plików w formacie .ptigprj umieszczonych w folderze pytigon/install. Z plików .ptigprj generowane są projekty django. W związku z tym nie zmieniaj plikow w pytigon_standard_prj bezpośrednio lecz za pomocą ich źródłowych plików .ptigprj.

* Testy wykonuj w folderach:
bieżącym, ../pytigon-lib, ../pytigon-gui
Możesz użyć: "ptig @pytest" tests/ lub "make test"

* Zwróć uwagę na shell, w którym będziesz pracował. Może się okazać że działasz w xonsh a nie bash.
