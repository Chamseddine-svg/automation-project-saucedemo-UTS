# Use official Playwright image with Node 20 + browsers
FROM mcr.microsoft.com/playwright:v1.57.0-jammy

# Set working directory
WORKDIR /tests

# Copy dependency files first for Docker caching
COPY package.json package-lock.json ./

# Install Node dependencies (including @playwright/test)
RUN npm ci

# Install Playwright Chrome browser
RUN npx playwright install chrome

# Copy the rest of the project
COPY . .

# Default command to run all tests
CMD ["npx", "playwright", "test", "--project=Chrome"]
