# Stage 0, "build-stage", based on Node.js, to build and compile the frontend
FROM node:latest as build-stage

WORKDIR /app

COPY package*.json /app/

RUN npm install

COPY ./ .

RUN npm run build


# Stage 1, based on Nginx, to have only the compiled app, ready for production with Nginx
FROM nginx:1.21

RUN mkdir /app

COPY --from=build-stage /app/public /app

COPY nginx.conf /etc/nginx/nginx.conf
