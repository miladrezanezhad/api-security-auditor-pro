# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# کپی فایل‌های requirements
COPY requirements.txt .
COPY requirements-dev.txt .

# نصب وابستگی‌های سیستم
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# نصب وابستگی‌های پایتون
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -r requirements-dev.txt

# کپی سورس کد
COPY . .

# نصب پکیج
RUN pip install -e .

ENTRYPOINT ["api-auditor"]