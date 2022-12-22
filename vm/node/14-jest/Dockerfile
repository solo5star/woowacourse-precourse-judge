FROM node:14

RUN apt update && apt install -y jq
WORKDIR /environment

COPY environment/package.json .
RUN npm install

COPY environment/ .
RUN chmod +x entrypoint.sh

CMD ./entrypoint.sh
