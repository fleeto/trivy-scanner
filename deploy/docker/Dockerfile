FROM flant/shell-operator:v1.0.0-rc.2
ENV TRIVY_CACHE_DIR=/root/.cache/trivy \
    TRIVY_QUIET=true \
    GITHUB_TOKEN="" \
    NS_LABEL="trivy=true"

RUN apk --no-cache add python3=3.8.8-r0 && \
    wget -q -O /tmp/trivy.tar.gz https://github.com/aquasecurity/trivy/releases/download/v0.16.0/trivy_0.16.0_Linux-64bit.tar.gz && \
    tar -C /usr/local/bin -xf /tmp/trivy.tar.gz && \
    rm -Rf /usr/local/bin/contrib && \
    rm /tmp/trivy.tar.gz
VOLUME [ "/data/trivy_db", "/data/cache" ]
COPY scanner.py /hooks