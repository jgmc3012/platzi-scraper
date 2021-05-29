FROM postgres:12

COPY ./docker/production/postgres/maintenance /usr/local/bin/maintenance
RUN chmod +x /usr/local/bin/maintenance/*
RUN cp -r /usr/local/bin/maintenance/* /usr/local/bin \
    && rm -r /usr/local/bin/maintenance
