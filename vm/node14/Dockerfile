FROM node:14

WORKDIR /environment

COPY package.json .
RUN npm install
RUN npm install -g jest
ENV NODE_PATH=/environment/node_modules

WORKDIR /code

RUN useradd judge
USER judge

CMD ["npx", "jest", "--silent", "--detectOpenHandles", "--json"]
