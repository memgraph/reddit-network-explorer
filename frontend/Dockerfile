FROM node:14.17.0-alpine3.12 as frontend-app
EXPOSE 4200

COPY . ./app
WORKDIR /app

RUN npm install
RUN npm run build


ENTRYPOINT ["npm", "run", "start:dev-proxy"]
