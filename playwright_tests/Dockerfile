FROM mcr.microsoft.com/playwright:v1.41.2-jammy

# ---- Workspace ----
WORKDIR /tests

# ---- Copy dependency files first (Docker layer cache) ----
COPY package.json package-lock.json ./

# ---- Install Node dependencies ----
RUN npm ci

# ---- Copy the rest of the project ----
COPY . .

# ---- Default command ----
CMD ["npx", "playwright", "test"]
