FROM node:18-alpine AS base

# Dependencies
FROM base AS deps


# Setup npm Env
ENV NPM_HOME="/npm"
ENV PATH="$NPM_HOME:$PATH"
RUN apk add --no-cache libc6-compat

WORKDIR /app

COPY package.json package-lock.json ./
# RUN npm install -g npm@11.1.0
RUN npm ci

# Rebuild the source
FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .

ENV NEXT_TELEMETRY_DISABLED=1

RUN npm run build

# Production image

FROM base AS runner
WORKDIR /app

ENV NODE_ENV=production

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

COPY --from=builder /app/public ./public

# Automatically leverage output traces to reduce image size
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
# Copy static assets separately to .next/static
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs

EXPOSE 3000

ENV PORT=3000

LABEL authors="blueprime"

ENV HOSTNAME="0.0.0.0"
CMD ["node", "server.js"]
