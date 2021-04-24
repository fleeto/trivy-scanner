FROM flant/shell-operator:v1.0.0-rc.2

ENV TRIVY_CACHE_DIR=/data/trivy \
    TRIVY_QUIET=true \
    GITHUB_TOKEN="" \
    NS_LABEL="trivy=true"

RUN apk --no-cache add python3=3.8.8-r0

COPY trivy-scanner.py /hooks
COPY trivy /usr/local/bin

RUN apk add --no-cache git && \
    addgroup -S -g 10001 kube-trivy-exporter && \
    adduser -S -u 10001 kube-trivy-exporter -G kube-trivy-exporter && \
    mkdir /var/run/shell-operator && \
    chown -R kube-trivy-exporter:kube-trivy-exporter /var/run/shell-operator

USER 10001:10001

EXPOSE 9115

VOLUME [ "/data/trivy", "/data/cache" ]
