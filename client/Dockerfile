FROM node:22.23.2-alpine3.24

ARG BB2-APP_LAUNCH

ENV BB2_APP_LAUNCH=${BB2_APP_LAUNCH:-"start"}

LABEL version="1.1"
LABEL description="Demo of a Medicare claims data sample app"

WORKDIR /client

COPY . .

# In case machine is Mac M1 chip
RUN apk update && \
    apk add --no-cache libcap python3 py3-pip libssh2

RUN yarn install
# comment build out if not going to use preview to save build time
RUN yarn build

EXPOSE 3000

CMD ["sh", "-c", "yarn $BB2_APP_LAUNCH"]
