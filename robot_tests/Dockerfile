FROM python:3.12-slim

# ---- System + browser dependencies ----
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    wget \
    curl \
    unzip \
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libcups2 \
    libdbus-1-3 \
    libdrm2 \
    libgbm1 \
    libgtk-3-0 \
    libnss3 \
    libx11-xcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libxshmfence1 \
    libxss1 \
    libxtst6 \
    xdg-utils \
    --no-install-recommends \
 && rm -rf /var/lib/apt/lists/*

# ---- Python dependencies ----
RUN pip install --no-cache-dir \
    robotframework \
    robotframework-seleniumlibrary \
    selenium

# ---- Environment ----
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER=/usr/bin/chromedriver
ENV PATH="/usr/bin:${PATH}"

# ---- Workspace ----
WORKDIR /tests

# ---- Default command ----
CMD ["robot", "-d", "results", "tests"]
