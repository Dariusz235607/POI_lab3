import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score



#Wczytanie danych z CSVki
def wczytaj_dane(sciezka='cechy_tekstur.csv'):
    df = pd.read_csv(sciezka)

    #podział danych na wartości(cechy) i etykiety(która tekstura)
    V = df.drop(columns=['kategoria']).values  #kolumny wartosci oprócz 'kategoria'
    etyk = df['kategoria'].values  #etykiety (tekstura1, tekstura2, itd.)

    return V, etyk


#Trenowanie i ocena modelu
def klasyfikuj_tekstury(V, etyk, test_size=0.2, random_state=42):
    #Podział zbioru na treningowy(80%) i testowy(20%)
    V_train, V_test, etyk_train, etyk_test = train_test_split(V, etyk, test_size=test_size, random_state=random_state)

    #inicjalizacja modelu (domyślnie SVM)
    model = SVC(kernel='linear')  #SVM basowy/liniowy

    #trenowanie modelu
    model.fit(V_train, etyk_train)

    #predykcja na zbiorze testowym
    etyk_pred = model.predict(V_test)

    #obliczenie dokładności
    dokladnosc = accuracy_score(etyk_test, etyk_pred)
    print(f"Dokładność klasyfikacji: {dokladnosc * 100:.2f}%")

    return model


if __name__ == "__main__":
    #wczytanie danych
    V, etyk = wczytaj_dane()

    #klasyfikacja i rezultat
    model = klasyfikuj_tekstury(V, etyk)