#!/usr/bin/env bash
VERSION=v0.94
ENV=prod
PORT=30080
TOKEN=lampas
IMAGE=test-assignment
uv sync
docker build . -t $IMAGE:$VERSION
kubectl config use-context docker-desktop
kubectl delete ns lta-$ENV
kubectl apply -k k8s/kustomize/overlays/$ENV
sleep 20
curl --silent "http://localhost:30080/"
curl --silent "http://localhost:30080/metrics"
curl --silent "http://localhost:$PORT/healthz"
curl --silent "http://localhost:$PORT/today/?token=$TOKEN"
curl --silent "http://localhost:$PORT/version/?token=$TOKEN"
