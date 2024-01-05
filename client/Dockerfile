FROM node:19.9-slim

LABEL version="1.1"
LABEL description="Demo of a Medicare claims data sample app"

WORKDIR /client

COPY . .

RUN yarn install

EXPOSE 3000

CMD ["yarn","start"]