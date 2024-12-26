# Dockerfile
# Node.js 이미지를 사용해 React 빌드
FROM node:16 AS build

# 작업 디렉토리 설정
WORKDIR /app

# package.json 및 package-lock.json 복사
COPY package*.json ./

# 의존성 설치
RUN npm install

# 애플리케이션 복사 및 빌드
COPY . .
RUN npm run build

# Nginx를 사용하여 배포
FROM nginx:stable-alpine

# Nginx 설정 복사
COPY nginx.conf /etc/nginx/conf.d/default.conf

# React 빌드 파일 복사
COPY --from=build /app/dist /usr/share/nginx/html

# Nginx 포트 노출
EXPOSE 80

# Nginx 시작
CMD ["nginx", "-g", "daemon off;"]
