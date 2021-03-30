#!/bin/sh
set -e
cp trivy-scanner.py deploy/docker
docker build -t $1 deploy/docker
rm deploy/docker/trivy-scanner.py