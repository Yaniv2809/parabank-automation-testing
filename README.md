<p align="center">
  <img src="parabank_logo_automation_project.png" alt="ParaBank Automation Framework" width="800"/>
</p>

# ParaBank Automation Framework

> Multi-layer QA automation for the [ParaBank](https://parabank.parasoft.com/parabank/) simulated banking system —  
> UI · API · E2E · DB integrity tests, powered by **TestAxiom** · **FixtureForge** · **Failscope**

[![CI](https://github.com/Yaniv2809/parabank-automation-testing/actions/workflows/playwright_tests.yml/badge.svg)](https://github.com/Yaniv2809/parabank-automation-testing/actions/workflows/playwright_tests.yml)
[![Python 3.13](https://img.shields.io/badge/python-3.13-blue.svg)](https://www.python.org/)
[![Playwright](https://img.shields.io/badge/playwright-latest-green.svg)](https://playwright.dev/)
[![pytest](https://img.shields.io/badge/pytest-9.x-orange.svg)](https://pytest.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

| | Link |
|---|---|
| 📊 **Allure Report** | [yaniv2809.github.io/parabank-automation-testing](https://yaniv2809.github.io/parabank-automation-testing/) |
| 📋 **Test Plan (STP)** | [yaniv2809.github.io/parabank-automation-testing/test-plan.html](https://yaniv2809.github.io/parabank-automation-testing/test-plan.html) |

---

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Test Cases](#test-cases)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Quick Start](#quick-start)
- [Running Tests](#running-tests)
- [CI/CD Pipeline](#cicd-pipeline)
- [Custom Libraries](#custom-libraries)

---

## Overview

This framework validates **data integrity and behavioral consistency** across all layers of the ParaBank banking application. Every test case maps directly to the [Test Plan v1.0](Parabank_Test_Plan_v1.0.html) and covers login, account management, fund transfers, loan requests, and user registration.

**CI environment:** `parasoft/parabank` Docker image — isolated, always available, seeded via `POST /services/bank/initializeDB`  
**Local default:** `https://parabank.parasoft.com/parabank/` (override with `PARABANK_BASE_URL`)  
**Default credentials:** `john / demo`

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│  UI Layer       Playwright + Page Object Model                  │
│  API Layer      requests + BankAPIClient                        │
│  E2E Layer      UI action → API verify → DB confirm             │
│  DB Layer       SQLite (local Docker) / API proxy (public)      │
└─────────────────────────────────────────────────────────────────┘
```

### Test Design Techniques

| Technique | Tool | Applied To |
|---|---|---|
| Equivalence Partitioning | TestAxiom | Login fields, transfer amounts |
| Boundary Value Analysis | TestAxiom | Transfer boundaries (0.01 – 100.00) |
| Decision Table | TestAxiom | Loan approval logic |
| Data-Driven Testing | FixtureForge | Registration — 2 realistic fixtures, seed=42 |
| Failure Analysis | Failscope | Dual-agent RCA on every CI failure |

---

## Test Cases

### UI (10 tests)

| ID | Title | Priority |
|---|---|---|
| UI-001 | Valid login with default credentials | High |
| UI-002 | Login with invalid password | High |
| UI-003 | Login with empty username — BVA via TestAxiom | Medium |
| UI-004 | Account overview balance matches API | High |
| UI-005 | Fund transfer — valid amount | High |
| UI-006 | Fund transfer — boundary amounts BVA via TestAxiom (invalid boundaries → `xfail`: demo accepts all amounts) | High |
| UI-007 | Fund transfer — negative amount rejected (`xfail`: ParaBank demo accepts negative amounts — known SUT defect) | Medium |
| UI-008 | New user registration — DDT via FixtureForge | High |
| UI-009 | Loan request — approved scenario | High |
| UI-010 | Loan request — denied scenario | High |

### API (8 tests)

| ID | Endpoint | Scenario | Priority |
|---|---|---|---|
| API-001 | `GET /accounts/{id}` | Valid account returns correct data | High |
| API-002 | `GET /accounts/{id}` | Invalid ID returns error | High |
| API-003 | `POST /transfer` | Valid transfer updates balance | High |
| API-004 | `POST /transfer` | Insufficient funds returns error | High |
| API-005 | `POST /requestLoan` | Decision table — approved & denied | Medium |
| API-006 | `GET /accounts/{id}/transactions` | Transaction list returned | Low |
| API-007 | `POST /register` | Duplicate username returns error | Medium |
| API-008 | `GET /customers/{id}` | Customer data returned | Medium |

### E2E + DB (2 tests)

| ID | Title | Layers | Priority |
|---|---|---|---|
| E2E-001 | Transfer via UI → verify API balance → confirm DB record | UI + API + DB | High |
| E2E-003 | Loan request via UI → verify API status → DB confirmation | UI + API + DB | High |

> **Total: 25 test cases** (including 4 BVA parametrized sub-cases from TestAxiom)

---

## Tech Stack

| Component | Technology | Version |
|---|---|---|
| Language | Python | 3.13 |
| UI Automation | Playwright | latest |
| Test Framework | pytest | 9.x |
| Test Design | TestAxiom | ≥ 0.1.0 |
| Failure Analysis | Failscope | ≥ 0.3.0 |
| Test Data | FixtureForge | ≥ 2.1.0 |
| Reporting | Allure | 2.29 |
| CI/CD | GitHub Actions | — |
| SUT Container | Docker (`parasoft/parabank`) | latest |
| Test Timeout | pytest-timeout | latest |
| Database | SQLite | built-in |
| HTTP Client | requests | built-in |

---

## Project Structure

```
parabank-automation-testing/
│
├── .github/
│   └── workflows/
│       └── playwright_tests.yml   # CI pipeline
│
├── api_clients/
│   └── bank_api_client.py         # REST client — all ParaBank endpoints
│
├── config/
│   └── settings.py                # Base URL, credentials, env flags
│
├── data/
│   ├── users.csv                  # Seed data for registration DDT
│   └── transfers.json             # Transfer scenario definitions
│
├── pages/                         # Page Object Model
│   ├── base_page.py
│   ├── login_page.py
│   ├── accounts_page.py
│   ├── transfer_page.py
│   ├── loan_page.py
│   └── registration_page.py
│
├── tests/
│   ├── ui/
│   │   ├── test_login.py          # UI-001, 002, 003
│   │   ├── test_accounts.py       # UI-004
│   │   ├── test_transfer.py       # UI-005, 006, 007
│   │   ├── test_registration.py   # UI-008
│   │   └── test_loan.py           # UI-009, 010
│   ├── api/
│   │   └── test_endpoints.py      # API-001 → 008
│   └── e2e/
│       ├── test_transfer_consistency.py   # E2E-001
│       └── test_loan_logic.py             # E2E-003
│
├── utils/
│   ├── db_connector.py            # SQLite connector (local Docker)
│   └── fixture_forge_engine.py    # FixtureForge setup + Pydantic models
│
├── conftest.py                    # pytest fixtures
├── pytest.ini                     # pytest configuration
├── requirements.txt
├── .env.example                   # Environment variable template
└── Parabank_Test_Plan_v1.0.html   # Full test plan document
```

---

## Quick Start

### 1. Clone & install

```bash
git clone https://github.com/Yaniv2809/parabank-automation-testing.git
cd parabank-automation-testing
pip install -r requirements.txt
python -m playwright install chromium
```

### 2. Start ParaBank (choose one)

**Option A — Docker (recommended, identical to CI):**
```bash
docker run -d --name parabank -p 8080:8080 parasoft/parabank
# Wait ~30s for startup, then seed the database:
curl -X POST http://localhost:8080/parabank/services/bank/initializeDB
export PARABANK_BASE_URL=http://localhost:8080/parabank
```

**Option B — Public server (no Docker required):**
```bash
# Default — no setup needed, uses https://parabank.parasoft.com/parabank/
```

### 3. Run all tests

```bash
pytest
```

---

## Running Tests

### Run by layer

```bash
# UI only
pytest -m ui

# API only
pytest -m api

# E2E only
pytest -m e2e

# High priority only
pytest -m high
```

### Run a specific test

```bash
pytest tests/ui/test_login.py::TestLogin::test_valid_login
pytest tests/api/test_endpoints.py -v
```

### Run with Failscope AI analysis

```bash
# Offline mode — no API key needed
pytest --failscope --fs-offline

# With Groq (free tier)
export GROQ_API_KEY=your_key
pytest --failscope --fs-provider=groq
```

### Run with Allure report

```bash
pytest --alluredir=allure-results
allure serve allure-results
```

### Watch mode (visible browser)

```bash
HEADLESS=false pytest -m ui -v
```

---

## CI/CD Pipeline

Every push to `main` and every pull request triggers the full suite automatically.

```
Push / PR / Daily 06:00 UTC
        │
        ▼
┌──────────────────────────┐
│  parasoft/parabank       │  ← Docker service, port 8080
│  (health-check ready)    │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│  Setup Python 3.13       │
│  pip install             │
│  playwright install      │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│  POST /initializeDB      │  ← Seed john/demo + sample accounts
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│  pytest                  │
│    --failscope           │  ← Failscope dual-agent RCA
│    --fs-offline          │
│    --timeout=45          │  ← per-test hard cap
│    --alluredir           │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│  Allure CLI generates    │
│  HTML report             │
│  + Test Plan copied in   │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│  GitHub Pages publish    │  ← Allure report + Test Plan (STP)
│  Artifacts upload        │  ← allure-results + .failscope/
└──────────────────────────┘
```

**Allure report** → `https://yaniv2809.github.io/parabank-automation-testing/`  
**Test Plan (STP)** → `https://yaniv2809.github.io/parabank-automation-testing/test-plan.html`  
**Failscope RCA report** is uploaded as a CI artifact (`failscope-report`).

---

## Custom Libraries

This framework integrates three custom PyPI libraries built for AI-powered QA:

### [TestAxiom](https://pypi.org/project/testaxiom/) — Test Design Engine

Generates mathematically optimal test cases using ISTQB techniques (EP, BVA).

```python
from testaxiom import analyze

# Generates 7 test cases: 3 EP partitions + 4 BVA boundaries
result = analyze("amount", param_type="float", valid_range=(0.01, 100.00))

# Used in pytest.mark.parametrize — each boundary becomes a test case
@pytest.mark.parametrize("amount,validity", [
    (tc.input_value, tc.expected.value)
    for tc in result.test_cases
    if tc.technique.value == "bva"
])
def test_boundary_amounts(self, logged_in_page, amount, validity):
    ...
```

**Used in:** `test_login.py` (UI-003), `test_transfer.py` (UI-006), `test_endpoints.py` (API-005)

---

### [FixtureForge](https://pypi.org/project/fixtureforge/) — Test Data Harness

Generates realistic, deterministic test data fixtures via Pydantic models.

```python
from fixtureforge import Forge
from pydantic import BaseModel

class RegistrationData(BaseModel):
    first_name: str
    last_name:  str
    address:    str
    city:       str
    state:      str
    zip_code:   str
    phone:      str
    username:   str

# CI mode — deterministic, zero AI cost, same seed = same data always
forge = Forge(use_ai=False, seed=42, interactive=False)
users = forge.create_batch(RegistrationData, count=2)
```

**Used in:** `test_registration.py` (UI-008) — DDT with 2 generated users

---

### [Failscope](https://pypi.org/project/failscope/) — AI Failure Analysis

Zero-config pytest plugin that runs dual-agent RCA on every test failure.

```bash
# Added to CI pytest command — no code changes needed
pytest --failscope --fs-offline
```

Failscope automatically:
- Deduplicates failures by fingerprint
- Runs Analyzer → Critic dual-agent pipeline
- Generates `.failscope/rca_report.html` (uploaded as CI artifact)

**Used in:** GitHub Actions CI — post-test failure analysis

---

## Author

**Yaniv Metuku** — QA / SDET  
[TestAxiom](https://pypi.org/project/testaxiom/) · [FixtureForge](https://pypi.org/project/fixtureforge/) · [Failscope](https://pypi.org/project/failscope/)
