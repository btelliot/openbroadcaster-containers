FROM ubuntu/nginx:latest
USER root
RUN apt-get update -y && apt-get upgrade -y
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y \
  apache2 \
  apg \
  festival \
  imagemagick \
  libavcodec-extra \
  libavfilter-extra \
  mysql-server \
  vorbis-tools

RUN apt-get update -y 
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y software-properties-common
RUN apt-add-repository ppa:ondrej/php -y
RUN apt-get update -y

RUN DEBIAN_FRONTEND=noninteractive apt-get install -y \
  php8.3 \
  php8.3-fpm \
  php8.3-mysql \
  php8.3-mysql \
  php8.3-mbstring \
  php8.3-xml \
  php8.3-gd \
  php8.3-curl \
  php8.3-cli \
  php8.3-imagick

RUN DEBIAN_FRONTEND=noninteractive apt-get install -y \
  ufw \
  systemd \
  git

# Remove the files initailly created by apache
RUN rm -dfr /var/www/html

RUN DEBIAN_FRONTEND=noninteractive apt-get install -y ffmpeg;
RUN ln -s /usr/bin/ffmpeg /usr/local/bin/avconv
RUN ln -s /usr/bin/ffprobe /usr/local/bin/avprobe

RUN mkdir /home/media && chmod 777 /home/media;
RUN mkdir /home/media/uploads && chmod 777 /home/media/uploads;
RUN mkdir /home/media/thumbnails && chmod 777 /home/media/thumbnails;
RUN mkdir /home/media/archive && chmod 777 /home/media/archive;
RUN mkdir /home/media/cache && chmod 777 /home/media/cache;
RUN mkdir /home/assets && chmod 777 /home/assets;

WORKDIR /var/www/html

# Own /var/www/html
RUN chmod 755 .

ARG USER=obsuser
ARG OBCONF_PASS=password
ARG OBCONF_EMAIL=ob@example.com
ARG MYSQL_PASS=password
ARG OB_UPDATES_PW=password
ARG OBCONF_URL=http://localhost/
ARG OBCONF_SALT=randomsalt123
ARG OB_DB_HOST=mysql-db
ARG OB_DB_PASS=password
ARG OB_DB_NAME=obdb

RUN useradd obsuser > /dev/null 2>&1  && \
  usermod -a -G obsuser obsuser > /dev/null 2>&1  && \
  usermod -a -G www-data obsuser > /dev/null 2>&1

RUN mkdir -p /home/assets/uploads
RUN chown -R www-data /home/media /home/assets
RUN find /home/media/ -type d -exec chmod 0775 {} \;
RUN find /home/media/ -type f -exec chmod 0664 {} \;

# Pipe NGINX logs to docker terminal
RUN ln -sf /dev/stdout /var/log/nginx/access.log && ln -sf /dev/stderr /var/log/nginx/error.log

# Link available config to enabled NGINX directory
RUN ln -s /etc/nginx/sites-available/observer.conf /etc/nginx/sites-enabled/

ARG REPOSITORY=https://github.com/openbroadcaster/observer.git
ENV REPOSITORY=$REPOSITORY

ARG BRANCH
ENV BRANCH=5.3-develop

RUN git clone $REPOSITORY /var/www/html
RUN git checkout $BRANCH

ARG MODULE_NAMES
ARG MODULE_REPOSITORIES

SHELL ["/bin/bash", "-c"]

RUN \
declare -a MODULES=$MODULE_NAMES;\
declare -a REPOS=$MODULE_REPOSITORIES;\
INDEX=0;\
for module in $MODULES; do \
  repository=${REPOS[$INDEX]};\
  echo "Installing module $INDEX: '$module' from '$repository'";\
  git clone $repository /var/www/html/modules/$module; \
  INDEX=$((INDEX + 1));\
done;

SHELL ["/bin/sh", "-c"]

RUN echo '\
<?php\n\
const OB_HASH_SALT = "'$OBCONF_SALT'";\n\
const OB_DB_USER = "'$USER'";\n\
const OB_DB_PASS = "'$OB_DB_PASS'";\n\
const OB_DB_HOST = "'$OB_DB_HOST'";\n\
const OB_DB_NAME = "'$OB_DB_NAME'";\n\
const OB_MEDIA = "/home/media";\n\
const OB_MEDIA_UPLOADS = "/home/media/uploads";\n\
const OB_MEDIA_ARCHIVE = "/home/media/archive";\n\
const OB_CACHE = "/home/media/cache";\n\
const OB_THUMBNAILS = "/home/media/thumbnails";\n\
const OB_ASSETS = "/home/assets";\n\
const OB_SITE = "'$OBCONF_URL'";\n\
const OB_EMAIL_REPLY = "'$OBCONF_EMAIL'";\n\
const OB_EMAIL_FROM = "OpenBroadcaster";\n\
const OB_UPDATES_USER = "admin";\n\
const OB_UPDATES_PW = "'$OB_UPDATES_PW'";\n\
?>' >> /var/www/html/config.php;

RUN apt-get install -y ffmpeg

# Install Composer
RUN apt-get update && apt-get install -y curl unzip && \
    curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer

# Run Composer to install dependencies
RUN composer install --no-dev --optimize-autoloader

# Download Node.js
RUN apt-get install -y npm

# Run NPM to install Node.js
RUN npm install

RUN chown -R www-data:www-data /var/www/html
RUN chmod -R 755 /var/www/html

RUN echo "NGINX is working!" > /var/www/html/test.html
RUN echo "<?php phpinfo();" > /var/www/html/test.php

# iputils for testing connection to mysql
RUN apt-get update && apt-get install -y iputils-ping

COPY ./observer.conf /etc/nginx/sites-enabled/
COPY ./startup.sh /home/startup.sh

ENTRYPOINT ["/bin/bash", "/home/startup.sh"]



EXPOSE 80
EXPOSE 443
EXPOSE 465
EXPOSE 25