from typing import List, Optional

from kubernetes.client import (
    AppsV1Api,
    V1ReplicaSet,
    V1ReplicaSetList,
    V1Scale,
    exceptions,
)
from kubernetes.utils import create_from_yaml

from .resource_api import ResourceApi


class ReplicaSet(ResourceApi[AppsV1Api]):
    """
    A class to manage the Kubernetes ReplicaSet resource.
    """

    api_client_type = AppsV1Api

    def get(self, namespace: str, name: str) -> Optional[V1ReplicaSet]:
        replicaset = None
        try:
            replicaset = self.api_client.read_namespaced_replica_set(
                name=name, namespace=namespace
            )
        except exceptions.ApiException as e:
            self._logger.error(
                f"Failed to get replicaset {name} in namespace {namespace}: {e}"
            )

        return replicaset

    def list(self, namespace: str) -> Optional[V1ReplicaSetList]:
        replicasets = None
        try:
            replicasets = self.api_client.list_namespaced_replica_set(
                namespace=namespace
            )
        except exceptions.ApiException as e:
            self._logger.error(
                f"Failed to list replicasets in namespace {namespace}: {e}"
            )

        return replicasets

    def create(self, namespace: str, body: V1ReplicaSet) -> Optional[V1ReplicaSet]:
        created_replicaset = None
        try:
            created_replicaset = self.api_client.create_namespaced_replica_set(
                namespace=namespace, body=body
            )
        except exceptions.ApiException as e:
            self._logger.error(
                f"Failed to create replicaset {body.metadata.name} in namespace {namespace}: {e}"
            )

        return created_replicaset

    def delete(self, namespace: str, name: str) -> Optional[V1ReplicaSet]:
        deleted_replicaset = None
        try:
            deleted_replicaset = self.api_client.delete_namespaced_replica_set(
                name=name, namespace=namespace
            )
        except exceptions.ApiException as e:
            self._logger.error(
                f"Failed to delete replicaset {name} in namespace {namespace}: {e}"
            )

        return deleted_replicaset

    def patch(
        self, namespace: str, name: str, body: V1ReplicaSet
    ) -> Optional[V1ReplicaSet]:
        patched_replicaset = None
        try:
            patched_replicaset = self.api_client.patch_namespaced_replica_set(
                name=name, namespace=namespace, body=body
            )
        except exceptions.ApiException as e:
            self._logger.error(
                f"Failed to patch replicaset {name} in namespace {namespace}: {e}"
            )

        return patched_replicaset

    def update(
        self, namespace: str, name: str, body: V1ReplicaSet
    ) -> Optional[V1ReplicaSet]:
        updated_replicaset = None
        try:
            updated_replicaset = self.api_client.replace_namespaced_replica_set(
                name=name, namespace=namespace, body=body
            )
        except exceptions.ApiException as e:
            self._logger.error(
                f"Failed to update replicaset {name} in namespace {namespace}: {e}"
            )

        return updated_replicaset

    def scale(self, namespace: str, name: str, replicas: int) -> Optional[V1Scale]:
        scaled_replicaset = None
        try:
            scaled_replicaset = self.api_client.replace_namespaced_replica_set_scale(
                name=name, namespace=namespace, body={"spec": {"replicas": replicas}}
            )
        except exceptions.ApiException as e:
            self._logger.error(
                f"Failed to scale replicaset {name} in namespace {namespace}: {e}"
            )

        return scaled_replicaset

    def create_from_yaml(
        self, namespace: str, yaml_file_path: str
    ) -> Optional[List[V1ReplicaSet]]:
        created_replicaset = None
        try:
            created_replicaset = create_from_yaml(
                self.api_client, yaml_file_path, namespace=namespace
            )
        except exceptions.ApiException as e:
            self._logger.error(
                f"Failed to create replicaset from yaml in namespace {namespace}: {e}"
            )

        return created_replicaset

    def is_ready(self, namespace: str, name: str) -> bool:
        replicaset = self.get(namespace, name)
        if replicaset is None:
            return False

        ready_replicas = replicaset.status.ready_replicas
        desired_replicas = replicaset.spec.replicas
        return ready_replicas == desired_replicas
