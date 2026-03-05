# Build stage
FROM python:3.10-slim AS builder
WORKDIR /build
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY scarlet-common/ ./scarlet-common/
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir ./scarlet-common

COPY volition/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Runtime stage
FROM python:3.10-slim AS runtime
WORKDIR /app
RUN useradd --no-create-home --shell /bin/false appuser

COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH" \
    PYTHONPATH="/app"

COPY volition/src/ ./src/
COPY volition/config/ ./config/

USER appuser
EXPOSE 8002
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8002"]
