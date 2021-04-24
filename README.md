# Monitoring vulnerabilities in docker images

Built with [Shell Operator](https://github.com/flant/shell-operator)

## Build & Deploy

### Docker Image

```bash
$ ./build.image.sh [repository:tag]
...
```

## Deploy

```bash
kubectl apply -k deploy/kubernetes/
```

## Usage

Every 5 minutes, the script will be executed, It will get image list from all namespaces with the label `trivy=true`, and then scan this images with trivy, finally we will get metrics on `http://[pod-ip]:9115/metrics` like this:

```bash
kubectl label namespaces guestbook-demo trivy=true

curl -s http://10.43.179.39:9115/metrics | grep so_vulnerabilities
```

~~~text
# HELP so_vulnerabilities so_vulnerabilities
# TYPE so_vulnerabilities gauge
so_vulnerabilities{hook="trivy-scanner.py",image="nginx:1.19.6-alpine",severity="CRITICAL"} 0
so_vulnerabilities{hook="trivy-scanner.py",image="nginx:1.19.6-alpine",severity="HIGH"} 4
so_vulnerabilities{hook="trivy-scanner.py",image="nginx:1.19.6-alpine",severity="LOW"} 2
so_vulnerabilities{hook="trivy-scanner.py",image="nginx:1.19.6-alpine",severity="MEDIUM"} 4
so_vulnerabilities{hook="trivy-scanner.py",image="nginx:1.19.6-alpine",severity="UNKNOWN"} 0
~~~
