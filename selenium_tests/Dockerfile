FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    wget curl unzip gnupg ca-certificates fonts-liberation libnss3 \
    libxss1 libatk1.0-0 libatk-bridge2.0-0 libgtk-3-0 libgbm-dev xvfb \
    --no-install-recommends && rm -rf /var/lib/apt/lists/*

# Install Google Chrome
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /usr/share/keyrings/google-linux-signing-key.gpg \
    && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-linux-signing-key.gpg] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /tests

# Copy requirements and install globally
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Default command: run pytest
CMD ["pytest", "-v", "-s", "--html=/tests/reports/report.html", "--self-contained-html", "selenium_tests/"]
