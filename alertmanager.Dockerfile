FROM alpine:latest AS downloader
ADD https://github.com/prometheus/alertmanager/releases/download/v0.27.0/alertmanager-0.27.0.linux-amd64.tar.gz /tmp/
RUN tar -xzf /tmp/alertmanager-0.27.0.linux-amd64.tar.gz -C /tmp
RUN mv /tmp/alertmanager-0.27.0.linux-amd64/alertmanager /usr/local/bin/

FROM alpine:latest
RUN apk add --no-cache gettext
COPY --from=downloader /usr/local/bin/alertmanager /bin/alertmanager
USER nobody
ENTRYPOINT ["/bin/sh"]
CMD ["-c", "envsubst < /etc/alertmanager/alertmanager.yml.template > /etc/alertmanager/alertmanager.yml && /bin/alertmanager --config.file=/etc/alertmanager/alertmanager.yml"]