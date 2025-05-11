import os       #biblioteka do interakcji z systemem operacyjnym
import cv2      #do przetwarzania obrazu
import numpy as np  #do obliczen
import pandas as pd #do analizy danych
from skimage.feature import graycomatrix, graycoprops   #do cech obrazu


def oblicz_cechy(obraz, odleglosci=[1, 3, 5], kierunki=[0, 45, 90, 135]):
    """
    Oblicza cechy tekstury na podstawie macierzy GLCM.

    Parametry:
    - obraz.
    - odległości pikseli (domyślnie [1, 3, 5]).
    - kąty kierunków (domyślnie [0, 45, 90, 135]).
    """

    #konwersja do skali szarości i kompresja z 8 do 5 bitów
    obraz_szary = cv2.cvtColor(obraz, cv2.COLOR_BGR2GRAY) #szarość
    obraz_szary = (obraz_szary // 4).astype(np.uint8)  #do 5 bit

    cechy = {} #stworzenie zestawu/slownika do zapisywania cech

    for d in odleglosci:
        for a in kierunki:
            #wygenerowanie macierzy współwystępowania szarości
            glcm = graycomatrix(obraz_szary, [d], [a], levels=64, symmetric=True)

            #obliczenie cech tekstur
            cechy[f'dissimilarity_{d}_{a}'] = graycoprops(glcm, 'dissimilarity')[0, 0]
            cechy[f'contrast_{d}_{a}'] = graycoprops(glcm, 'contrast')[0, 0]
            cechy[f'energy_{d}_{a}'] = graycoprops(glcm, 'energy')[0, 0]
            cechy[f'homogeneity_{d}_{a}'] = graycoprops(glcm, 'homogeneity')[0, 0]
            cechy[f'correlation_{d}_{a}'] = graycoprops(glcm, 'correlation')[0, 0]
            cechy[f'ASM_{d}_{a}'] = graycoprops(glcm, 'ASM')[0, 0]

    return cechy


def przetworz_wycinki():
    """
    Zbiera ,cechy' ze wszystkich wycinkow i zapisuje je do pliku CSV.
    """
    foldery_tekstur = ['wycinki_tekstura1', 'wycinki_tekstura2', 'wycinki_tekstura3']
    dane = [] #lista na przechowywanie cech

    for folder in foldery_tekstur:
        #pobierz rodzaj powierzchni (tekstura1, tekstura2, tekstura3)
        kategoria = folder.replace('wycinki_', '')
        print(f"Przetwarzanie: {kategoria}...")

        #przetwarzanie każdego wycinka z folderu
        for plik in os.listdir(folder):
            sciezka = os.path.join(folder, plik)

            #omijanie plików niebędących obrazami
            if not plik.lower().endswith(('.png', '.jpg', '.jpeg')):
                continue

            #wczytanie obrazu
            obraz = cv2.imread(sciezka)
            if obraz is None:
                print(f"Uwaga: Nie można wczytać {sciezka}. Pomijam...")
                continue

            #obliczanie cech tekstury
            cechy = oblicz_cechy(obraz)
            cechy['kategoria'] = kategoria
            dane.append(cechy)

    #zapisanie danych do pliku CSV
    if dane:
        df = pd.DataFrame(dane)
        df.to_csv('cechy_tekstur.csv', index=False)
        print("Zapisano cechy do pliku 'cechy_tekstur.csv'")
    else:
        print("Brak danych do zapisania!")


if __name__ == "__main__":
    przetworz_wycinki()