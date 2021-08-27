FROM node:14.16.1-alpine3.12 as frontend-app
EXPOSE 4200

# Install deps
RUN npm install

WORKDIR /app
COPY frontend/package*.json ./
RUN npm install

COPY . .
RUN npm run build


ENTRYPOINT ["npm", "run", "start:dev-proxy"]

