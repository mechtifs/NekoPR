FROM node:latest

WORKDIR /app
COPY . .
RUN npm config set registry https://registry.npmmirror.com/
RUN npm install
EXPOSE 5173

ENTRYPOINT [ "npm", "run", "dev" ]
