FROM node:20.18.0-alpine3.20
COPY . /app
WORKDIR /app
RUN npm install --non-interactive --frozen-lockfile
EXPOSE 8545
ENTRYPOINT [ "/bin/sh", "entrypoint.sh"]