# Zadanie zaliczeniowe z przedmiotu „Uczenie maszynowe”

## Temat zadania

**Raport dotyczący wybranego algorytmu uczenia maszynowego**

## Cel zadania

Celem zadania jest przygotowanie krótkiego raportu opisującego jeden wybrany algorytm uczenia maszynowego. Zadanie ma na celu sprawdzenie, czy osoba studiująca:

- rozumie podstawową ideę działania wybranego algorytmu,
- potrafi wskazać jego możliwe zastosowania,
- umie wyjaśnić, jakiego typu dane mogą zostać wykorzystane w przykładowym problemie uczenia maszynowego.

Zadanie **nie wymaga implementacji algorytmu w języku Python**. Najważniejsze jest przedstawienie algorytmu własnymi słowami, w sposób uporządkowany, zrozumiały i odnoszący się do konkretnego przykładu zastosowania.

## Zakres zadania

Należy przygotować raport o długości około **2–3 stron** dotyczący jednego wybranego algorytmu uczenia maszynowego.

Można wybrać między innymi jeden z następujących algorytmów:

- *k-nearest neighbors*, czyli algorytm k najbliższych sąsiadów,
- drzewo decyzyjne,
- regresję liniową,
- regresję logistyczną,
- naiwny klasyfikator Bayesa,
- maszynę wektorów nośnych,
- las losowy,
- *gradient boosting*,
- sieć neuronową,
- *k-means*,
- PCA, czyli analizę głównych składowych.

Dopuszczalne jest również wybranie innego algorytmu uczenia maszynowego, pod warunkiem że zostanie on poprawnie opisany i powiązany z konkretnym przykładem zastosowania.

---

# Wymagana struktura raportu

Raport powinien zawierać następujące części.

## 1. Wprowadzenie

W tej części należy krótko przedstawić wybrany algorytm. Należy wyjaśnić, czym jest dany algorytm oraz do jakiego rodzaju problemów może być wykorzystywany.

W szczególności należy odpowiedzieć na pytania:

- czy algorytm służy do klasyfikacji, regresji, grupowania, redukcji wymiarowości lub innego zadania,
- jakie problemy może pomagać rozwiązywać,
- w jakich obszarach może być stosowany w praktyce.

## 2. Ogólna intuicja działania algorytmu

W tej części należy opisać ogólną zasadę działania algorytmu. Opis powinien być napisany własnymi słowami i nie musi zawierać szczegółowego zapisu matematycznego.

Należy wyjaśnić, w jaki sposób algorytm „uczy się” na podstawie danych oraz jak podejmuje decyzję dla nowych przykładów.

W zależności od wybranego algorytmu można opisać na przykład:

- w jaki sposób algorytm porównuje nowe przypadki z wcześniejszymi przykładami,
- jak tworzy reguły decyzyjne,
- jak dopasowuje linię lub granicę decyzyjną,
- jak dzieli dane na grupy,
- jak łączy wiele prostszych modeli w jeden bardziej złożony model.

## 3. Przykład zastosowania

Należy przedstawić jeden konkretny przykład zastosowania wybranego algorytmu.

Przykład powinien być opisany możliwie konkretnie. Należy wskazać, jaki problem miałby zostać rozwiązany oraz jaki wynik miałby zwracać model.

Przykładowe obszary zastosowań:

- rozpoznawanie obrazów,
- klasyfikacja wiadomości jako spam lub nie-spam,
- przewidywanie wyniku testu lub egzaminu,
- analiza zachowania użytkownika,
- rozpoznawanie emocji,
- przewidywanie ceny,
- analiza danych medycznych,
- rekomendowanie treści,
- grupowanie podobnych osób, tekstów lub zachowań.

## 4. Dane potrzebne do działania modelu

W tej części należy opisać, jakiego rodzaju dane byłyby potrzebne w zaproponowanym przykładzie.

Należy wskazać:

- co byłoby danymi wejściowymi,
- co byłoby oczekiwanym wynikiem modelu,
- czy problem dotyczy klasyfikacji, regresji, grupowania lub innego rodzaju zadania,
- jak mógłby wyglądać pojedynczy przykład w zbiorze danych.

Można dodać prostą tabelę z przykładowymi danymi. Tabela nie musi zawierać prawdziwych danych — może być przykładem pokazującym, jakiego typu informacje mogłyby zostać wykorzystane.

Przykład:

| Osoba | Czas reakcji | Liczba błędów | Wynik |
|---|---:|---:|---|
| A | 250 ms | 1 | brak zmęczenia |
| B | 620 ms | 7 | zmęczenie |
| C | 410 ms | 3 | ? |

W takim przypadku zadaniem modelu mogłoby być przewidzenie, czy osoba C jest zmęczona na podstawie wcześniejszych przykładów.

## 5. Najważniejsze parametry algorytmu

Należy wskazać wybrane parametry algorytmu, które mogą wpływać na jego działanie.

Nie trzeba omawiać wszystkich możliwych parametrów. Wystarczy opisać kilka najważniejszych i wyjaśnić, co mogą zmieniać w działaniu modelu.

Przykłady:

- dla *k-nearest neighbors*: liczba sąsiadów `k`,
- dla drzewa decyzyjnego: maksymalna głębokość drzewa,
- dla regresji logistycznej: parametr regularyzacji,
- dla lasu losowego: liczba drzew,
- dla *gradient boosting*: liczba estymatorów i szybkość uczenia,
- dla sieci neuronowej: liczba warstw, liczba neuronów, funkcja aktywacji.

## 6. Zalety i ograniczenia algorytmu

W tej części należy wskazać najważniejsze zalety oraz ograniczenia wybranego algorytmu.

Należy rozważyć między innymi:

- czy algorytm jest łatwy do zrozumienia,
- czy jego decyzje są łatwe do wyjaśnienia,
- czy wymaga dużej liczby danych,
- czy może być podatny na błędy,
- w jakich sytuacjach może działać dobrze,
- w jakich sytuacjach może działać gorzej.

## 7. Podsumowanie

Na końcu raportu należy krótko podsumować najważniejsze informacje.

Podsumowanie powinno zawierać odpowiedzi na pytania:

- czego dotyczył opisany algorytm,
- do jakiego problemu został zastosowany w przykładzie,
- dlaczego ten algorytm może być użyteczny,
- jakie są jego główne ograniczenia.

---

# Wymagania formalne

Raport powinien mieć długość około **2–3 stron**.

Raport należy przygotować w jednym z następujących formatów:

- `.docx`,
- `.pdf`,
- `.md`.

Tekst powinien być napisany samodzielnie, w sposób uporządkowany i zrozumiały. Należy unikać kopiowania definicji bez wyjaśnienia ich własnymi słowami.

W przypadku korzystania ze źródeł zewnętrznych należy podać je na końcu raportu. Źródłami mogą być na przykład:

- dokumentacja biblioteki `scikit-learn`,
- materiały dydaktyczne,
- podręczniki,
- artykuły naukowe lub popularnonaukowe,
- inne wiarygodne opracowania.

Przygotowany raport należy przesłać na adres mailowy: **michal.maj@mail.umcs.pl**.

---

# Korzystanie z narzędzi AI

Dopuszczalne jest korzystanie z narzędzi AI jako pomocy w przygotowaniu raportu, na przykład do:

- uporządkowania tekstu,
- wyjaśnienia pojęć,
- poprawy stylu językowego,
- sprawdzenia czytelności wypowiedzi.

Oddany raport powinien jednak świadczyć o zrozumieniu tematu przez osobę studiującą. W szczególności raport powinien zawierać:

- własny przykład zastosowania algorytmu,
- wyjaśnienie, jakiego typu dane byłyby potrzebne w tym przykładzie,
- opis działania algorytmu napisany własnymi słowami.

Nie należy oddawać tekstu składającego się wyłącznie z ogólnych definicji wygenerowanych automatycznie.

---

# Kryteria oceny

Raport będzie oceniany według następujących kryteriów:

| Kryterium | Waga | Opis |
|---|---:|---|
| Zrozumienie algorytmu | 40% | Oceniane będzie, czy wybrany algorytm został opisany poprawnie i zrozumiale. Ważne jest przedstawienie ogólnej intuicji działania algorytmu, a nie tylko podanie formalnej definicji. |
| Przykład zastosowania | 25% | Oceniane będzie, czy raport zawiera konkretny i sensowny przykład użycia algorytmu. Przykład powinien być powiązany z opisanym algorytmem i jasno pokazywać, jaki problem miałby zostać rozwiązany. |
| Opis danych | 20% | Oceniane będzie, czy osoba przygotowująca raport potrafi wskazać, jakiego rodzaju dane byłyby potrzebne do zastosowania algorytmu. Ważne jest rozróżnienie danych wejściowych oraz oczekiwanego wyniku modelu. |
| Przejrzystość i uporządkowanie raportu | 15% | Oceniana będzie struktura tekstu, poprawność językowa, czytelność oraz logiczne uporządkowanie treści. |

---

# Uwagi końcowe

Celem zadania nie jest szczegółowe matematyczne omówienie algorytmu ani jego implementacja programistyczna.

Najważniejsze jest pokazanie, że osoba studiująca:

- rozumie podstawową ideę działania wybranego algorytmu uczenia maszynowego,
- potrafi wskazać jego możliwe zastosowanie,
- umie opisać dane potrzebne do rozwiązania przykładowego problemu.
