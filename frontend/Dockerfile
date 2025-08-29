# 使用官方 Nginx 映像檔作為基礎
FROM nginx:alpine

# 移除預設的 Nginx 配置檔
RUN rm /etc/nginx/conf.d/default.conf

# 【！！！關鍵修改！！！】
# 將旗標放在一個 Nginx 不會直接對外提供服務的路徑下
RUN mkdir -p /goodhacker && \
    echo "FLAG{THIS_IS_A_REAL_SSRF_FLAG!}" > /goodhacker/flag.txt

# 將自定義的 Nginx 配置檔複製到容器中
COPY nginx.conf /etc/nginx/conf.d/

# 將前端 HTML 檔案複製到 Nginx 的預設靜態檔案目錄
COPY . /usr/share/nginx/html

# 暴露 Nginx 監聽的埠號
EXPOSE 80

# 定義容器啟動時執行的命令 (Nginx 預設會啟動)
CMD ["nginx", "-g", "daemon off;"]
