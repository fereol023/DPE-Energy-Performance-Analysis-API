# builder les wheels
FROM python:3.12 AS builder

# outils nécessaires pour compiler les paquets depuis la dist. source source
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN pip install uv
WORKDIR /app
COPY requirements.txt .
COPY . .
RUN apt-get update && \
    apt-get install -y git && \
    git submodule update --init --recursive && \
    git submodule foreach 'git checkout main || :'
# builder les wheels (avec cache buildx pour accélérer les rebuilds)
RUN --mount=type=cache,target=/root/.cache/uv \
    uv pip wheel -r requirements.txt --wheel-dir /wheels

# image finale
FROM python:3.12-slim
RUN pip install uv
WORKDIR /app
# copier les wheels déjà compilés
COPY --from=builder /wheels /wheels
COPY requirements.txt .
# installer les deps depuis les wheels
RUN --mount=type=cache,target=/root/.cache/uv \
    uv pip install --no-index --find-links=/wheels -r requirements.txt
COPY . .
RUN apt-get update && \
    apt-get install -y git && \
    git submodule update --init --recursive && \
    git submodule foreach 'git checkout main || :'
EXPOSE 8000
CMD ["python3", "main.py"]


