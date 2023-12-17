from typing import List, Optional

from kubernetes.client import (
    AppsV1Api,
    V1Scale,
    V1StatefulSet,
    V1StatefulSetList,
    exceptions,
)
from kubernetes.utils import create_from_yaml

from .resource_api import ResourceApi


class StatefulSet(ResourceApi[AppsV1Api]):
    """
    A class to manage the Kubernetes StatefulSet resource.
    """

    api_client_type = AppsV1Api

    def get(self, namespace: str, name: str) -> Optional[V1StatefulSet]:
        statefulset = None
        try:
            statefulset = self.api_client.read_namespaced_stateful_set(
                name=name, namespace=namespace
            )
        except exceptions.ApiException as e:
            self._logger.error(
                f"Failed to get statefulset {name} in namespace {namespace}: {e}"
            )

        return statefulset

    def list(self, namespace: str) -> Optional[V1StatefulSetList]:
        statefulsets = None
        try:
            statefulsets = self.api_client.list_namespaced_stateful_set(
                namespace=namespace
            )
        except exceptions.ApiException as e:
            self._logger.error(
                f"Failed to list statefulsets in namespace {namespace}: {e}"
            )

        return statefulsets

    def create(self, namespace: str, body: V1StatefulSet) -> Optional[V1StatefulSet]:
        created_statefulset = None
        try:
            created_statefulset = self.api_client.create_namespaced_stateful_set(
                namespace=namespace, body=body
            )
        except exceptions.ApiException as e:
            self._logger.error(
                f"Failed to create statefulset {body.metadata.name} in namespace {namespace}: {e}"
            )

        return created_statefulset

    def delete(self, namespace: str, name: str) -> Optional[V1StatefulSet]:
        deleted_statefulset = None
        try:
            deleted_statefulset = self.api_client.delete_namespaced_stateful_set(
                name=name, namespace=namespace
            )
        except exceptions.ApiException as e:
            self._logger.error(
                f"Failed to delete statefulset {name} in namespace {namespace}: {e}"
            )

        return deleted_statefulset

    def patch(
        self, namespace: str, name: str, body: V1StatefulSet
    ) -> Optional[V1StatefulSet]:
        patched_statefulset = None
        try:
            patched_statefulset = self.api_client.patch_namespaced_stateful_set(
                name=name, namespace=namespace, body=body
            )
        except exceptions.ApiException as e:
            self._logger.error(
                f"Failed to patch statefulset {name} in namespace {namespace}: {e}"
            )

        return patched_statefulset

    def update(
        self, namespace: str, name: str, body: V1StatefulSet
    ) -> Optional[V1StatefulSet]:
        updated_statefulset = None
        try:
            updated_statefulset = self.api_client.replace_namespaced_stateful_set(
                name=name, namespace=namespace, body=body
            )
        except exceptions.ApiException as e:
            self._logger.error(
                f"Failed to update statefulset {name} in namespace {namespace}: {e}"
            )

        return updated_statefulset

    def scale(self, namespace: str, name: str, replicas: int) -> Optional[V1Scale]:
        scaled_statefulset = None
        try:
            scaled_statefulset = self.api_client.patch_namespaced_stateful_set_scale(
                name=name, namespace=namespace, body={"spec": {"replicas": replicas}}
            )
        except exceptions.ApiException as e:
            self._logger.error(
                f"Failed to scale statefulset {name} in namespace {namespace}: {e}"
            )

        return scaled_statefulset

    def create_from_yaml(
        self, namespace: str, yaml_file_path: str
    ) -> Optional[List[V1StatefulSet]]:
        created_statefulset = None
        try:
            created_statefulset = create_from_yaml(
                self.api_client, yaml_file_path, namespace=namespace
            )
        except exceptions.ApiException as e:
            self._logger.error(
                f"Failed to create statefulset from yaml in namespace {namespace}: {e}"
            )

        return created_statefulset

    def is_ready(self, namespace: str, name: str) -> bool:
        statefulset = self.get(namespace, name)
        if statefulset is None:
            return False

        return statefulset.status.ready_replicas == statefulset.status.replicas
