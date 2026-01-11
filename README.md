# System Obecności z Rozpoznawaniem Twarzy

System do automatycznego rejestrowania obecności za pomocą rozpoznawania twarzy.

## Wymagania

- Python 3.10 lub 3.11 (zalecane) – **Python 3.12+ może powodować problemy**
- Kamera internetowa
- Przeglądarka z obsługą JavaScript
- System Windows (testowano), Linux/macOS (nie testowano)

## Instalacja (Windows)

### Krok 1: Zainstaluj Python

1. Pobierz [Python 3.10 lub 3.11](https://www.python.org/downloads/)
2. Podczas instalacji zaznacz **"Add Python to PATH"**

> ⚠️ **Uwaga:** Python 3.13 może powodować problemy z kompatybilnością bibliotek.

### Krok 2: Zainstaluj Visual Studio Build Tools

Wymagane do kompilacji biblioteki dlib (face_recognition).

1. Pobierz [Visual Studio Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
2. Uruchom instalator
3. Wybierz **"Desktop development with C++"**
4. W panelu "Installation details" (po prawej) zostaw tylko:
   - ✅ MSVC v143 - VS 2022 C++ x64/x86 build tools
   - ✅ Windows 10/11 SDK
5. Zainstaluj i **uruchom ponownie komputer**

### Krok 3: Zainstaluj CMake (opcjonalnie)

CMake jest wymagany do kompilacji dlib. Zazwyczaj instaluje się automatycznie z requirements.txt, ale jeśli wystąpią błędy:

1. Pobierz [CMake](https://cmake.org/download/)
2. Podczas instalacji zaznacz **"Add CMake to PATH"**

Lub zainstaluj przez pip (po utworzeniu środowiska wirtualnego):

```bash
pip install cmake
```

### Krok 4: Sklonuj repozytorium

```bash
git clone https://github.com/metadreamm/face-recognition-attendance-system
cd face-recognition-attendance-system
```

### Krok 5: Utwórz środowisko wirtualne

```bash
python -m venv venv
```

```bash
venv\Scripts\activate
```

Po aktywacji zobaczysz `(venv)` na początku wiersza poleceń.

### Krok 6: Zainstaluj zależności

```bash
pip install --upgrade pip
```

```bash
pip install -r requirements.txt
```

> ⏱️ Instalacja może potrwać 5-15 minut (kompilacja dlib).

#### Jeśli wystąpią błędy z requirements.txt:

Spróbuj zainstalować zależności bez sztywnych wersji:

```bash
pip install Flask Flask-SQLAlchemy Flask-Login SQLAlchemy Werkzeug setuptools opencv-python face-recognition numpy Pillow python-dotenv
```

### Krok 7: Uruchom aplikację

```bash
python run.py
```

### Krok 8: Otwórz w przeglądarce

```
http://127.0.0.1:5000
```

**Dane logowania:** `admin` / `admin123`

---

## Rozwiązywanie problemów

### "Microsoft Visual C++ 14.0 or greater is required"

→ Zainstaluj Visual Studio Build Tools (Krok 2)

### "CMake must be installed"

→ Uruchom: `pip install cmake`

### "No module named 'face_recognition'"

→ Uruchom: `pip install face_recognition --no-cache-dir`

### "No module named 'dotenv'"

→ Uruchom: `pip install python-dotenv`

### Błędy z SQLAlchemy na Python 3.13

→ Uruchom: `pip install SQLAlchemy>=2.0.30 --upgrade`

### Ostrzeżenie "pkg_resources is deprecated"

→ Można zignorować – nie wpływa na działanie aplikacji.

---

## Instalacja (Linux – nie testowano)

```bash
sudo apt update
sudo apt install python3-venv python3-dev cmake build-essential
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python run.py
```

---

## Instalacja (macOS – nie testowano)

```bash
brew install cmake python@3.11
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python run.py
```

---

## Funkcje

- ✅ Rejestracja osób ze zdjęciem referencyjnym (kamera lub plik)
- ✅ Rozpoznawanie twarzy z kamery w czasie rzeczywistym
- ✅ Automatyczne rejestrowanie obecności
- ✅ Zapobieganie wielokrotnej rejestracji w tym samym dniu
- ✅ Historia obecności z filtrowaniem po dacie
- ✅ Raporty: dzienne, miesięczne, indywidualne (CSV)
- ✅ Panel administracyjny chroniony logowaniem

---

## Struktura projektu

```
├── app/                 # Logika aplikacji
│   ├── __init__.py      # Fabryka aplikacji Flask
│   ├── models.py        # Modele bazy danych
│   └── routes.py        # Endpointy API i widoki
├── templates/           # Szablony HTML (Jinja2)
├── static/              # Pliki statyczne (CSS)
├── known_faces/         # Zdjęcia referencyjne osób
├── database/            # Baza danych SQLite
├── config.py            # Konfiguracja aplikacji
├── requirements.txt     # Zależności Python
└── run.py               # Punkt wejścia aplikacji
```

---

## Technologie

- **Flask** – Python web framework
- **SQLAlchemy + SQLite** – baza danych
- **face_recognition + dlib** – rozpoznawanie twarzy (algorytm HOG)
- **Bootstrap 5** – interfejs użytkownika
- **JavaScript** – obsługa kamery (MediaDevices API)
