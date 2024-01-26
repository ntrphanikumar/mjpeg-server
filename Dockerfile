FROM ubuntu:latest

ENV TZ=Asia/Calcutta
ARG DEBIAN_FRONTEND=noninteractive
RUN apt update && apt install -y lighttpd ffmpeg
RUN cd /etc/lighttpd/conf-enabled && ln -s ../conf-available/10-cgi.conf
COPY 10-cgi.conf /etc/lighttpd/conf-available/10-cgi.conf
COPY start.sh /
RUN mkdir /var/www/cgi-bin
COPY cgi-bin /var/www/cgi-bin

CMD ["/start.sh"]
