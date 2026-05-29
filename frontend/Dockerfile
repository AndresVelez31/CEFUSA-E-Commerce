FROM node:20-alpine
WORKDIR /app
# Instala dependencias en tiempo de build (no en cada arranque)
COPY package.json package-lock.json ./
RUN npm ci --silent
COPY . .
EXPOSE 3000
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "3000"]
