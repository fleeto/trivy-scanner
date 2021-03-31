FROM flant/shell-operator:v1.0.0-rc.2
ENV TRIVY_CACHE_DIR=/data/trivy \
    TRIVY_QUIET=true \
    GITHUB_TOKEN="" \
    NS_LABEL="trivy=true"
RUN apk --no-cache add python3=3.8.8-r0
COPY trivy-scanner.py /hooks
COPY trivy /usr/local/bin
VOLUME [ "/data/trivy", "/data/cache" ]
