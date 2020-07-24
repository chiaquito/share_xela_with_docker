FROM nginx:1.15.12-alpine

# デフォルトのconfを消して、別の設定を追加
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d
#RUN mkdir -p /usr/share/nginx/html/static
RUN mkdir -p /usr/src/app/media_root
RUN mkdir -p /usr/src/app/media_root/images
COPY ./media/default_item.png /usr/src/app/media_root/images
COPY ./media/user_icon.png /usr/src/app/media_root/images
