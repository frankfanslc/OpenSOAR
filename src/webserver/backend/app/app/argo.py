import base64
from functools import wraps
import json
import urllib3

import argo.workflows.client as argo
from fastapi import Depends
from fastapi.routing import APIRouter
from kubernetes import config, client

from .schemas import User


def is_httpresponse(f):
    @wraps(f)
    def inner(*args, **kwargs):
        r: urllib3.HTTPResponse = f(*args, **kwargs)
        return json.loads(r.data)

    return inner


def get_argo_router(fastapi_users):
    router = APIRouter()

    config.load_incluster_config()
    k8s = client.CoreV1Api()
    service_account = k8s.read_namespaced_service_account(
        namespace="default", name="fastapi"
    )
    secret_name = service_account.secrets[0].name
    secret = k8s.read_namespaced_secret(name=secret_name, namespace="default")
    token = base64.b64decode(secret.data["token"]).decode("utf-8")

    argo_config = argo.Configuration(
        host="https://argo-server.argo.svc.cluster.local:2746"
    )
    argo_config.verify_ssl = False
    argo_client = argo.ApiClient(
        configuration=argo_config,
        header_name="Authorization",
        header_value=f"Bearer {token}",
    )
    argo_client.client_side_validation = False
    archived_workflow = argo.ArchivedWorkflowServiceApi(api_client=argo_client)
    cluster_workflow_template = argo.ClusterWorkflowTemplateServiceApi(
        api_client=argo_client
    )
    cron_workflow = argo.CronWorkflowServiceApi(api_client=argo_client)
    event = argo.EventServiceApi(api_client=argo_client)
    info = argo.InfoServiceApi(api_client=argo_client)
    workflow = argo.WorkflowServiceApi(api_client=argo_client)
    workflow_template = argo.WorkflowTemplateServiceApi(api_client=argo_client)

    @router.get("/archived-workflows")
    @is_httpresponse
    def list_archived_workflows(
        user: User = Depends(fastapi_users.current_user(active=True)),
    ):
        return archived_workflow.list_archived_workflows(_preload_content=False)

    @router.get("/archived-workflows/{uid}")
    @is_httpresponse
    def get_archived_workflow(uid):
        return archived_workflow.get_archived_workflow(uid, _preload_content=False)

    @router.delete("/archived-workflows/{uid}")
    @is_httpresponse
    def delete_archived_workflow(uid):
        return archived_workflow.delete_archived_workflow(uid, _preload_content=False)

    @router.get("/cluster-workflow-templates")
    @is_httpresponse
    def list_cluster_workflow_templates():
        return cluster_workflow_template.list_cluster_workflow_templates(
            _preload_content=False
        )

    @router.get("/cluster-workflow-templates/{name}")
    @is_httpresponse
    def get_cluster_workflow_template(name):
        return cluster_workflow_template.get_cluster_workflow_template(
            name, _preload_content=False
        )

    @router.post("/cluster-workflow-templates/lint")
    @is_httpresponse
    def lint_cluster_workflow_template(body):
        return cluster_workflow_template.lint_cluster_workflow_template(
            body, _preload_content=False
        )

    @router.post("/cluster-workflow-templates")
    @is_httpresponse
    def create_cluster_workflow_template(body):
        return cluster_workflow_template.create_cluster_workflow_template(
            body, _preload_content=False
        )

    @router.post("/cluster-workflow-templates/{name}")
    @is_httpresponse
    def update_cluster_workflow_template(name, body):
        return cluster_workflow_template.update_cluster_workflow_template(
            name, body, _preload_content=False
        )

    @router.delete("/cluster-workflow-templates/{name}")
    @is_httpresponse
    def delete_cluster_workflow_template(name):
        return cluster_workflow_template.delete_cluster_workflow_template(
            name, _preload_content=False
        )

    @router.get("/cron-workflows")
    @is_httpresponse
    def list_cron_workflows(
        user: User = Depends(fastapi_users.current_user(active=True, superuser=True))
    ):
        return cron_workflow.list_cron_workflows(
            namespace="default", _preload_content=False
        )

    @router.get("/cron-workflows/{name}")
    @is_httpresponse
    def get_cron_workflows(name):
        return cron_workflow.get_cron_workflow(
            namespace="default", name=name, _preload_content=False
        )

    @router.post("/cron-workflows/lint")
    @is_httpresponse
    def lint_cron_workflows(body):
        return cron_workflow.lint_cron_workflow(
            namespace="default", body=body, _preload_content=False
        )

    @router.post("/cron-workflows")
    @is_httpresponse
    def create_cron_workflows(body):
        return cron_workflow.create_cron_workflow(
            namespace="default", body=body, _preload_content=False
        )

    @router.post("/cron-workflows/{name}")
    @is_httpresponse
    def update_cron_workflows(name, body):
        return cron_workflow.update_cron_workflow(
            namespace="default", name=name, body=body, _preload_content=False
        )

    @router.delete("/cron-workflows/{name}")
    @is_httpresponse
    def delete_cron_workflows(name):
        return cron_workflow.delete_cron_workflow(
            namespace="default", name=name, _preload_content=False
        )

    @router.post("/events/{discriminator}")
    @is_httpresponse
    def receive_event(discriminator, body):
        return event.receive_event(
            namespace="default",
            discriminator=discriminator,
            body=body,
            _preload_content=False,
        )

    @router.get("/info")
    @is_httpresponse
    def get_info():
        return info.get_info(_preload_content=False)

    @router.get("/userinfo")
    @is_httpresponse
    def get_userinfo():
        return info.get_user_info(_preload_content=False)

    @router.get("/version")
    @is_httpresponse
    def get_version():
        return info.get_version(_preload_content=False)

    @router.get("/workflows")
    @is_httpresponse
    def list_workflows(user: User = Depends(fastapi_users.current_user(active=True))):
        return workflow.list_workflows(namespace="default", _preload_content=False)

    @router.get("/workflows/{name}")
    @is_httpresponse
    def get_workflow(name):
        return workflow.get_workflow(
            namespace="default", name=name, _preload_content=False
        )

    @router.post("/workflows/lint")
    @is_httpresponse
    def lint_workflow(body):
        return cron_workflow.lint_cron_workflow(
            namespace="default", body=body, _preload_content=False
        )

    @router.post("/workflows")
    @is_httpresponse
    def create_workflow(body):
        return workflow.create_workflow(
            namespace="default", body=body, _preload_content=False
        )

    @router.delete("/workflows/{name}")
    @is_httpresponse
    def delete_workflow(name):
        return workflow.delete_workflow(
            namespace="default", name=name, _preload_content=False
        )

    @router.get("/workflows/{name}/{pod_name}/log")
    @is_httpresponse
    def get_podlogs(name, pod_name):
        return workflow.pod_logs(namespace="default", name=name, pod_name=pod_name)

    @router.put("/workflows/{name}/resubmit")
    @is_httpresponse
    def resubmit_workflow(name, body):
        return workflow.resubmit_workflow(namespace="default", name=name, body=body)

    @router.put("/workflows/{name}/resume")
    @is_httpresponse
    def resume_workflow(name, body):
        return workflow.resume_workflow(namespace="default", name=name, body=body)

    @router.put("/workflows/{name}/retry")
    @is_httpresponse
    def retry_workflow(name, body):
        return workflow.retry_workflow(namespace="default", name=name, body=body)

    @router.put("/workflows/{name}/set")
    @is_httpresponse
    def set_workflow(name, body):
        return workflow.set_workflow(namespace="default", name=name, body=body)

    @router.put("/workflows/{name}/stop")
    @is_httpresponse
    def stop_workflow(name, body):
        return workflow.stop_workflow(namespace="default", name=name, body=body)

    @router.post("/workflows/{name}/submit")
    @is_httpresponse
    def submit_workflow(name, body):
        return workflow.submit_workflow(namespace="default", name=name, body=body)

    @router.put("/workflows/{name}/suspend")
    @is_httpresponse
    def suspend_workflow(name, body):
        return workflow.suspend_workflow(namespace="default", name=name, body=body)

    @router.put("/workflows/{name}/terminate")
    @is_httpresponse
    def terminate_workflow(name, body):
        return workflow.terminate_workflow(namespace="default", name=name, body=body)

    @router.get("/stream/events")
    @is_httpresponse
    def watch_events():
        return workflow.watch_events(namespace="default")

    @router.get("/workflow-events")
    @is_httpresponse
    def watch_workflows():
        return workflow.watch_workflows(namespace="default")

    @router.post("/workflow-templates")
    @is_httpresponse
    def create_workflow_template(body):
        return workflow_template.create_workflow_template(
            namespace="default", body=body
        )

    @router.delete("/workflow-templates/{name}")
    @is_httpresponse
    def delete_workflow_template(name):
        return workflow_template.delete_workflow_template(
            namespace="default", name=name
        )

    @router.get("/workflow-templates/{name}")
    @is_httpresponse
    def get_workflow_template(name):
        return workflow_template.get_workflow_template(namespace="default", name=name)

    @router.post("/workflow-templates/lint")
    @is_httpresponse
    def lint_workflow_template(body):
        return workflow_template.lint_workflow_template(namespace="default", body=body)

    @router.get("/workflow-templates")
    @is_httpresponse
    def list_workflow_templates():
        return workflow_template.list_workflow_templates(namespace="default")

    @router.put("/workflow-templates/name}")
    @is_httpresponse
    def update_workflow_templates(name, body):
        return workflow_template.update_workflow_template(
            namespace="default", name=name, body=body
        )

    return router
