![halyard](asset/halyard_logo_main.svg)
> A production-grade zero-dependency feature flag engine.

[![.github/workflows/Continuous%20Integration.yml](https://img.shields.io/github/actions/workflow/status/bugra-ozer/adze/Continuous%20Integration.yml?style=flat-square&logo=github&label=Continuous%20Integration)](https://github.com/bugra-ozer/adze/Continuous%20Integration.yml)
![Python](https://img.shields.io/badge/Python-v3.14%2B-3776AB?style=flat-square&logo=python&logoColor=white&color=3776AB)
![HTML](https://img.shields.io/badge/HTML-v5-E34F26?style=flat-square&logo=html5&logoColor=white)
![CSS](https://img.shields.io/badge/CSS-v3-1572B6?style=flat-square&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-vECMA-F7DF1E?style=flat-square&logo=javascript&logoColor=black)
![Flask](https://img.shields.io/badge/v3.1.3%2B-3776AB?style=flat-square&logo=FastAPI&label=FastAPI)
![PostgreSQL](https://img.shields.io/badge/v18.6%2B-3776AB?style=flat-square&logo=PostgreSQL&label=PostgreSQL&logoColor=white)
![Docker](https://img.shields.io/badge/v29.6.2%2B-3776AB?style=flat-square&logo=Docker&label=Docker&logoColor=white)
![Auth](https://img.shields.io/badge/bcrypt,%20PyJWT,%20secrets,%20hashlib-000000?style=flat-square&logo=jsonwebtokens&logoColor=white&label=Auth)

---

## What is it?

Halyard is a feature flag and rollout engine that lets teams turn features on or off in a live application without redeploying code. 

Meaning? Shipping code and releasing a feature are two different things. Halyard separates them: a new checkout flow can go out hidden, be tested on a small group, and be switched off instantly if something breaks, with no emergency redeploy.

The dashboard and SDK are written in raw HTML5, CSS3, and vanilla ES6+ JavaScript with no UI framework. The backend runs on PostgreSQL with SQLAlchemy, JWT and refresh-token auth for admins, hashed API keys for SDK clients, and a Dockerized, pytest-covered pipeline with GitHub Actions CI.

---


## Architecture

![Architecture](asset/halyard_architecture.svg)

---

| Layer             | Technology                                     |
|-------------------|------------------------------------------------|
| Language          | Python 3.14+, HTML5, Raw CSS3, Vanilla ES6+ JS |
| Backend API       | FastAPI                                        |
| Database Tools    |                                                |
| Database Deploy   | PostgreSQL                                     |
| Infra and Testing | Docker, `pytest`, GitHub Actions CI            |
| Auth and Security | `bcrypt`, `PyJWT`, `secrets`, `hashlib`        |
| Config            | python-dotenv                                  |
| Deployment        |                                                |

---

## Getting Started