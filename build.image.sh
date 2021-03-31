#!/bin/sh
wget -q -O /tmp/trivy.tar.gz https://github.com/aquasecurity/trivy/releases/download/v0.16.0/trivy_0.16.0_Linux-64bit.tar.gz
tar -C /tmp -xf /tmp/trivy.tar.gz
cp /tmp/trivy deploy/docker
cp trivy-scanner.py deploy/docker
docker build -t $1 \
  deploy/docker
rm -f deploy/docker/trivy-scanner.py
rm -f deploy/docker/trivy
