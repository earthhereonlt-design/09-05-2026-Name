FROM python:3.12-slim-bookworm

# System deps for Playwright
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    apt-transport-https \
    ca-certificates \
    libglib2.0-0 \
    libx11-6 \
    libx11-xcb1 \
    libxcb1 \
    libxext6 \
    libxrender1 \
    libnss3 \
    libnspr4 \
    fonts-liberation \
    libappindicator1 \
    libindicator7 \
    xdg-utils \
    --no-install-recommends && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browser and dependencies
RUN playwright install chromium
RUN playwright install-deps chromium

COPY . .

# Create data dir
RUN mkdir -p data

CMD ["python", "-m", "bot.main"]
