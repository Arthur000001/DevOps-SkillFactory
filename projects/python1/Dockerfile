
# Этап сборки зависимостей
FROM python:3.11-slim AS builder
WORKDIR /app
ENV PIP_NO_CACHE_DIR=1 PYTHONDONTWRITEBYTECODE=1
RUN apt-get update && apt-get install -y --no-install-recommends build-essential && rm -rf /var/lib/apt/lists/*
COPY pyproject.toml README.md ./
COPY src ./src
RUN pip wheel --no-deps -w /wheels .

# Рантайм
FROM python:3.11-slim
WORKDIR /app
ENV PIP_NO_CACHE_DIR=1 PYTHONDONTWRITEBYTECODE=1
COPY --from=builder /wheels /wheels
RUN pip install /wheels/*.whl && rm -rf /wheels
ENTRYPOINT ["kcsv"]
CMD ["--help"]
