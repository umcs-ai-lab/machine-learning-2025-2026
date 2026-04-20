# pip install opencv-python mediapipe numpy

# Importujemy bibliotekę OpenCV.
# To ona pozwala nam korzystać z kamery, obrabiać obraz i wyświetlać okno z podglądem.
import cv2

# Importujemy moduł math.
# Przyda się do policzenia odległości między dwoma punktami.
import math

# Importujemy moduł time.
# Dzięki niemu możemy sprawdzać czas i nie wysyłać komendy zmiany głośności zbyt często.
import time

# Importujemy subprocess.
# To narzędzie pozwala uruchamiać polecenia systemowe z poziomu Pythona.
# U nas będzie potrzebne do wywołania AppleScript przez "osascript".
import subprocess

# Importujemy numpy i nadajemy mu skróconą nazwę "np".
# Numpy bardzo dobrze radzi sobie z liczbami i mapowaniem wartości.
import numpy as np

# Importujemy bibliotekę MediaPipe.
# To ona rozpoznaje dłoń i wskazuje pozycje palców.
import mediapipe as mp


# Tworzymy funkcję do ustawiania głośności na macOS.
# "def" oznacza: definiuję własną funkcję.
def set_macos_volume(vol: int) -> None:
    # Pilnujemy, żeby głośność nie zeszła poniżej 0 i nie weszła powyżej 100.
    # int(vol) zamienia wartość na liczbę całkowitą.
    vol = max(0, min(100, int(vol)))

    # Budujemy tekst polecenia dla AppleScript.
    # Przykład końcowy może wyglądać tak:
    # "set volume output volume 35"
    script = f"set volume output volume {vol}"

    # Uruchamiamy polecenie systemowe:
    # osascript -e "set volume output volume 35"
    # check=False oznacza: nie wywalaj błędu programu, nawet jeśli komenda się nie uda.
    # capture_output=True oznacza: przechwyć odpowiedź programu, zamiast wypisywać ją w terminalu.
    subprocess.run(["osascript", "-e", script], check=False, capture_output=True)


# Tworzymy funkcję do odczytu aktualnej głośności z macOS.
def get_macos_volume() -> int:
    # To polecenie AppleScript zwraca aktualny poziom głośności wyjściowej.
    script = "output volume of (get volume settings)"

    # Uruchamiamy polecenie systemowe.
    # text=True oznacza, że wynik chcemy dostać jako zwykły tekst, a nie bajty.
    result = subprocess.run(
        ["osascript", "-e", script],
        check=False,
        capture_output=True,
        text=True
    )

    # Próbujemy zamienić odpowiedź z systemu na liczbę całkowitą.
    try:
        return int(result.stdout.strip())

    # Jeżeli coś pójdzie nie tak, na wszelki wypadek zwracamy 50.
    except Exception:
        return 50


# Tworzymy pomocniczą funkcję "clamp".
# Ona "przycina" wartość do zadanego zakresu.
# Przykład:
# clamp(120, 0, 100) da 100
# clamp(-5, 0, 100) da 0
def clamp(value, lo, hi):
    # Najpierw sprawdzamy, czy wartość nie jest za mała,
    # a potem czy nie jest za duża.
    return max(lo, min(hi, value))


# Tworzymy funkcję "lerp", czyli łagodne przejście od jednej wartości do drugiej.
# To nam wygładzi skoki głośności.
def lerp(a, b, t):
    # Matematycznie:
    # gdy t = 0, wynik to a
    # gdy t = 1, wynik to b
    # gdy t = 0.25, jesteśmy trochę bliżej b niż a
    return a + (b - a) * t


# Tworzymy skrót do modułu "hands" z MediaPipe.
# Dzięki temu nie musimy później pisać całej długiej ścieżki.
mp_hands = mp.solutions.hands

# Tworzymy skrót do narzędzi rysujących z MediaPipe.
# To posłuży do rysowania punktów dłoni i połączeń między nimi.
mp_draw = mp.solutions.drawing_utils

# Tworzymy obiekt odpowiedzialny za wykrywanie dłoni.
hands = mp_hands.Hands(
    # static_image_mode=False oznacza:
    # traktuj obraz jako wideo, a nie pojedyncze niezależne zdjęcia.
    # To jest lepsze do pracy z kamerą.
    static_image_mode=False,

    # max_num_hands=1 oznacza:
    # szukamy maksymalnie jednej dłoni.
    # Dzięki temu program jest trochę prostszy i szybszy.
    max_num_hands=1,

    # model_complexity=1 oznacza:
    # używamy średnio dokładnego modelu.
    # Zwykle to sensowny kompromis między szybkością a jakością.
    model_complexity=1,

    # min_detection_confidence=0.7 oznacza:
    # model musi być pewny wykrycia dłoni przynajmniej na 70%.
    min_detection_confidence=0.7,

    # min_tracking_confidence=0.7 oznacza:
    # śledzenie dłoni między klatkami też musi mieć pewność minimum 70%.
    min_tracking_confidence=0.7,
)


# Otwieramy kamerę.
# "0" zwykle oznacza pierwszą, domyślną kamerę w komputerze.
cap = cv2.VideoCapture(0)

# Sprawdzamy, czy kamera faktycznie się otworzyła.
if not cap.isOpened():
    # Jeśli nie, przerywamy program i pokazujemy błąd.
    raise RuntimeError("Nie mogę otworzyć kamery.")


# Ustawiamy szerokość obrazu z kamery na 960 pikseli.
# Mniejsza rozdzielczość = często lepsza płynność działania.
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 960)

# Ustawiamy wysokość obrazu z kamery na 540 pikseli.
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 540)


# Odczytujemy aktualną głośność systemu i zapisujemy ją jako punkt startowy.
current_volume = get_macos_volume()

# Zmienna do wygładzania.
# Na początku ustawiamy ją na aktualną głośność.
smoothed_target = float(current_volume)

# Zmienna przechowująca ostatnią głośność, którą faktycznie wysłaliśmy do systemu.
last_sent_volume = current_volume

# Zmienna przechowująca czas ostatniego wysłania komendy.
# Na starcie ustawiamy 0.0.
last_send_time = 0.0


# Ustalamy minimalny dystans między palcami, który uznamy za 0% głośności.
MIN_DIST = 25

# Ustalamy maksymalny dystans między palcami, który uznamy za 100% głośności.
MAX_DIST = 180


# Określamy, jak często maksymalnie wolno wysyłać komendę do systemu.
# 0.08 sekundy to 80 milisekund.
SEND_INTERVAL = 0.08

# Określamy minimalną zmianę głośności, przy której wyślemy nową wartość.
# Dzięki temu nie reagujemy na każdą drobną różnicę o 1%.
MIN_STEP_TO_SEND = 2


# Wypisujemy informację do terminala.
print("Start. Naciśnij Q, aby zakończyć.")


# Zaczynamy pętlę nieskończoną.
# Program będzie działał cały czas, dopóki go nie przerwiemy.
while True:
    # Pobieramy jedną klatkę z kamery.
    # "ok" mówi, czy operacja się udała.
    # "frame" to sam obraz.
    ok, frame = cap.read()

    # Jeśli nie udało się pobrać obrazu, kończymy pętlę.
    if not ok:
        break

    # Odbijamy obraz w poziomie.
    # Dzięki temu zachowuje się jak lustro:
    # ruszasz prawą ręką w prawo i na ekranie też idzie w prawo.
    frame = cv2.flip(frame, 1)

    # Pobieramy wysokość i szerokość obrazu.
    # "_" oznacza, że trzecią wartość (liczbę kanałów koloru) ignorujemy.
    h, w, _ = frame.shape

    # Zamieniamy obraz z formatu BGR na RGB.
    # OpenCV czyta obraz jako BGR, a MediaPipe oczekuje RGB.
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Przekazujemy obraz do MediaPipe, żeby wykrył dłoń.
    result = hands.process(rgb)

    # Sprawdzamy, czy MediaPipe znalazł jakąś dłoń.
    if result.multi_hand_landmarks:
        # Bierzemy pierwszą wykrytą dłoń.
        hand_landmarks = result.multi_hand_landmarks[0]

        # Rysujemy na obrazie punkty dłoni i linie między nimi.
        mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        # Pobieramy punkt końcówki kciuka.
        # W MediaPipe punkt o numerze 4 to czubek kciuka.
        thumb = hand_landmarks.landmark[4]

        # Pobieramy punkt końcówki palca wskazującego.
        # W MediaPipe punkt o numerze 8 to czubek wskazującego.
        index = hand_landmarks.landmark[8]

        # Zamieniamy współrzędne kciuka z ułamków na piksele ekranu.
        x1, y1 = int(thumb.x * w), int(thumb.y * h)

        # Zamieniamy współrzędne palca wskazującego z ułamków na piksele ekranu.
        x2, y2 = int(index.x * w), int(index.y * h)

        # Liczymy środek odcinka między palcami.
        # To tylko do ładniejszego rysowania.
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        # Liczymy odległość między palcami.
        # math.hypot liczy długość odcinka między punktami.
        dist = math.hypot(x2 - x1, y2 - y1)

        # Rysujemy zielone kółko na końcówce kciuka.
        cv2.circle(frame, (x1, y1), 10, (0, 255, 0), -1)

        # Rysujemy zielone kółko na końcówce wskazującego.
        cv2.circle(frame, (x2, y2), 10, (0, 255, 0), -1)

        # Rysujemy linię między palcami.
        cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 255), 3)

        # Rysujemy czerwone kółko na środku tej linii.
        cv2.circle(frame, (cx, cy), 8, (0, 0, 255), -1)

        # Zamieniamy dystans palców na głośność od 0 do 100.
        # np.interp robi "mapowanie":
        # MIN_DIST -> 0
        # MAX_DIST -> 100
        # wartości pomiędzy też zostają proporcjonalnie przeliczone
        raw_volume = np.interp(dist, [MIN_DIST, MAX_DIST], [0, 100])

        # Dodatkowo pilnujemy zakresu 0-100.
        raw_volume = clamp(raw_volume, 0, 100)

        # Wygładzamy wynik, żeby głośność nie skakała jak szalona.
        # smoothed_target przesuwa się trochę w stronę raw_volume.
        smoothed_target = lerp(smoothed_target, raw_volume, 0.25)

        # Zaokrąglamy wygładzoną wartość do pełnego procenta.
        target_volume = int(round(smoothed_target))

        # Zamieniamy głośność na pozycję paska na ekranie.
        # Gdy głośność = 0, pasek ma być nisko.
        # Gdy głośność = 100, pasek ma być wysoko.
        bar_y = int(np.interp(target_volume, [0, 100], [400, 100]))

        # Rysujemy obramowanie paska głośności.
        cv2.rectangle(frame, (40, 100), (80, 400), (200, 200, 200), 2)

        # Wypełniamy pasek zielonym kolorem do odpowiedniej wysokości.
        cv2.rectangle(frame, (40, bar_y), (80, 400), (0, 255, 0), -1)

        # Wypisujemy obok aktualną głośność jako tekst, np. "63%".
        cv2.putText(frame, f"{target_volume}%", (30, 450),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

        # Pobieramy aktualny czas.
        now = time.time()

        # Sprawdzamy dwa warunki:
        # 1) czy zmiana głośności jest wystarczająco duża,
        # 2) czy minęło już trochę czasu od ostatniego wysłania komendy.
        if (
            abs(target_volume - last_sent_volume) >= MIN_STEP_TO_SEND
            and (now - last_send_time) >= SEND_INTERVAL
        ):
            # Jeśli warunki są spełnione, ustawiamy nową głośność systemu.
            set_macos_volume(target_volume)

            # Zapamiętujemy właśnie wysłaną głośność.
            last_sent_volume = target_volume

            # Zapamiętujemy czas wysłania komendy.
            last_send_time = now

        # Wyświetlamy na ekranie dystans między palcami w pikselach.
        cv2.putText(frame, f"Dist: {int(dist)} px", (100, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    # Ten blok wykona się, jeśli dłoń NIE została wykryta.
    else:
        # Pokazujemy komunikat dla użytkownika.
        cv2.putText(frame, "Pokaz dlon do kamery", (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 200, 255), 2)

    # Niezależnie od wszystkiego pokazujemy na dole informację o wyjściu z programu.
    cv2.putText(frame, "Q = wyjscie", (20, h - 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (180, 180, 180), 2)

    # Wyświetlamy gotową klatkę w oknie o podanej nazwie.
    cv2.imshow("Hand Volume Control - macOS", frame)

    # Czekamy 1 milisekundę na naciśnięcie klawisza.
    # cv2.waitKey zwraca kod klawisza.
    # "& 0xFF" pomaga poprawnie odczytać ten kod na różnych systemach.
    key = cv2.waitKey(1) & 0xFF

    # Jeśli użytkownik nacisnął klawisz "q", kończymy pętlę.
    if key == ord("q"):
        break


# Zwalniamy kamerę, żeby system wiedział, że już z niej nie korzystamy.
cap.release()

# Zamykamy wszystkie okna OpenCV.
cv2.destroyAllWindows()

# Zwalniamy zasoby MediaPipe.
hands.close()