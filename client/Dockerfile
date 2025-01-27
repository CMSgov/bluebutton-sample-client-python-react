FROM node:22

ARG BB2-APP_LAUNCH

ENV BB2_APP_LAUNCH=${BB2_APP_LAUNCH:-"start"}

LABEL version="1.1"
LABEL description="Demo of a Medicare claims data sample app"

WORKDIR /client

COPY . .

# In case machine is Mac M1 chip
RUN apt-get update
RUN apt-get install python3 -y
RUN apt-get install python3-pip -y

RUN yarn install
# comment build out if not going to use preview to save build time
RUN yarn build

EXPOSE 3000

CMD ["sh", "-c", "yarn $BB2_APP_LAUNCH"]
