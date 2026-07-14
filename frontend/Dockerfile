# 第一阶段：构建 Vue + Vite
FROM node:22-alpine AS build

WORKDIR /app

# 先复制依赖清单，利用 Docker 缓存
COPY package.json package-lock.json ./

# 根据 package-lock.json 安装确定的依赖
RUN npm ci

# 复制前端源代码
COPY . .

# 生成 dist
RUN npm run build


# 第二阶段：使用 Nginx 提供静态页面
FROM nginx:alpine

# 删除默认配置
RUN rm /etc/nginx/conf.d/default.conf

# 添加项目自己的 Nginx 配置
COPY nginx.conf /etc/nginx/conf.d/default.conf

# 从构建阶段复制 dist
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]