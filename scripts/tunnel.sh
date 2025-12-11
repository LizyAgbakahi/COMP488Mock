#!/usr/bin/env bash
set -euo pipefail

NAMESPACE="default"

echo "[*] Starting Kubernetes port-forward tunnels in namespace: ${NAMESPACE}"
echo ""
echo "  Frontend   -> http://localhost:8080"
echo ""
echo "Press Ctrl+C to stop the tunnel."

# Frontend: local 8080 -> service port 80
kubectl port-forward svc/frontend 8080:80 -n "${NAMESPACE}" &
PF1=$!

trap "echo 'Stopping tunnel...'; kill $PF1 2>/dev/null || true" INT TERM

wait
