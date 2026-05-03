FROM python:3.10-slim AS builder

WORKDIR /build
COPY requirements.txt .
RUN pip install --upgrade pip --trusted-host pypi.org --trusted-host files.pythonhosted.org && \
    pip wheel --no-cache-dir --wheel-dir /wheels -r requirements.txt \
    --trusted-host pypi.org \
    --trusted-host pypi.python.org \
    --trusted-host files.pythonhosted.org

FROM python:3.10-slim AS runtime

RUN apt-get update && apt-get install -y --no-install-recommends \
    tesseract-ocr \
    tesseract-ocr-heb \
    poppler-utils \
    libtesseract-dev \
    fonts-freefont-ttf \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY --from=builder /wheels /wheels
RUN pip install --no-cache-dir /wheels/* && rm -rf /wheels
COPY . .

ENTRYPOINT ["python", "main.py"]