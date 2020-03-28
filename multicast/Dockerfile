FROM ubuntu:bionic

RUN set -eux \
    && apt update --yes \
    && apt install --yes \
        nginx-full \
        libnginx-mod-rtmp \
        libnginx-mod-http-lua \
    && rm -r /var/cache/apt

CMD ["nginx", "-g", "daemon off;"]