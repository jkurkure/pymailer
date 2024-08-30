FROM alpine

RUN apk add --no-cache python3 \
    && apk add --no-cache npm \
    && apk add --no-cache nano