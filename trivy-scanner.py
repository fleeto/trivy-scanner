#!/usr/bin/env python3
import argparse
import os
import sys
import json
import subprocess

parser = argparse.ArgumentParser(description='Pod hook for Shell-Operator')
parser.add_argument('--config', action='store_true')

args = parser.parse_args()
CONFIG_FILE = os.getenv("CONFIG_FILE", "/etc/trivy-scanner/config.yaml")
CONTEXT_FILE = os.getenv("BINDING_CONTEXT_PATH")
METRIC_FILE = os.getenv("METRICS_PATH")
NS_LABEL = os.getenv("NS_LABEL", "trivy=true")

if args.config:
    with open(CONFIG_FILE) as cfg:
        print("".join(cfg.readlines()))
    sys.exit(0)

## Get namespaces.
CMD = ["kubectl", "get", "ns", "-o", "json" ,"-l", NS_LABEL]
ns_list = json.loads(
    subprocess.check_output(CMD).decode("UTF-8")
)

result_cache = {}
vul_list = {}
for ns in ns_list["items"]:
    ns_name = ns["metadata"]["name"]
    CMD = ["kubectl", "get", "pods",
    "-o", 'jsonpath="{.items[*].spec.containers[*].image}"',
    "-n", ns_name]
    image_str = subprocess.check_output(CMD).decode("UTF-8")
    image_list = set(image_str.split(" "))
    for image_name in image_list:
        if image_name in result_cache.keys():
            continue
        image_name = image_name.strip(" \"'").strip()
        if len(image_name) == 0:
            continue
        print("Scanning " + image_name)
        TRIVY = ["trivy", "-q", "i", "-f", "json", image_name]
        trivy_result = json.loads(
            subprocess.check_output(TRIVY).decode("UTF-8")
        )
        item_list = trivy_result[0]["Vulnerabilities"]
        vuls = {
            "UNKNOWN": 0,"LOW": 0,
            "MEDIUM": 0,"HIGH": 0,
            "CRITICAL": 0
        }
        for item in item_list:
            vuls[item["Severity"]] += 1
        vul_list[image_name] = vuls

with open(METRIC_FILE, "w") as metric_file:
    for image_name in vul_list.keys():
        for severity in vul_list[image_name].keys():
            metric = {
                "name": "so_vulnerabilities",
                "action": "set",
                "value": vul_list[image_name][severity],
                "labels": {
                    "image": image_name,
                    "severity": severity
                }
            }
            line = json.dumps(metric)
            metric_file.write(line + "\n")
