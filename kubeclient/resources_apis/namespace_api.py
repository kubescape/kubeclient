from typing import List, Optional

from kubernetes.client import CoreV1Api, V1Namespace, V1NamespaceList, exceptions
from kubernetes.utils import create_from_yaml

from .resource_api import ResourceApi


class Namespace(ResourceApi[CoreV1Api]):
    """
    A class to manage the Kubernetes Namespace resource.
    """

    api_client_type = CoreV1Api

    def get(self, name: str) -> Optional[V1Namespace]:
        namespace = None
        try:
            namespace = self.api_client.read_namespace(name=name)
        except exceptions.ApiException as e:
            self._logger.error(f"Failed to get namespace {name}: {e}")

        return namespace

    def list(self) -> Optional[V1NamespaceList]:
        namespaces = None
        try:
            namespaces = self.api_client.list_namespace()
        except exceptions.ApiException as e:
            self._logger.error(f"Failed to list namespaces: {e}")

        return namespaces

    def create(self, body: V1Namespace) -> Optional[V1Namespace]:
        created_namespace = None
        try:
            created_namespace = self.api_client.create_namespace(body=body)
        except exceptions.ApiException as e:
            self._logger.error(f"Failed to create namespace {body.metadata.name}: {e}")

        return created_namespace

    def delete(self, name: str) -> Optional[V1Namespace]:
        deleted_namespace = None
        try:
            deleted_namespace = self.api_client.delete_namespace(name=name)
        except exceptions.ApiException as e:
            self._logger.error(f"Failed to delete namespace {name}: {e}")

        return deleted_namespace

    def patch(self, name: str, body: V1Namespace) -> Optional[V1Namespace]:
        patched_namespace = None
        try:
            patched_namespace = self.api_client.patch_namespace(name=name, body=body)
        except exceptions.ApiException as e:
            self._logger.error(f"Failed to patch namespace {name}: {e}")

        return patched_namespace

    def update(self, name: str, body: V1Namespace) -> Optional[V1Namespace]:
        updated_namespace = None
        try:
            updated_namespace = self.api_client.replace_namespace(name=name, body=body)
        except exceptions.ApiException as e:
            self._logger.error(f"Failed to update namespace {name}: {e}")

        return updated_namespace

    def create_from_yaml(self, yaml_file_path: str) -> Optional[List[V1Namespace]]:
        created_namespace = None
        try:
            created_namespace = create_from_yaml(self.api_client, yaml_file_path)
        except exceptions.ApiException as e:
            self._logger.error(f"Failed to create namespace from yaml: {e}")

        return created_namespace

    def is_ready(self, namespace: str, name: str) -> bool:
        namespace = self.get(name)
        return namespace is not None and namespace.status.phase == "Active"
