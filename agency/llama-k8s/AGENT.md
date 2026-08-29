# Kubernetes AI Operator Integration Guide for Agents

This guide provides instructions for AI agents on how to integrate and deploy the Agentic AI Kubernetes Operator into a target cluster.

## Objective
Deploy the `ai-operator` into the `kube-system` namespace, ensure it is configured to route decisions to a local LLM inference server (for data sovereignty), and verify its operation.

## Prerequisites Verification
Before proceeding, an agent MUST verify:
1. `kubectl` is authenticated to the target cluster.
2. A local LLM inference endpoint is accessible within the cluster (e.g., `llama-server` or `vLLM`).
3. (Optional) Argo CD is running if GitOps management is required.

## Configuration Instructions
When preparing the deployment, ensure the environment variables in `k8s_manifests/deployment.yaml` correctly point to the local infrastructure:

- `LLM_API_BASE`: Must be updated to the internal cluster DNS of the local LLM server (e.g., `http://llama-server.default.svc.cluster.local:8080/v1`). **Never route this to a public cloud API like `api.openai.com`.**
- `LLM_MODEL_NAME`: Must match the model served by the local inference engine.
- `ARGOCD_URL`: Must be set to the internal Argo CD server URL.

## Deployment Steps
Execute the following steps sequentially to deploy the operator:

1. **Build and Push the Image**:
   Build the Dockerfile and push it to a registry accessible by the cluster. Update the `image:` tag in `k8s_manifests/deployment.yaml` with the pushed image location.
   
2. **Apply RBAC Permissions**:
   The operator requires broad read access and specific write access to investigate logs and execute remediations.
   ```bash
   kubectl apply -f k8s_manifests/rbac.yaml
   ```

3. **Apply the Deployment**:
   ```bash
   kubectl apply -f k8s_manifests/deployment.yaml
   ```

## Verification & Post-Deployment Checks
After deployment, an agent MUST verify the operator is functioning correctly:

1. **Check Pod Status**:
   ```bash
   kubectl get pods -n kube-system -l app=ai-operator
   ```
   Ensure the pod is in a `Running` state.

2. **Verify Local Routing Logs**:
   Read the logs of the operator pod to ensure it is explicitly hooking into the local inference engine. Look for the log line: `"Routing agent decision-making to local LLM server at..."`
   ```bash
   kubectl logs -n kube-system -l app=ai-operator | grep "Routing"
   ```
   If this log is not present when an event occurs, the routing configuration is incorrect and must be fixed.

3. **Test Cluster Anomaly**:
   You can verify the operator's response by intentionally creating a failing pod in the `default` namespace and watching the `ai-operator` logs to observe the Log Analyst and Incident Responder agents diagnosing the issue.
