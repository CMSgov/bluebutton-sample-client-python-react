FROM node:19.9-slim

LABEL version="1.1"
LABEL description="Demo of a Medicare claims data sample app"

WORKDIR /client

COPY . .

# In case machine is Mac M1 chip
RUN apt-get update
RUN apt-get install python3 -y
RUN apt-get install python3-pip -y

RUN yarn install

EXPOSE 3000

CMD ["yarn","start"]