#!/bin/bash

kubectl apply --wait -f src/crd/minio.yaml
kubectl apply --wait -f src/crd/argo.yaml
sleep 5

kubectl apply --wait -f src/services/minio.yaml
kubectl apply --wait -n argo -f src/services/argo.yaml
sleep 5
