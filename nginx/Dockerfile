# develop stage
FROM node:lts-alpine AS develop-stage
WORKDIR /app

FROM nginx:alpine AS production-build
COPY ./nginx/production.conf /etc/nginx/nginx.conf
COPY ./nginx/certificates /etc/nginx/certificates

## Remove default nginx index page
RUN rm -rf /usr/share/nginx/html/*

# Copy from the stage 1

EXPOSE 443
