from typing import List, Optional

from kubernetes.client import CoreV1Api, V1Pod, V1PodList, exceptions
from kubernetes.utils import create_from_yaml

from .resource_api import ResourceApi


class Pod(ResourceApi[CoreV1Api]):
    """
    A class to manage the Kubernetes Pod resource.
    """

    api_client_type = CoreV1Api

    def get(self, namespace: str, name: str) -> Optional[V1Pod]:
        pod = None
        try:
            pod = self.api_client.read_namespaced_pod(name=name, namespace=namespace)
        except exceptions.ApiException as e:
            self._logger.error(
                f"Failed to get pod {name} in namespace {namespace}: {e}"
            )

        return pod

    def list(self, namespace: str) -> Optional[V1PodList]:
        pods = None
        try:
            pods = self.api_client.list_namespaced_pod(namespace=namespace)
        except exceptions.ApiException as e:
            self._logger.error(f"Failed to list pods in namespace {namespace}: {e}")

        return pods

    def create(self, namespace: str, body: V1Pod) -> Optional[V1Pod]:
        created_pod = None
        try:
            created_pod = self.api_client.create_namespaced_pod(
                namespace=namespace, body=body
            )
        except exceptions.ApiException as e:
            self._logger.error(
                f"Failed to create pod {body.metadata.name} in namespace {namespace}: {e}"
            )

        return created_pod

    def create_from_yaml(
        self, namespace: str, yaml_file_path: str
    ) -> Optional[List[V1Pod]]:
        created_pod = None
        try:
            created_pod = create_from_yaml(
                self.api_client, yaml_file_path, namespace=namespace
            )
        except exceptions.ApiException as e:
            self._logger.error(
                f"Failed to create pod from yaml in namespace {namespace}: {e}"
            )

        return created_pod

    def delete(self, namespace: str, name: str) -> Optional[V1Pod]:
        deleted_pod = None
        try:
            deleted_pod = self.api_client.delete_namespaced_pod(
                name=name, namespace=namespace
            )
        except exceptions.ApiException as e:
            self._logger.error(
                f"Failed to delete pod {name} in namespace {namespace}: {e}"
            )

        return deleted_pod

    def patch(self, namespace: str, name: str, body: V1Pod) -> Optional[V1Pod]:
        patched_pod = None
        try:
            patched_pod = self.api_client.patch_namespaced_pod(
                name=name, namespace=namespace, body=body
            )
        except exceptions.ApiException as e:
            self._logger.error(
                f"Failed to patch pod {name} in namespace {namespace}: {e}"
            )

        return patched_pod

    def update(self, namespace: str, name: str, body: V1Pod) -> Optional[V1Pod]:
        updated_pod = None
        try:
            updated_pod = self.api_client.replace_namespaced_pod(
                name=name, namespace=namespace, body=body
            )
        except exceptions.ApiException as e:
            self._logger.error(
                f"Failed to update pod {name} in namespace {namespace}: {e}"
            )

        return updated_pod

    def is_ready(self, namespace: str, name: str) -> bool:
        pod = self.get(namespace, name)
        if pod is None:
            return False

        return pod.status.phase == "Running"
