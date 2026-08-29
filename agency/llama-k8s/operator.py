import os
import time
import json
import logging
import datetime
import requests
from pydantic import BaseModel, Field
from openai import OpenAI
from kubernetes import client, config
from kubernetes.stream import stream

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

# ==========================================
# Config
# ==========================================
class Settings(BaseModel):
    # LLM Settings
    llm_api_base: str = Field(default=os.getenv("LLM_API_BASE", "http://llama-server.default.svc.cluster.local:8080/v1"))
    llm_model_name: str = Field(default=os.getenv("LLM_MODEL_NAME", "llama-3"))
    llm_api_key: str = Field(default=os.getenv("LLM_API_KEY", "dummy-key"))

    # Argo CD Settings
    argocd_url: str = Field(default=os.getenv("ARGOCD_URL", "http://argocd-server.argocd.svc.cluster.local"))
    argocd_token: str = Field(default=os.getenv("ARGOCD_TOKEN", ""))

    # Polling Settings
    polling_interval_seconds: int = Field(default=int(os.getenv("POLLING_INTERVAL_SECONDS", "60")))

settings = Settings()

# ==========================================
# Core LLM Client
# ==========================================
class LLMClient:
    def __init__(self):
        self.client = OpenAI(
            base_url=settings.llm_api_base,
            api_key=settings.llm_api_key
        )
        self.model_name = settings.llm_model_name

    def route_to_local_inference(self, system_prompt: str, user_prompt: str, temperature: float = 0.2) -> str:
        """
        Explicit hook to route decision-making to a local LLM inference server 
        (like llama-server) instead of cloud APIs. Guarantees data sovereignty.
        """
        logger.debug(f"Routing agent decision-making to local LLM server at {settings.llm_api_base}")
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=temperature
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"[LLM ERROR] Failed to generate completion: {e}")
            return ""

# ==========================================
# Integrations
# ==========================================
class KubernetesClient:
    def __init__(self):
        try:
            config.load_incluster_config()
            logger.info("Loaded in-cluster Kubernetes config.")
        except config.ConfigException:
            try:
                config.load_kube_config()
                logger.info("Loaded local kubeconfig.")
            except Exception as e:
                logger.error(f"Failed to load Kubernetes configuration: {e}")
        
        self.core_v1 = client.CoreV1Api()
        self.apps_v1 = client.AppsV1Api()

    def get_pods(self, namespace: str = "default") -> list:
        try:
            pods = self.core_v1.list_namespaced_pod(namespace=namespace)
            return pods.items
        except Exception as e:
            logger.error(f"Error fetching pods in {namespace}: {e}")
            return []

    def get_pod_logs(self, pod_name: str, namespace: str = "default", tail_lines: int = 100) -> str:
        try:
            logs = self.core_v1.read_namespaced_pod_log(
                name=pod_name,
                namespace=namespace,
                tail_lines=tail_lines
            )
            return logs
        except Exception as e:
            logger.error(f"Error fetching logs for pod {pod_name}: {e}")
            return ""

    def exec_command(self, pod_name: str, namespace: str, command: list) -> str:
        try:
            resp = stream(
                self.core_v1.connect_get_namespaced_pod_exec,
                pod_name,
                namespace,
                command=command,
                stderr=True,
                stdin=False,
                stdout=True,
                tty=False
            )
            return resp
        except Exception as e:
            logger.error(f"Error executing command in pod {pod_name}: {e}")
            return str(e)

    def delete_pod(self, pod_name: str, namespace: str = "default") -> bool:
        try:
            self.core_v1.delete_namespaced_pod(name=pod_name, namespace=namespace)
            return True
        except Exception as e:
            logger.error(f"Error deleting pod {pod_name}: {e}")
            return False

    def restart_deployment(self, deployment_name: str, namespace: str = "default") -> bool:
        try:
            deployment = self.apps_v1.read_namespaced_deployment(name=deployment_name, namespace=namespace)
            if deployment.spec.template.metadata.annotations is None:
                deployment.spec.template.metadata.annotations = {}
            
            deployment.spec.template.metadata.annotations['kubectl.kubernetes.io/restartedAt'] = datetime.datetime.utcnow().isoformat() + "Z"
            self.apps_v1.patch_namespaced_deployment(
                name=deployment_name,
                namespace=namespace,
                body=deployment
            )
            return True
        except Exception as e:
            logger.error(f"Error restarting deployment {deployment_name}: {e}")
            return False

    def get_events(self, namespace: str = "default") -> list:
        try:
            events = self.core_v1.list_namespaced_event(namespace=namespace)
            return events.items
        except Exception as e:
            logger.error(f"Error fetching events in {namespace}: {e}")
            return []

class ArgoCDClient:
    def __init__(self):
        self.base_url = settings.argocd_url.rstrip("/")
        self.token = settings.argocd_token
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

    def get_applications(self) -> list:
        try:
            response = requests.get(f"{self.base_url}/api/v1/applications", headers=self.headers, timeout=10)
            response.raise_for_status()
            return response.json().get("items", [])
        except Exception as e:
            logger.error(f"Failed to fetch Argo CD applications: {e}")
            return []

    def get_application(self, app_name: str) -> dict:
        try:
            response = requests.get(f"{self.base_url}/api/v1/applications/{app_name}", headers=self.headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Failed to fetch Argo CD application {app_name}: {e}")
            return {}

    def sync_application(self, app_name: str) -> bool:
        try:
            response = requests.post(f"{self.base_url}/api/v1/applications/{app_name}/sync", headers=self.headers, timeout=10)
            response.raise_for_status()
            return True
        except Exception as e:
            logger.error(f"Failed to sync Argo CD application {app_name}: {e}")
            return False

    def rollback_application(self, app_name: str) -> bool:
        try:
            app = self.get_application(app_name)
            history = app.get("status", {}).get("history", [])
            if len(history) < 2:
                logger.error(f"Not enough history to rollback application {app_name}.")
                return False
            
            previous_history_id = history[-2].get("id")
            
            payload = {"id": previous_history_id}
            response = requests.post(
                f"{self.base_url}/api/v1/applications/{app_name}/rollback",
                headers=self.headers,
                json=payload,
                timeout=10
            )
            response.raise_for_status()
            return True
        except Exception as e:
            logger.error(f"Failed to rollback Argo CD application {app_name}: {e}")
            return False


# ==========================================
# Agents
# ==========================================
class GitOpsManager:
    def __init__(self, llm_client: LLMClient, argocd_client: ArgoCDClient):
        self.llm_client = llm_client
        self.argocd_client = argocd_client

    def analyze_dtap_impact(self, pr_diff: str, target_env: str) -> dict:
        system_prompt = (
            "You are an elite Kubernetes SRE. Analyze the following GitOps pull request diff "
            f"for a change targeting the {target_env} environment. Assess the risk level (Low, Medium, High) "
            "and determine if it is safe to auto-approve. Return your answer in JSON format with keys: "
            "'risk_level', 'auto_approve' (boolean), and 'reasoning'."
        )
        response = self.llm_client.route_to_local_inference(system_prompt, pr_diff)
        try:
            return json.loads(response)
        except Exception:
            return {"risk_level": "High", "auto_approve": False, "reasoning": "Failed to parse LLM response. " + response}

    def check_application_health(self) -> list:
        apps = self.argocd_client.get_applications()
        unhealthy_apps = []
        for app in apps:
            name = app.get("metadata", {}).get("name")
            status = app.get("status", {}).get("health", {}).get("status")
            sync_status = app.get("status", {}).get("sync", {}).get("status")
            
            if status != "Healthy" or sync_status != "Synced":
                unhealthy_apps.append({
                    "name": name,
                    "health": status,
                    "sync": sync_status
                })
        return unhealthy_apps

class LogTelemetryAnalyst:
    def __init__(self, llm_client: LLMClient, k8s_client: KubernetesClient):
        self.llm_client = llm_client
        self.k8s_client = k8s_client

    def analyze_namespace_health(self, namespace: str = "default") -> dict:
        pods = self.k8s_client.get_pods(namespace)
        events = self.k8s_client.get_events(namespace)
        
        pod_summaries = []
        for pod in pods:
            status = pod.status.phase
            restarts = sum([cs.restart_count for cs in pod.status.container_statuses]) if pod.status.container_statuses else 0
            pod_summaries.append(f"Pod: {pod.metadata.name}, Status: {status}, Restarts: {restarts}")
            
        event_summaries = [f"Event: {e.reason} - {e.message}" for e in events[-20:]]

        telemetry_data = (
            f"Namespace: {namespace}\n"
            f"Pods:\n" + "\n".join(pod_summaries) + "\n"
            f"Recent Events:\n" + "\n".join(event_summaries)
        )

        system_prompt = (
            "You are an AI Log & Telemetry Analyst for a Kubernetes cluster. "
            "Analyze the provided namespace telemetry (pod statuses, restarts, and events). "
            "Identify any anomalies or potential incidents. "
            "Return a JSON object with keys: "
            "'status' (Healthy, Degraded, Critical), "
            "'anomalies' (list of identified issues), "
            "'suspect_pods' (list of pod names that seem problematic)."
        )

        response = self.llm_client.route_to_local_inference(system_prompt, telemetry_data)
        
        try:
            clean_response = response.replace('```json', '').replace('```', '').strip()
            return json.loads(clean_response)
        except Exception as e:
            return {
                "status": "Unknown", 
                "anomalies": ["Failed to parse Analyst output.", str(e)],
                "suspect_pods": [],
                "raw_response": response
            }

class IncidentResponder:
    def __init__(self, llm_client: LLMClient, k8s_client: KubernetesClient):
        self.llm_client = llm_client
        self.k8s_client = k8s_client

    def investigate_pod(self, pod_name: str, namespace: str) -> str:
        logs = self.k8s_client.get_pod_logs(pod_name, namespace, tail_lines=200)
        
        system_prompt = (
            "You are a Kubernetes Incident Responder. "
            "Analyze the following pod logs. Identify the root cause of the crash or error. "
            "Draft a remediation plan. "
            "Return a JSON object with: "
            "'root_cause' (string), "
            "'remediation_action' (choose from: restart_pod, rollback_deployment, none, manual_intervention), "
            "'target_resource' (the name of the pod or deployment to act on), "
            "'explanation' (string explaining the reasoning)."
        )
        
        response = self.llm_client.route_to_local_inference(system_prompt, logs)
        try:
            clean_response = response.replace('```json', '').replace('```', '').strip()
            return json.loads(clean_response)
        except Exception:
            return {
                "root_cause": "Unknown",
                "remediation_action": "manual_intervention",
                "target_resource": pod_name,
                "explanation": "Failed to parse LLM response. " + response
            }

    def execute_remediation(self, action: str, target: str, namespace: str) -> bool:
        if action == "restart_pod":
            logger.info(f"[Responder] Deleting pod {target} in namespace {namespace} to force restart...")
            return self.k8s_client.delete_pod(target, namespace)
        elif action == "rollback_deployment":
            logger.info(f"[Responder] Restarting/rolling back deployment {target} in namespace {namespace}...")
            return self.k8s_client.restart_deployment(target, namespace)
        else:
            logger.info(f"[Responder] No automated execution for action: {action}")
            return False

# ==========================================
# Operations Coordinator (Main Loop)
# ==========================================
class OperationsCoordinator:
    def __init__(self):
        self.llm_client = LLMClient()
        self.k8s_client = KubernetesClient()
        self.argocd_client = ArgoCDClient()
        
        self.gitops = GitOpsManager(self.llm_client, self.argocd_client)
        self.analyst = LogTelemetryAnalyst(self.llm_client, self.k8s_client)
        self.responder = IncidentResponder(self.llm_client, self.k8s_client)

    def is_action_safe(self, incident_context: dict, remediation_plan: dict) -> bool:
        system_prompt = (
            "You are the Operations Coordinator (Router) for an AI Kubernetes Operator. "
            "Review the incident context and the proposed remediation plan. "
            "Determine if the remediation action is safe for AUTONOMOUS execution without human intervention. "
            "Safe actions include: restarting stateless pods, rolling back stateless deployments. "
            "Unsafe actions include: deleting PVCs/PVs, database modifications, cross-environment promotions. "
            "Respond in JSON format with a single boolean key 'is_safe' and a string key 'reason'."
        )
        
        prompt_data = json.dumps({
            "incident_context": incident_context,
            "remediation_plan": remediation_plan
        })
        
        response = self.llm_client.route_to_local_inference(system_prompt, prompt_data)
        try:
            clean_response = response.replace('```json', '').replace('```', '').strip()
            decision = json.loads(clean_response)
            return decision.get("is_safe", False)
        except Exception as e:
            logger.error(f"Failed to parse safety decision: {e}")
            return False

    def run_loop(self):
        logger.info("Starting Operations Coordinator control loop...")
        namespaces_to_monitor = ["default", "kube-system"]
        
        while True:
            logger.info("--- Beginning Observation Cycle ---")
            
            for ns in namespaces_to_monitor:
                logger.info(f"Analyzing namespace: {ns}")
                health_report = self.analyst.analyze_namespace_health(ns)
                logger.info(f"Health Report for {ns}: {health_report.get('status')}")
                
                if health_report.get("status") in ["Degraded", "Critical"]:
                    logger.warning(f"Anomalies detected in {ns}: {health_report.get('anomalies')}")
                    
                    for pod in health_report.get("suspect_pods", []):
                        logger.info(f"Triggering Incident Responder for pod: {pod}")
                        remediation_plan = self.responder.investigate_pod(pod, ns)
                        logger.info(f"Proposed Remediation: {remediation_plan}")
                        
                        if self.is_action_safe(health_report, remediation_plan):
                            logger.info(f"Action deemed SAFE. Executing autonomously: {remediation_plan.get('remediation_action')}")
                            success = self.responder.execute_remediation(
                                action=remediation_plan.get("remediation_action"),
                                target=remediation_plan.get("target_resource"),
                                namespace=ns
                            )
                            logger.info(f"Remediation Execution Success: {success}")
                        else:
                            logger.warning(f"Action deemed UNSAFE. Escalating to human for pod {pod}: {remediation_plan.get('remediation_action')}")
            
            logger.info("Checking Argo CD Application health...")
            unhealthy_apps = self.gitops.check_application_health()
            if unhealthy_apps:
                logger.warning(f"Found unhealthy Argo CD Apps: {unhealthy_apps}")
            
            logger.info(f"Sleeping for {settings.polling_interval_seconds} seconds...")
            time.sleep(settings.polling_interval_seconds)

if __name__ == "__main__":
    coordinator = OperationsCoordinator()
    coordinator.run_loop()
