# Maria Skłodowska-Curie – prezentacja

1. Otwórz `index.html` w przeglądarce (Chrome, Edge, Firefox, Safari). Działa offline, czcionki są w folderze `fonts`.
2. Sterowanie: **← →** (także spacja / PageUp / PageDown), **F** – pełny ekran, **I** – źródła materiałów, Home / End – pierwszy / ostatni slajd. Na telefonie: przesuwanie palcem.
3. Pobranie zdjęć i filmów z domeny publicznej (Wikimedia Commons, Internet Archive):
   ```
   python3 pobierz_media.py
   ```
   Skrypt zapisuje pliki w `media/` i tworzy `media/media.js` z autorami i licencjami. Jeśli masz ffmpeg, filmy zostaną przycięte do ok. 40 s.
4. Własne pliki: wrzuć do `media/` plik o nazwie `<id>.jpg` (zdjęcie) albo `<id>.webm` / `<id>.mp4` (film). Identyfikatory (`data-id`) są w `index.html` i w `pobierz_media.py`. Dopóki pliku nie ma, w tym miejscu widać placeholder „[tu film: …]” albo „[tu zdjęcie: …]”.
