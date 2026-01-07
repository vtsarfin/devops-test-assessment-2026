# DevOps Test Assessment Project

## Vadim Tsarfin, January 2026

# DevOps Test Assessment (2026)

This repo contains my solution for the DevOps homework assignment.
My goal was to ship a small web API as a container, run it on Kubernetes, and keep it easy to build, run, and test.

> Copy/paste the commands. Everything explained could be easy reproduced on any modern Linux or MacOS system.

---

## Stack

### Python framework

- [**FastAPI**](https://github.com/fastapi/fastapi)

  - Fast start, wide spread across developers all over the world
  - Built-in OpenAPI + Swagger UI (`/docs`) means the API is self-documented automatically.
  - Async-friendly and production-ready
  - Easy deployment by [uv](https://github.com/astral-sh/uv) (see below)

### Python tooling

- [**uv**](https://github.com/astral-sh/uv)
  - new and fast-growing, but already mature enough
  - One tool for everything: `venv`, `pyenv`, `pyenv-virtualenv`; in the same time, compatible with `pip`/`pipx`. No compilation of Python interpreter itself, unlike `pyenv`.

### Container

- **Docker-desktop**
  - Just fast and simple for test Assessment; nothing specific was used.
  - Same artifact for local runs and Kubernetes.

### Kubernetes

- **kubeadm** 1-node cluster; nothing specific used
- **Manifests + Kustomize overlays**
  - Base resources are shared.
  - Overlays allow different settings for dev/prod (image tags, ports, replicas, etc.).
  - Cloud CD-ready (i.g. ArgoCD) technology

---

## Quick start (local)

### 1 Requirements

- `uv`
- docker
- Kubernetes

### 2 Clone the repo and install deps

```bash
git clone git@github.com:vtsarfin/devops-test-assessment-2026.git
cd devops-test-assessment-2026
uv sync
```

### 3 Build the image and run it locally

```bash
docker build . -t test-assessment:v0.94
docker run -e "TOKEN=lampas" --rm -d -p 9000:80 test-assessment:v0.94
```

Smoke test (see detailed endpoints description below):

```bash
curl "http://localhost:9000/healthz/?token=lampas" 
```

Result:

```
{"status":"ok"}
```

### 4 Kubernetes deployment

Check current context:

```
alias k=kubectl
k config current-context
```

(docker-desktop in my case)

Deploy everything with Kustomize. We have 2 overlays: _prod_ and _dev_ which could be used simultaneously and isolated by namespaces.
For preliminary cleanup it's normal to destroy both NS: `k delete ns lta-prod lta-dev`
Let's deploy _prod_:

```bash
cd k8s/kustomize
k apply -k overlays/prod
```

The output has to be like:

```
namespace/lta-prod created
secret/token-secret created
service/test-assessment created
deployment.apps/test-assessment created
```

Check deployment's readiness :

```bash
k -n lta-prod get deployment
```

Normal output is like:

```
NAME              READY   UP-TO-DATE   AVAILABLE   AGE
test-assessment   3/3     3            3           3m49s
```

Check out all the resources deployed:

```bash
k -n lta-prod get all
```

Output:

```
NAME                                   READY   STATUS    RESTARTS   AGE
pod/test-assessment-84dd76445b-6xhnm   1/1     Running   0          6m18s
pod/test-assessment-84dd76445b-7t25z   1/1     Running   0          6m18s
pod/test-assessment-84dd76445b-rdvhp   1/1     Running   0          6m18s

NAME                      TYPE       CLUSTER-IP     EXTERNAL-IP   PORT(S)        AGE
service/test-assessment   NodePort   10.101.5.184   <none>        80:30080/TCP   6m18s

NAME                              READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/test-assessment   3/3     3            3           6m18s

NAME                                         DESIRED   CURRENT   READY   AGE
replicaset.apps/test-assessment-84dd76445b   3         3         3       6m18s
```

## Workload Functionality

### Embedded documentation

To explore endpoints using embedded FastAPI documentation, open in browser:
[http://localhost:30080/docs](http://localhost:30080/docs)

### Health and Metrics

`/healthz/` endpoint provides simple status message and is used for health and readiness probes in k8s:

```bash
curl "http://localhost:30080/healthz/"
```

```
{"status":"ok"}%
```

`/today/` and `/version/` return the actual date and version of workload requiring simple plaintext token comparing with k8s secret value:

```
curl "http://localhost:30080/version/?token=lampas"
```

```
{"Version":"0.9"}
```

```
curl "http://localhost:30080/today/?token=lampas"
```

```
{"today":"2026-01-07"}
```

`/metrics` endpoint returns a lot of ready to use metrics in [Prometheus](https://prometheus.io/) format:

```
curl "http://localhost:30080/metrics"
```

```
# HELP python_gc_objects_collected_total Objects collected during gc
# TYPE python_gc_objects_collected_total counter
python_gc_objects_collected_total{generation="0"} 0.0
python_gc_objects_collected_total{generation="1"} 318.0
python_gc_objects_collected_total{generation="2"} 0.0
# HELP python_gc_objects_uncollectable_total Uncollectable objects found during GC
# TYPE python_gc_objects_uncollectable_total counter
python_gc_objects_uncollectable_total{generation="0"} 0.0
python_gc_objects_uncollectable_total{generation="1"} 0.0
python_gc_objects_uncollectable_total{generation="2"} 0.0
# HELP python_gc_collections_total Number of times this generation was collected
# TYPE python_gc_collections_total counter
python_gc_collections_total{generation="0"} 0.0
python_gc_collections_total{generation="1"} 12.0
python_gc_collections_total{generation="2"} 0.0
# HELP python_info Python platform information
# TYPE python_info gauge
python_info{implementation="CPython",major="3",minor="14",patchlevel="2",version="3.14.2"} 1.0
```

(cut)

## Bonus Items implementation

- /healthz/ endpoint
- /metrics endpoint with production-ready Prometheus metrics
- _token-secret_ k8s secret is used to keep token value
- non-root user  used in Docker image
- slim python image was chosen
- Kustomize is used for k8s deployment
- simple automation: `all_in_one_deployment.sh` could be used to install everything at once and run check all the endpoints:

```
chmod +x ./all-in-one-deployment.sh
./all-in-one-deployment.sh
```
