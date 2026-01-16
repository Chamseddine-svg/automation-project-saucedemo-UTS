# Use official Python slim image
FROM python:3.12-slim

# ---- Install system dependencies ----
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    unzip \
    gnupg \
    ca-certificates \
    fonts-liberation \
    libnss3 \
    libxss1 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    libgbm-dev \
    xvfb \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# ---- Install Google Chrome ----
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /usr/share/keyrings/google-linux-signing-key.gpg \
    && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-linux-signing-key.gpg] http://dl.google.com/linux/chrome/deb/ stable main" \
       > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# ---- Set working directory ----
WORKDIR /tests

# ---- Create Python virtual environment ----
RUN python -m venv /tests/venv

# ---- Activate venv and install Python dependencies ----
COPY requirements.txt .
RUN /bin/bash -c "source /tests/venv/bin/activate && pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt"

# ---- Copy the rest of the project ----
COPY . .

# ---- Default command: activate venv and run pytest ----
CMD ["/bin/bash", "-c", "source /tests/venv/bin/activate && pytest -v -s --html=reports/login_report.html --self-contained-html selenium_tests/"]
