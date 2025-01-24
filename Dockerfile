FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Security hardening
RUN adduser --disabled-password coder
USER coder
COPY . .

CMD ["python", "-u", "/app/composer.py"]