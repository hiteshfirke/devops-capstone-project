# DevOps Capstone Project

Accounts Service

![Build Status](https://github.com/hiteshfirke/devops-capstone-project/actions/workflows/ci-build.yaml/badge.svg)

Accounts REST API microservice: Flask, SQLAlchemy, Talisman security headers, CORS,
Docker, Kubernetes and a Tekton CD pipeline.

## Endpoints
| Method | Path | Action |
|---|---|---|
| POST | /accounts | Create |
| GET | /accounts | List |
| GET | /accounts/{id} | Read |
| PUT | /accounts/{id} | Update |
| DELETE | /accounts/{id} | Delete |

## Develop
```
python -m venv .venv && . .venv/bin/activate
pip install -r requirements-dev.txt
nosetests
flake8 service
```
