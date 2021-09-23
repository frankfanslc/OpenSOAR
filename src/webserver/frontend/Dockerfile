FROM node:16 as build-stage

WORKDIR /app

COPY package*.json ./

RUN npm clean-install

COPY . .

#RUN npm run css-build
RUN npm run build

FROM node:16

WORKDIR /app

COPY --from=build-stage /app .

EXPOSE 3000
CMD ["node", "./build"]