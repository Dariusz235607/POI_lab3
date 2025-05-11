import os
import cv2


def wycinaj_fragmenty(sciezka_zdjecia, sciezka_wycinki, rozmiar=128):
    """
    Wycinanie framgentów obrazu i zapisanie ich w folderze.

    Parametry:
    - sciezka_zdjecia: folder ze zdjeciami tekstury.
    - sciezka_wycinki: folder zapisu wycinków.
    - rozmiar: rozmiar wycinka, domyślnie 128x128
    """
    # Wczytanie obrazów
    obraz = cv2.imread(sciezka_zdjecia)
    if obraz is None:
        print(f"Błąd: Nie można wczytać obrazu {sciezka_zdjecia}")
        return

    #pobranie wymiarów obrazu
    wysokosc, szerokosc = obraz.shape[:2]

    #Obliczanie na ile kolumn i wierszy podzielić obraz
    liczba_kolumn = szerokosc // rozmiar
    liczba_wierszy = wysokosc // rozmiar

    #wycięcie i zapis wycinka
    numer_wycinka = 0
    for w in range(liczba_wierszy):
        for k in range(liczba_kolumn):
            #ustalenie współrzędnych aktualnie wycinanego wycinka obrazu
            y1 = w * rozmiar
            y2 = y1 + rozmiar
            x1 = k * rozmiar
            x2 = x1 + rozmiar

            #Wycięcie wycinka
            wycinek = obraz[y1:y2, x1:x2]

            # Zapisz fragment do pliku
            nazwa_pliku = f"fragment_{numer_wycinka}.jpg"
            sciezka_zapisu = os.path.join(sciezka_wycinki, nazwa_pliku)
            cv2.imwrite(sciezka_zapisu, wycinek)

            numer_wycinka += 1


def przetworz_tekstury(rozmiar=128):
    """
    użycie funkcji wycinania_fragmentów do wycięcia wycinków ze wszystkich 3 tekstur
    i zapisanie ich do 3 osobnych folderów
    """

    #Nazwy folderów ze zdjeciami tekstur
    foldery_tekstur = ["tekstura1", "tekstura2", "tekstura3"]

    for folder_tekstury in foldery_tekstur:
        # Sprawdź, czy folder z teksturami istnieje
        if not os.path.exists(folder_tekstury):
            print(f"Uwaga: Folder {folder_tekstury} nie istnieje. Pomijam lokalizacje...")
            continue

        #Utworzenie folderu na wycinki, jeśli nie istnieje
        folder_wycinkow = f"wycinki_{folder_tekstury}"
        if not os.path.exists(folder_wycinkow):
            os.makedirs(folder_wycinkow)

        print(f"Przetwarzanie tekstury: {folder_tekstury}...")

        #Przetwarzanie każdego obrazu w folderze
        for nazwa_zdjecia in os.listdir(folder_tekstury):
            sciezka_zdjecia = os.path.join(folder_tekstury, nazwa_zdjecia)

            #Pominięcie plików inne niż obrazy
            if not nazwa_zdjecia.lower().endswith(('.png', '.jpg', '.jpeg')):
                continue

            #Wycinanie fragmentów danego zdjęcia danej tekstury
            wycinaj_fragmenty(sciezka_zdjecia, folder_wycinkow, rozmiar)

    print("Wycinki zapisano w folderach 'wycinki_tekstura1/2/3'.")


if __name__ == "__main__":
    #uruchomienie funkcji przetwarzania 3 folderów ze zdjęciami
    #(która to korzysta z funkcji wycinania z pojedynczego obrazu)
    przetworz_tekstury()