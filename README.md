# File Manager

Project for subject "ASU": Warsaw University of Technology

Program do porządkowania plików w systemie Linux. Ma on za zadanie przeszukać główny katalog X razem z jego podkatalogami, oraz inne katalogi Y1, Y2, ... wraz z ich podkatalogami (o podobnej strukturze), a następnie uporządkować te katalogi w następujący sposób:
- w katalogu X znalazły się wszystkie pliki,
- zlikwidować duplikaty czyli sposród plików o identycznej zawartości zasugerować pozostawienie tylko najstarszego (nowsze daty są zapewne datami utworzenia kopii),
- zaproponować skasowanie plików pustych i tymczasowych,
- w przypadku plików o tej samej nazwie zasugerować pozostawienie nowszego,
- zasugerować ujednolicenie atrybutów np. rw-r–r–,
- zasugerować przemianowanie plików, których nazwy zawierają znaki mogące komplikować operowanie nimi (np. ’:’, ’”’, ’.’, ’;’, ’*’, ’?’, ’$’, ’#’, ’‘’, ’|’, ’\’, ...) zastępując te znaki zdefiniowanym substytutem np. _

Program potrafi wyszukiwać:
- pliki o identycznej zawartości (choć niekoniecznie identycznej nazwie i niekonieczne w analogicznej pozycji w drzewie),
- pliki puste,
- nowsze wersje plików o tej samej nazwie (choć niekoniecznie znajdujące się w analogicznym katalogu),
- pliki tymczasowe (*˜, *.tmp, ew. inne rozszerzenia zdefiniowane przez użytkownika),
- pliki o nietypwych atrybutach np. rwxrwxrwx,
- pliki o nazwach zawierających kłopotliwe znaki.

Dla każdego znalezionego pliku program proponuje odpowiednią akcję:
- skasowanie duplikatu, pliku pustego lub tymczasowego,
- zastąpienie starszej wersji nowszą (w przypadku plików z identyczną zawartością),
- zastapienie wersji nowszej starszą (w przypadku plików z identyczną zawartością),
- zmianę atrybutów,
- zmianę nazwy,
- pozostawienie bez zmian

## Uruchomienie

Aby uruchomić program należy mieć zainstalowanego Pythona w wersji 3.10 i za jego pomocą uruchomić skrypt main.py z następującymi parametrami
```
main.py [--temp_del] [--temp_keep] [--empty_del] [--empty_keep] [--bad_change] [--bad_keep] [--perm_change] [--perm_keep] [--same_action {old,new,none}] main_path [copy_paths ...]

gdzie:

main_path oznacza ścieżkę do folderu, w którym mają znaleźć się wszystkie pliki (korzeń głównego katalogu plików)
copy_paths to ścieżki do folderów, które program ma przeszukać dodatkowo (i w razie potrzeby przenieść z nich pliki do katalogu głównego)
--temp_del włącza permanentne usuwanie plików tymczasowych (bez pytania o zgodę użytkownika)
--temp_keep włącza permanentne zachowywanie plików tymczasowych (bez pytania o zgodę użytkownika)
--empty_del włącza permanentne usuwanie plików pustych (bez pytania o zgodę użytkownika)
--empty_keep włącza permanentne zachowywanie plików pustych (bez pytania o zgodę użytkownika)
--bad_change włącza permanentne zmienianie kłopotliwych nazw plików (bez pytania o zgodę użytkownika)
--bad_keep włącza permanentne zachowywanie kłopotliwych nazw plików (bez pytania o zgodę użytkownika)
--perm_change włącza permanentne zmienianie kłopotliwych atrybutów plików (bez pytania o zgodę użytkownika)
--perm_keep włącza permanentne zachowywanie kłopotliwych atrybutów plików (bez pytania o zgodę użytkownika)
--same_action oznacza akcję wykonywaną podczas znalezienia dwóch plików o takiej samej zawartości (old - usunięcie starszego, new - usunięcie nowszego, none - zachowanie obu)
```

## Konfiguracja
W pliku doc/clean_files znajduje się modyfikowalna konfiguracja programu tj.:
- permissions: sugerowana wartość atrybutów plików
- bad-characters: kłopotliwe znaki w nazwach plików
- substitute: substytut znaków kłopotliwych
- temporary-extensions: dodatkowe (do standardowych *.tmp i *~) rozszerzenia plików uznawanych tymczasowych
