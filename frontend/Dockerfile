# 1. Build stage
FROM node:20 AS builder
WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm install

# Copy the rest of the source
COPY . .

# Build the React app
RUN npm run build

# 2. Production stage with Nginx
FROM nginx:alpine

# Copy built assets from previous stage
COPY --from=builder /app/dist /usr/share/nginx/html

# Use a custom Nginx config for SPA routing
COPY ./docker/nginx/default.conf /etc/nginx/conf.d/default.conf
