FROM node:22-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 8080

CMD ["npx", "webpack", "serve", "--config", "webpack.config.js", "--host", "0.0.0.0", "--port", "8080"]