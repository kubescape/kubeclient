from typing import List, Optional

from kubernetes.client import AppsV1Api, V1DaemonSet, V1DaemonSetList, exceptions
from kubernetes.utils import create_from_yaml

from .resource_api import ResourceApi


class DaemonSet(ResourceApi[AppsV1Api]):
    """
    A class to manage the Kubernetes DaemonSet resource.
    """

    api_client_type = AppsV1Api

    def get(self, namespace: str, name: str) -> Optional[V1DaemonSet]:
        daemonset = None
        try:
            daemonset = self.api_client.read_namespaced_daemon_set(
                name=name, namespace=namespace
            )
        except exceptions.ApiException as e:
            self._logger.error(
                f"Failed to get daemonset {name} in namespace {namespace}: {e}"
            )

        return daemonset

    def list(self, namespace: str) -> Optional[V1DaemonSetList]:
        daemonsets = None
        try:
            daemonsets = self.api_client.list_namespaced_daemon_set(namespace=namespace)
        except exceptions.ApiException as e:
            self._logger.error(
                f"Failed to list daemonsets in namespace {namespace}: {e}"
            )

        return daemonsets

    def create(self, namespace: str, body: V1DaemonSet) -> Optional[V1DaemonSet]:
        created_daemonset = None
        try:
            created_daemonset = self.api_client.create_namespaced_daemon_set(
                namespace=namespace, body=body
            )
        except exceptions.ApiException as e:
            self._logger.error(
                f"Failed to create daemonset {body.metadata.name} in namespace {namespace}: {e}"
            )

        return created_daemonset

    def delete(self, namespace: str, name: str) -> Optional[V1DaemonSet]:
        deleted_daemonset = None
        try:
            deleted_daemonset = self.api_client.delete_namespaced_daemon_set(
                name=name, namespace=namespace
            )
        except exceptions.ApiException as e:
            self._logger.error(
                f"Failed to delete daemonset {name} in namespace {namespace}: {e}"
            )

        return deleted_daemonset

    def patch(
        self, namespace: str, name: str, body: V1DaemonSet
    ) -> Optional[V1DaemonSet]:
        patched_daemonset = None
        try:
            patched_daemonset = self.api_client.patch_namespaced_daemon_set(
                name=name, namespace=namespace, body=body
            )
        except exceptions.ApiException as e:
            self._logger.error(
                f"Failed to patch daemonset {name} in namespace {namespace}: {e}"
            )

        return patched_daemonset

    def update(
        self, namespace: str, name: str, body: V1DaemonSet
    ) -> Optional[V1DaemonSet]:
        updated_daemonset = None
        try:
            updated_daemonset = self.api_client.replace_namespaced_daemon_set(
                name=name, namespace=namespace, body=body
            )
        except exceptions.ApiException as e:
            self._logger.error(
                f"Failed to update daemonset {name} in namespace {namespace}: {e}"
            )

        return updated_daemonset

    def create_from_yaml(
        self, namespace: str, yaml_file_path: str
    ) -> Optional[List[V1DaemonSet]]:
        created_daemonset = None
        try:
            created_daemonset = create_from_yaml(
                self.api_client, yaml_file_path, namespace=namespace
            )
        except exceptions.ApiException as e:
            self._logger.error(
                f"Failed to create daemonset from yaml in namespace {namespace}: {e}"
            )

        return created_daemonset

    def is_ready(self, namespace: str, name: str) -> bool:
        daemonset = self.get(namespace, name)
        if daemonset is None:
            return False

        return (
            daemonset.status.number_ready == daemonset.status.desired_number_scheduled
        )
