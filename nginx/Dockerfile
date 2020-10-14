FROM nginx

RUN cp nginx.conf /etc/nginx/nginx.conf
RUN rm /etc/nginx/conf.d/*
RUN mkdir -p /etc/nginx/sites-enabled
RUN cp sites-enabled/atptennisapi /etc/nginx/sites-enabled

ENTRYPOINT ["nginx", "-g", "daemon off;"]