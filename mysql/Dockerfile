FROM ubuntu/mysql

ARG REPOSITORY=https://github.com/openbroadcaster/observer.git
ENV REPOSITORY=$REPOSITORY

WORKDIR /app

RUN apt-get update -y && apt-get install -y git

ARG BRANCH
ENV BRANCH=5.3-develop

RUN git clone $REPOSITORY .
RUN git checkout $BRANCH

RUN cp ./db/dbclean.sql /docker-entrypoint-initdb.d/dbclean.sql

RUN rm -rf /app

# Disable binary logging
RUN echo "[mysqld]" >> /etc/mysql/conf.d/mysql.cnf && \
    echo "skip-log-bin" >> /etc/mysql/conf.d/mysql.cnf

EXPOSE 3306