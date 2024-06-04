FROM postgres:latest

COPY init.sql /docker-entrypoint-initdb.d/
RUN useradd -m postgres
USER postgres
