from typing import List, Optional

from kubernetes.client import (
    AppsV1Api,
    V1Deployment,
    V1DeploymentList,
    V1Scale,
    exceptions,
)
from kubernetes.utils import create_from_yaml

from .resource_api import ResourceApi


class Deployment(ResourceApi[AppsV1Api]):
    """
    A class to manage the Kubernetes Deployment resource.
    """

    api_client_type = AppsV1Api

    def get(self, namespace: str, name: str) -> Optional[V1Deployment]:
        deployment = None
        try:
            deployment = self.api_client.read_namespaced_deployment(
                name=name, namespace=namespace
            )
        except exceptions.ApiException as e:
            self._logger.error(
                f"Failed to get deployment {name} in namespace {namespace}: {e}"
            )

        return deployment

    def list(self, namespace: str) -> Optional[V1DeploymentList]:
        deployments = None
        try:
            deployments = self.api_client.list_namespaced_deployment(
                namespace=namespace
            )
        except exceptions.ApiException as e:
            self._logger.error(
                f"Failed to list deployments in namespace {namespace}: {e}"
            )

        return deployments

    def create(self, namespace: str, body: V1Deployment) -> Optional[V1Deployment]:
        created_deployment = None
        try:
            created_deployment = self.api_client.create_namespaced_deployment(
                namespace=namespace, body=body
            )
        except exceptions.ApiException as e:
            self._logger.error(
                f"Failed to create deployment {body.metadata.name} in namespace {namespace}: {e}"
            )

        return created_deployment

    def delete(self, namespace: str, name: str) -> Optional[V1Deployment]:
        deleted_deployment = None
        try:
            deleted_deployment = self.api_client.delete_namespaced_deployment(
                name=name, namespace=namespace
            )
        except exceptions.ApiException as e:
            self._logger.error(
                f"Failed to delete deployment {name} in namespace {namespace}: {e}"
            )

        return deleted_deployment

    def patch(
        self, namespace: str, name: str, body: V1Deployment
    ) -> Optional[V1Deployment]:
        patched_deployment = None
        try:
            patched_deployment = self.api_client.patch_namespaced_deployment(
                name=name, namespace=namespace, body=body
            )
        except exceptions.ApiException as e:
            self._logger.error(
                f"Failed to patch deployment {name} in namespace {namespace}: {e}"
            )

        return patched_deployment

    def update(
        self, namespace: str, name: str, body: V1Deployment
    ) -> Optional[V1Deployment]:
        updated_deployment = None
        try:
            updated_deployment = self.api_client.replace_namespaced_deployment(
                name=name, namespace=namespace, body=body
            )
        except exceptions.ApiException as e:
            self._logger.error(
                f"Failed to update deployment {name} in namespace {namespace}: {e}"
            )

        return updated_deployment

    def scale(self, namespace: str, name: str, replicas: int) -> Optional[V1Scale]:
        scaled_deployment = None
        try:
            scaled_deployment = self.api_client.patch_namespaced_deployment_scale(
                name=name, namespace=namespace, body={"spec": {"replicas": replicas}}
            )
        except exceptions.ApiException as e:
            self._logger.error(
                f"Failed to scale deployment {name} in namespace {namespace}: {e}"
            )

        return scaled_deployment

    def create_from_yaml(
        self, namespace: str, yaml_file_path: str
    ) -> Optional[List[V1Deployment]]:
        created_deployment = None
        try:
            created_deployment = create_from_yaml(
                self.api_client, yaml_file_path, namespace=namespace
            )
        except exceptions.ApiException as e:
            self._logger.error(
                f"Failed to create deployment from yaml in namespace {namespace}: {e}"
            )

        return created_deployment

    def is_ready(self, namespace: str, name: str) -> bool:
        deployment = self.get(namespace, name)
        if deployment is None:
            return False

        return deployment.status.ready_replicas == deployment.status.replicas
