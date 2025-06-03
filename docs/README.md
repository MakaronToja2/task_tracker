# System Zarządzania Zadaniami z Użytkownikami
## Dokumentacja Projektu

**Autor:** [Twoje Imię i Nazwisko]  
**Data:** Czerwiec 2025  
**Wersja:** 2.0  
**Technologie:** Python, FastAPI, SQLAlchemy, SQLite, Docker  

---

## Spis Treści

1. [Wymagania Funkcjonalne i Niefunkcjonalne](#1-wymagania-funkcjonalne-i-niefunkcjonalne)
2. [Opis Architektury](#2-Opis-architektury)
3. [Opis Sposobów i Metod Testowania](#3-opis-sposobów-i-metod-testowania)
4. [Implementacja](#4-implementacja)
5. [Instrukcje Uruchomienia](#5-instrukcje-uruchomienia)

---

## 1. Wymagania Funkcjonalne i Niefunkcjonalne

### 1.1 Wymagania Funkcjonalne

**RF01: Zarządzanie użytkownikami**
- System umożliwia utworzenie nowego użytkownika z unikalną nazwą i adresem email
- System waliduje poprawność danych użytkownika
- System wyświetla listę wszystkich użytkowników z liczbą ich zadań
- System umożliwia pobranie szczegółów konkretnego użytkownika

**RF02: Tworzenie zadań**
- System umożliwia użytkownikowi utworzenie nowego zadania z tytułem i opcjonalnym opisem
- System przypisuje zadanie do konkretnego użytkownika
- System sprawdza poprawność danych wejściowych
- System przypisuje unikalne ID do każdego zadania

**RF03: Przeglądanie zadań**
- System umożliwia wyświetlenie wszystkich zadań w systemie
- System umożliwia wyświetlenie zadań konkretnego użytkownika
- System wyświetla informacje: ID, tytuł, opis, status ukończenia, ID właściciela, data utworzenia

**RF04: Oznaczanie zadań jako ukończone**
- System umożliwia oznaczenie zadania jako ukończone przez jego właściciela
- System sprawdza uprawnienia użytkownika do modyfikacji zadania
- System uniemożliwia ponowne oznaczenie już ukończonego zadania

**RF05: Usuwanie zadań**
- System umożliwia usunięcie zadania przez jego właściciela
- System sprawdza uprawnienia użytkownika do usunięcia zadania
- System stosuje reguły biznesowe dotyczące usuwania

### 1.2 Wymagania Niefunkcjonalne

**RNF01: Wydajność**
- System odpowiada na żądania w czasie < 1 sekundy
- API zwraca dane w formacie JSON z minimalnymi opóźnieniami

**RNF02: Niezawodność**
- System zachowuje integralność danych za pomocą transakcji bazodanowych
- System zawiera mechanizmy odzyskiwania po awarii

**RNF03: Użyteczność**
- API jest samodokumentujące się (FastAPI automatyczna dokumentacja)
- Komunikaty o błędach są zrozumiałe dla użytkownika
- Interfejs REST API jest intuicyjny i zgodny ze standardami

**RNF04: Bezpieczeństwo**
- System waliduje wszystkie dane wejściowe
- System zabezpiecza przed atakami SQL Injection poprzez ORM
- System implementuje walidację na poziomie modelu danych
- System sprawdza uprawnienia do operacji na zadaniach

**RNF05: Skalowalność**
- Architektura wielowarstwowa umożliwia łatwe rozszerzanie funkcjonalności
- Separacja logiki biznesowej od warstwy danych
- Możliwość dodania nowych modułów bez modyfikacji istniejącego kodu
- Przygotowanie do containeryzacji i wdrożenia w chmurze

**RNF06: Maintainability**
- Kod jest dobrze udokumentowany i skomentowany
- Zastosowanie wzorców projektowych (Repository, Dependency Injection)
- Wysokie pokrycie kodu testami jednostkowymi i integracyjnymi
- Jasna struktura katalogów i organizacja kodu

### 1.3 Reguły Biznesowe

**RB01: Walidacja danych użytkownika**
- Nazwa użytkownika nie może być pusta i musi być unikalna w systemie
- Adres email musi mieć poprawny format i być unikalny w systemie
- Długość nazwy użytkownika: minimum 3, maksimum 50 znaków

**RB02: Walidacja zadań**
- Tytuł zadania nie może być pusty
- Tytuł zadania nie może przekraczać 100 znaków
- Zadanie musi być przypisane do istniejącego użytkownika

**RB03: Uprawnienia użytkownika**
- Tylko właściciel zadania może je modyfikować (oznaczać jako ukończone)
- Tylko właściciel zadania może je usunąć
- Administratorzy mogą przeglądać wszystkie zadania w systemie

**RB04: Ograniczenia operacyjne**
- Nie można usunąć zadania, które zostało oznaczone jako ukończone
- Nie można ponownie oznaczać ukończonego zadania jako ukończone
- Usunięcie użytkownika powoduje usunięcie wszystkich jego zadań (cascade delete)

### 2.1 Opis Architektury

**Wzorzec Architektoniczny: Layered Architecture (Architektura Warstwowa)**

System został zaprojektowany zgodnie z wzorcem architektury warstwowej, która zapewnia:
- Separację odpowiedzialności (Separation of Concerns)
- Luźne powiązanie między warstwami (Loose Coupling)
- Wysoką kohezję w obrębie warstw (High Cohesion)
- Łatwość testowania i utrzymania

**Warstwa Prezentacji (Presentation Layer)**
- **Odpowiedzialność:** Obsługa żądań HTTP, walidacja danych wejściowych, serializacja odpowiedzi
- **Klasy główne:** `UserRoutes`, `TaskRoutes`
- **DTOs:** `UserCreate`, `UserResponse`, `TaskCreate`, `TaskResponse`
- **Technologia:** FastAPI z automatyczną dokumentacją OpenAPI

**Warstwa Logiki Biznesowej (Business Layer)**
- **Odpowiedzialność:** Implementacja reguł biznesowych, walidacja, koordynacja operacji
- **Klasy główne:** `UserService`, `TaskService`
- **Wyjątki:** `UserValidationError`, `TaskValidationError`
- **Wzorce:** Service Pattern, Domain Logic Pattern

**Warstwa Dostępu do Danych (Data Access Layer)**
- **Odpowiedzialność:** Abstrakcja operacji bazodanowych, mapowanie obiektów
- **Klasy główne:** `UserRepository`, `TaskRepository`
- **Wzorce:** Repository Pattern, Data Access Object (DAO)
- **Technologia:** SQLAlchemy ORM

**Warstwa Modelu (Model Layer)**
- **Odpowiedzialność:** Definicja struktury danych, relacje między encjami
- **Klasy główne:** `User`, `Task`
- **Relacje:** One-to-Many (User → Task)
- **Technologia:** SQLAlchemy Models z automatyczną migracją

**Warstwa Bazy Danych (Database Layer)**
- **Odpowiedzialność:** Zarządzanie połączeniami, konfiguracja bazy danych
- **Klasy główne:** `DatabaseConnection`
- **Technologia:** SQLite (development), PostgreSQL (production ready)

### 3. Wzorce Projektowe Zastosowane

**1. Repository Pattern**
- Abstrakcja dostępu do danych
- Ułatwia testowanie przez możliwość mock-owania
- Centralizuje logikę zapytań bazodanowych

**2. Dependency Injection**
- Luźne powiązanie między warstwami
- Lepsze testowanie i maintainability
- Konfiguracja zależności przez FastAPI

**3. DTO (Data Transfer Object) Pattern**
- Separacja między obiektami domenowymi a API
- Kontrola nad tym, jakie dane są udostępniane
- Walidacja danych na poziomie API

**4. Service Pattern**
- Enkapsulacja logiki biznesowej
- Koordynacja operacji między różnymi repozytoriami
- Centraliczne miejsce dla reguł biznesowych

## 3. Opis Sposobów i Metod Testowania

### 3.1 Strategia Testowania

**Filozofia Testowania:**
System wykorzystuje podejście Test-Driven Development (TDD) i Testing Pyramid:

```
    E2E Tests (10%)
   ________________
  Integration Tests (20%)
 ________________________
Unit Tests (70%)
```

**Cele Testowania:**
- Zapewnienie poprawności logiki biznesowej
- Weryfikacja integracji między warstwami
- Walidacja zachowania API
- Utrzymanie wysokiej jakości kodu

### 3.2 Testy Jednostkowe (Unit Tests)

**Zakres:** Testowanie warstwy logiki biznesowej w izolacji

**Testowane Klasy:**
- `UserService` - logika zarządzania użytkownikami
- `TaskService` - logika zarządzania zadaniami

**Metodologia:**
- **Wzorzec AAA:** Arrange-Act-Assert
- **Mocking:** Użycie mock obiektów dla repozytoriów
- **Framework:** pytest z unittest.mock

**Technologie:**
- Framework: `pytest`
- HTTP Client: `TestClient` (FastAPI)
- Baza testowa: SQLite in-memory

### 3.2 Metryki Jakości

**Pokrycie Kodu (Code Coverage):**
- **Cel:** Minimum 90% pokrycia kodu
- **Warstwa Biznesowa:** 100% (krytyczna)
- **Warstwa API:** 95%
- **Warstwa Repository:** 85%

**Konwencje Testów:**
- Czytelne nazwy testów opisujące scenariusz
- Jeden test = jeden scenariusz biznesowy
- Wzorzec AAA we wszystkich testach
- Mock-owanie zależności zewnętrznych

**Narzędzia Jakości:**
```bash
# Pokrycie kodu
pytest --cov=. --cov-report=html --cov-fail-under=90

# Analiza statyczna kodu
flake8 --max-line-length=100
black --check .
mypy .
```

### 3.4 Testowanie Manualne

**API Documentation:**
- FastAPI automatycznie generuje dokumentację
- Dostępna pod adresem: `http://localhost:8000/docs`
- Umożliwia testowanie endpointów przez przeglądarkę

**Scenariusze testów manualnych:**
1. Utworzenie zadania z poprawnymi danymi
2. Próba utworzenia zadania z pustym tytułem
3. Próba utworzenia zadania z za długim tytułem
4. Ukończenie zadania
5. Próba usunięcia ukończonego zadania


### 3.4 Scenariusze Testowe End-to-End

**Scenariusz 1: Pełny cykl życia zadania**
1. Utwórz użytkownika
2. Utwórz zadanie dla użytkownika
3. Pobierz listę zadań użytkownika
4. Oznacz zadanie jako ukończone
5. Sprawdź czy zadanie nie może być usunięte (reguła biznesowa)

**Scenariusz 2: Walidacja uprawnień**
1. Utwórz dwóch użytkowników
2. Pierwszy użytkownik tworzy zadanie
3. Drugi użytkownik próbuje oznaczyć zadanie jako ukończone (powinno się nie udać)
4. Pierwszy użytkownik oznacza swoje zadanie jako ukończone (powinno się udać)

**Scenariusz 3: Walidacja reguł biznesowych**
1. Próba utworzenia użytkownika z pustą nazwą (błąd)
2. Próba utworzenia zadania z pustym tytułem (błąd)
3. Próba utworzenia zadania dla nieistniejącego użytkownika (błąd)


### 3.5 Testowanie Wydajności

**Load Testing:**
- Symulacja 100 równoczesnych użytkowników
- Testowanie endpoint-ów pod obciążeniem
- Monitorowanie czasu odpowiedzi

**Narzędzia:**
```bash
# Użycie locust dla testów obciążenia
pip install locust
locust -f performance_tests.py --host=http://localhost:8000
```

## 4. Implementacja

### 4.1 Struktura Projektu

```
task_manager/
├── main.py                    # Punkt wejścia aplikacji
├── requirements.txt           # Zależności Python
├── Dockerfile                # Konfiguracja Docker
├── docker-compose.yml        # Orchestracja kontenerów
├── models/
│   ├── __init__.py
│   ├── user.py               # Model użytkownika
│   └── task.py               # Model zadania
├── services/
│   ├── __init__.py
│   ├── user_service.py       # Logika biznesowa użytkowników
│   └── task_service.py       # Logika biznesowa zadań
├── repositories/
│   ├── __init__.py
│   ├── user_repository.py    # Dostęp do danych użytkowników
│   └── task_repository.py    # Dostęp do danych zadań
├── api/
│   ├── __init__.py
│   ├── user_routes.py        # Endpoint-y użytkowników
│   └── task_routes.py        # Endpoint-y zadań
├── database/
│   ├── __init__.py
│   └── connection.py         # Konfiguracja bazy danych
├── tests/
│   ├── __init__.py
│   ├── test_user_service.py  # Testy logiki użytkowników
│   ├── test_task_service.py  # Testy logiki zadań
│   ├── test_user_routes.py   # Testy API użytkowników
│   └── test_task_routes.py   # Testy API zadań
└── docs/
    ├── README.md             # Dokumentacja uruchomienia
    └── api_examples.md       # Przykłady użycia API
```

### 4.2 Technologie Wykorzystane

**Backend Framework:**
- **FastAPI 0.104.1** - Nowoczesny, szybki framework web
- **Pydantic** - Walidacja danych i serializacja
- **OpenAPI/Swagger** - Automatyczna dokumentacja API

**ORM i Baza Danych:**
- **SQLAlchemy 2.0.23** - Object-Relational Mapping
- **SQLite** - Baza danych (development)

**Testing Framework:**
- **pytest 7.4.3** - Framework testowy
- **httpx** - HTTP client for testing
- **unittest.mock** - Mocking dependencies

**DevOps i Deployment:**
- **Docker** - Konteneryzacja aplikacji
- **Docker Compose** - Orchestracja wielu kontenerów
- **Uvicorn** - ASGI server (development)

### 4.3 Kluczowe Funkcjonalności

**Zarządzanie Użytkownikami:**
- Rejestracja nowych użytkowników
- Walidacja unikalności nazwy i emaila
- Lista użytkowników z liczbą zadań

**Zarządzanie Zadaniami:**
- Tworzenie zadań z przypisaniem do użytkownika
- Listowanie zadań per użytkownik
- Oznaczanie zadań jako ukończone
- Usuwanie zadań z regułami biznesowymi

**API Features:**
- RESTful design
- JSON request/response
- Automatyczna walidacja danych
- Interaktywna dokumentacja
- Error handling z informacyjnymi komunikatami

## 5. Instrukcje Uruchomienia

### 5.1 Wymagania Systemowe

**Minimum Requirements:**
- Python 3.8 lub nowszy
- Docker 20.10+ i Docker Compose 2.0+

**Recommended:**
- Python 3.11
- Docker 24.0+

### 5.2 Uruchomienie Lokalne (bez Docker)

**Krok 1: Klonowanie repozytorium**
```bash
git clone https://github.com/MakaronToja/renovation_budget task_manager
cd task-manager
```

**Krok 2: Tworzenie środowiska wirtualnego**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
```

**Krok 3: Instalacja zależności**
```bash
pip install -r requirements.txt
```

**Krok 4: Uruchomienie aplikacji**
```bash
uvicorn main:app --reload
```

**Krok 5: Testowanie**
```bash
# Uruchomienie testów
pytest

# Testy z pokryciem kodu
pytest --cov=. --cov-report=html
```

### 5.3 Uruchomienie z Docker

**Development Mode:**
```bash
# Build i uruchomienie
docker-compose up --build

# W tle
docker-compose up -d --build

# Zatrzymanie
docker-compose down
```

### 5.4 Dostęp do Aplikacji

**Endpoints:**
- **API:** http://localhost:8000
- **Interactive Docs:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

**Przykłady Wywołań:**
```bash
# Status aplikacji
curl http://localhost:8000/

# Tworzenie użytkownika
curl -X POST "http://localhost:8000/api/users/" \
     -H "Content-Type: application/json" \
     -d '{"username": "testuser", "email": "test@example.com"}'

# Lista użytkowników
curl http://localhost:8000/api/users/

# Tworzenie zadania
curl -X POST "http://localhost:8000/api/tasks/" \
     -H "Content-Type: application/json" \
     -d '{"title": "Test Task", "user_id": 1}'
```