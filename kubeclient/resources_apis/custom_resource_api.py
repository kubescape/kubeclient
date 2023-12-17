from typing import List, Optional

from kubernetes.client import (
    CustomObjectsApi,
    V1CustomResourceDefinition,
    V1CustomResourceDefinitionList,
    exceptions,
)
from kubernetes.utils import create_from_yaml

from kubeclient.client import KubernetesApiClient

from .resource_api import ResourceApi


class CustomResource(ResourceApi[CustomObjectsApi]):
    """
    A class to manage the Kubernetes CustomResource resource.
    """

    api_client_type = CustomObjectsApi
    _group: str
    _version: str
    _plural: str

    def __init__(
        self, kubeclient: KubernetesApiClient, group: str, version: str, plural: str
    ):
        super().__init__(kubeclient)
        self._group = group
        self._version = version
        self._plural = plural

    def get(self, namespace: str, name: str) -> Optional[V1CustomResourceDefinition]:
        customresource = None
        try:
            customresource = self.api_client.get_namespaced_custom_object(
                group=self._group,
                version=self._version,
                plural=self._plural,
                name=name,
                namespace=namespace,
            )
        except exceptions.ApiException as e:
            self._logger.error(
                f"Failed to get customresource {name} in namespace {namespace}: {e}"
            )

        return customresource

    def list(self, namespace: str) -> Optional[V1CustomResourceDefinitionList]:
        customresources = None
        try:
            customresources = self.api_client.list_namespaced_custom_object(
                namespace=namespace,
                group=self._group,
                version=self._version,
                plural=self._plural,
            )
        except exceptions.ApiException as e:
            self._logger.error(
                f"Failed to list customresources in namespace {namespace}: {e}"
            )

        return customresources

    def create(
        self, namespace: str, body: V1CustomResourceDefinition
    ) -> Optional[V1CustomResourceDefinition]:
        created_customresource = None
        try:
            created_customresource = self.api_client.create_namespaced_custom_object(
                namespace=namespace,
                group=self._group,
                version=self._version,
                plural=self._plural,
                body=body,
            )
        except exceptions.ApiException as e:
            self._logger.error(
                f"Failed to create customresource {body.metadata.name} in namespace {namespace}: {e}"
            )

        return created_customresource

    def delete(self, namespace: str, name: str) -> Optional[V1CustomResourceDefinition]:
        deleted_customresource = None
        try:
            deleted_customresource = self.api_client.delete_namespaced_custom_object(
                namespace=namespace,
                group=self._group,
                version=self._version,
                plural=self._plural,
                name=name,
            )
        except exceptions.ApiException as e:
            self._logger.error(
                f"Failed to delete customresource {name} in namespace {namespace}: {e}"
            )

        return deleted_customresource

    def patch(
        self, namespace: str, name: str, body: V1CustomResourceDefinition
    ) -> Optional[V1CustomResourceDefinition]:
        patched_customresource = None
        try:
            patched_customresource = self.api_client.patch_namespaced_custom_object(
                namespace=namespace,
                group=self._group,
                version=self._version,
                plural=self._plural,
                name=name,
                body=body,
            )
        except exceptions.ApiException as e:
            self._logger.error(
                f"Failed to patch customresource {name} in namespace {namespace}: {e}"
            )

        return patched_customresource

    def update(
        self, namespace: str, name: str, body: V1CustomResourceDefinition
    ) -> Optional[V1CustomResourceDefinition]:
        updated_customresource = None
        try:
            updated_customresource = self.api_client.replace_namespaced_custom_object(
                namespace=namespace,
                group=self._group,
                version=self._version,
                plural=self._plural,
                name=name,
                body=body,
            )
        except exceptions.ApiException as e:
            self._logger.error(
                f"Failed to update customresource {name} in namespace {namespace}: {e}"
            )

        return updated_customresource

    def create_from_yaml(
        self, namespace: str, yaml_file_path: str
    ) -> Optional[List[V1CustomResourceDefinition]]:
        created_customresource = None
        try:
            created_customresource = create_from_yaml(
                self.api_client, yaml_file_path, namespace=namespace
            )
        except exceptions.ApiException as e:
            self._logger.error(
                f"Failed to create customresource from yaml in namespace {namespace}: {e}"
            )

        return created_customresource

    def is_ready(self, namespace: str, name: str) -> bool:
        customresource = self.get(namespace, name)
        if customresource is None:
            return False

        return True
