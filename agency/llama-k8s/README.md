# Agentic AI Kubernetes Operator

An Agentic AI Operator designed to manage, troubleshoot, and automate local managed Kubernetes hosting environments. This operator runs autonomously within your cluster, monitors the health of your workloads, and utilizes local LLM inference engines (Data Sovereign Agentic Reasoning) to diagnose issues, draft remediation plans, and selectively execute safe actions.

## Architecture

The system utilizes a multi-agent architecture coordinated by a central routing loop, all implemented within a single unified script (`operator.py`):

1. **Operations Coordinator (Router)**: The main control loop. It polls the cluster for state changes, orchestrates specialized agents, and uses the LLM to verify if proposed remediations are safe for autonomous execution (e.g., restarting stateless pods) or if they require human review.
2. **Log & Telemetry Analyst**: Queries Kubernetes for pod statuses and events within monitored namespaces. It passes telemetry data to the LLM to detect anomalies and flag problematic pods.
3. **Incident Responder**: Triggered by the Analyst. It fetches detailed pod logs and asks the LLM for a root cause analysis and a proposed remediation action (like `restart_pod` or `rollback_deployment`).
4. **GitOps Manager**: Connects to the Argo CD API to check application sync statuses and health. It also has capabilities to analyze GitOps Pull Requests to determine the risk of deploying changes across DTAP environments.

## Data Sovereignty & Routing Hooks

This operator is built to interface with local OpenAI-compatible inference endpoints (such as `llama-server` or `vLLM`). To guarantee data sovereignty, all agent decision-making requests are explicitly routed through a dedicated hook (`route_to_local_inference`). Cluster logs, event data, and infrastructure state are never sent to external cloud APIs, ensuring your sensitive infrastructure data never leaves the local environment.

## Prerequisites

- A Kubernetes cluster.
- An instance of a local LLM API accessible from within the cluster (e.g., `http://llama-server.default.svc.cluster.local:8080/v1`).
- (Optional) Argo CD running in the cluster.

## Configuration

The operator is configured entirely via environment variables:

| Variable | Description | Default |
| -------- | ----------- | ------- |
| `LLM_API_BASE` | URL to the local LLM endpoint | `http://llama-server.default.svc.cluster.local:8080/v1` |
| `LLM_MODEL_NAME` | The name of the model being served | `llama-3` |
| `LLM_API_KEY` | API key if the local server requires it | `dummy-key` |
| `ARGOCD_URL` | Base URL of the Argo CD server | `http://argocd-server.argocd.svc.cluster.local` |
| `ARGOCD_TOKEN` | Bearer token for Argo CD API access | `""` |
| `POLLING_INTERVAL_SECONDS` | How often the control loop runs (seconds) | `60` |

## Deployment

The operator runs as a Deployment inside your Kubernetes cluster.

1. **Build the container image**:
   ```bash
   docker build -t your-registry/ai-operator:latest .
   docker push your-registry/ai-operator:latest
   ```
   *(Be sure to update `k8s_manifests/deployment.yaml` with your actual image repository)*

2. **Deploy to Kubernetes**:
   The operator requires specific RBAC permissions (defined in `rbac.yaml`) to read logs, list pods, and execute basic rollout commands.
   
   ```bash
   kubectl apply -f k8s_manifests/rbac.yaml
   kubectl apply -f k8s_manifests/deployment.yaml
   ```

3. **Monitor Logs**:
   ```bash
   kubectl logs -l app=ai-operator -n kube-system -f
   ```

## Local Development

If you wish to test the operator locally outside of a cluster (assuming you have a valid `~/.kube/config` and access to your LLM API):

```bash
pip install -r requirements.txt
python operator.py
```
