FROM node:22-alpine AS build

WORKDIR /app
COPY package*.json ./
RUN npm install

COPY . .
RUN npx webpack ./client.js --output-filename main.js --output-path ./dist

FROM nginx:1.27-alpine

COPY --from=build /app/index.html /usr/share/nginx/html/index.html
COPY --from=build /app/dist /usr/share/nginx/html/dist
COPY nginx.conf /etc/nginx/conf.d/default.conf
