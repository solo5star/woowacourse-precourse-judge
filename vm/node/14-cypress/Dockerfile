FROM cypress/included:8.7.0

RUN apt update && apt install -y jq libxml2-utils
WORKDIR /environment

COPY environment/package.json .
RUN npm install

COPY environment/ .
RUN chmod +x entrypoint.sh

ENTRYPOINT ./entrypoint.sh
