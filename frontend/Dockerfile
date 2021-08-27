FROM node:14.16.1-alpine3.12
EXPOSE 4200

# Install deps
RUN npm install

WORKDIR /app
COPY . .

ENTRYPOINT ["npm", "run", "start:dev-proxy"]

