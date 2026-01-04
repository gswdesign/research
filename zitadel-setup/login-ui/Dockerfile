# Multi-stage build for React + Vike Login UI
# Optimized for Railway deployment

# ============================================
# Stage 1: Dependencies
# ============================================
FROM node:20-alpine AS deps

WORKDIR /app

# Copy package files
COPY package.json pnpm-lock.yaml* package-lock.json* yarn.lock* ./

# Install dependencies based on available lockfile
RUN \
  if [ -f pnpm-lock.yaml ]; then \
    corepack enable && pnpm install --frozen-lockfile; \
  elif [ -f yarn.lock ]; then \
    yarn install --frozen-lockfile; \
  elif [ -f package-lock.json ]; then \
    npm ci; \
  else \
    npm install; \
  fi

# ============================================
# Stage 2: Builder
# ============================================
FROM node:20-alpine AS builder

WORKDIR /app

# Copy dependencies from previous stage
COPY --from=deps /app/node_modules ./node_modules
COPY . .

# Build arguments for environment variables
ARG VITE_ZITADEL_AUTHORITY
ARG VITE_ZITADEL_CLIENT_ID
ARG VITE_REDIRECT_URI
ARG VITE_POST_LOGOUT_REDIRECT_URI

# Set environment variables for build
ENV VITE_ZITADEL_AUTHORITY=$VITE_ZITADEL_AUTHORITY
ENV VITE_ZITADEL_CLIENT_ID=$VITE_ZITADEL_CLIENT_ID
ENV VITE_REDIRECT_URI=$VITE_REDIRECT_URI
ENV VITE_POST_LOGOUT_REDIRECT_URI=$VITE_POST_LOGOUT_REDIRECT_URI

# Build the application
RUN \
  if [ -f pnpm-lock.yaml ]; then \
    corepack enable && pnpm build; \
  elif [ -f yarn.lock ]; then \
    yarn build; \
  else \
    npm run build; \
  fi

# ============================================
# Stage 3: Production Runner
# ============================================
FROM node:20-alpine AS runner

WORKDIR /app

# Create non-root user for security
RUN addgroup --system --gid 1001 nodejs && \
    adduser --system --uid 1001 vike

# Copy built assets
COPY --from=builder --chown=vike:nodejs /app/dist ./dist
COPY --from=builder --chown=vike:nodejs /app/node_modules ./node_modules
COPY --from=builder --chown=vike:nodejs /app/package.json ./

# Install only production dependencies for server
RUN npm install --production express compression

# Create a simple production server
RUN echo 'const express = require("express"); \
const compression = require("compression"); \
const path = require("path"); \
const app = express(); \
app.use(compression()); \
app.use(express.static(path.join(__dirname, "dist/client"), { maxAge: "1y", immutable: true })); \
app.get("*", (req, res) => res.sendFile(path.join(__dirname, "dist/client/index.html"))); \
const port = process.env.PORT || 3000; \
app.listen(port, () => console.log(`Server running on port ${port}`));' > server.js

# Switch to non-root user
USER vike

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:3000/ || exit 1

# Start the server
CMD ["node", "server.js"]
