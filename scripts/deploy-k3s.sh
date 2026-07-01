#!/usr/bin/env bash
set -euo pipefail

NAMESPACE="${NAMESPACE:-content-platform}"
RELEASE="${RELEASE:-content-platform}"
CHART="${CHART:-deploy/helm}"

command -v kubectl >/dev/null || { echo "kubectl is required" >&2; exit 1; }
command -v helm >/dev/null || { echo "helm is required" >&2; exit 1; }

kubectl create namespace "$NAMESPACE" --dry-run=client -o yaml | kubectl apply -f -
helm upgrade --install "$RELEASE" "$CHART" -n "$NAMESPACE"
kubectl rollout status deployment/agennext-content-api -n "$NAMESPACE" --timeout=180s
kubectl rollout status deployment/agennext-content-dashboard -n "$NAMESPACE" --timeout=180s
kubectl get pods -n "$NAMESPACE"

echo "deployed $RELEASE in namespace $NAMESPACE"
