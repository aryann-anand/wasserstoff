FROM node:22 as build

WORKDIR /app

# Copy package.json and package-lock.json
COPY frontend/package*.json ./

# Install dependencies
RUN npm install

# Copy the frontend code
COPY frontend/ ./

# Build the application
RUN npm run build

# Production stage
FROM nginx:stable-alpine

# Copy the build files from the build stage
COPY --from=build /app/build /usr/share/nginx/html

# Configure nginx
RUN echo 'server { \
    listen 80; \
    location / { \
        root /usr/share/nginx/html; \
        index index.html index.htm; \
        try_files $uri $uri/ /index.html; \
    } \
}' > /etc/nginx/conf.d/default.conf

# Expose the port
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
