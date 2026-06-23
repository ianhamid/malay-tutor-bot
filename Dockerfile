FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
# This upgrades the library for both your web app and your Telegram bot
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --upgrade google-generativeai
COPY . .
# Note: We do NOT add the CMD here if you are using 'command:' in docker-compose.yml