# Full stack code for agent TODO app: roger.ai

This repo contains a **React + TypeScript** client and a **FastAPI + SQLAlchemy** server for managing personal TODO lists and projects. It's wired together via Docker Compose.

## Stack

- **Client**
  - React + TypeScript
  - Vite bundler
- **Server**
  - FastAPI
  - SQLAlchemy ORM
  - SQLite (default, easy to swap to Postgres later)
- **Infra**
  - Docker & Docker Compose

## Getting Started

```bash
# From repo root
docker-compose up --build
