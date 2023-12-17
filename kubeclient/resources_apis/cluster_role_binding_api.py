from typing import List, Optional

from kubernetes.client import (
    RbacAuthorizationV1Api,
    V1ClusterRoleBinding,
    V1ClusterRoleBindingList,
    exceptions,
)
from kubernetes.utils import create_from_yaml

from .resource_api import ResourceApi


class ClusterRoleBinding(ResourceApi[RbacAuthorizationV1Api]):
    """
    A class to manage the Kubernetes ClusterRoleBinding resource.
    """

    api_client_type = RbacAuthorizationV1Api

    def get(self, name: str) -> Optional[V1ClusterRoleBinding]:
        clusterrolebinding = None
        try:
            clusterrolebinding = self.api_client.read_cluster_role_binding(name=name)
        except exceptions.ApiException as e:
            self._logger.error(f"Failed to get clusterrolebinding {name}: {e}")

        return clusterrolebinding

    def list(self) -> Optional[V1ClusterRoleBindingList]:
        clusterrolebindings = None
        try:
            clusterrolebindings = self.api_client.list_cluster_role_binding()
        except exceptions.ApiException as e:
            self._logger.error(f"Failed to list clusterrolebindings: {e}")

        return clusterrolebindings

    def create(self, body: V1ClusterRoleBinding) -> Optional[V1ClusterRoleBinding]:
        created_clusterrolebinding = None
        try:
            created_clusterrolebinding = self.api_client.create_cluster_role_binding(
                body=body
            )
        except exceptions.ApiException as e:
            self._logger.error(
                f"Failed to create clusterrolebinding {body.metadata.name}: {e}"
            )

        return created_clusterrolebinding

    def delete(self, name: str) -> Optional[V1ClusterRoleBinding]:
        deleted_clusterrolebinding = None
        try:
            deleted_clusterrolebinding = self.api_client.delete_cluster_role_binding(
                name=name
            )
        except exceptions.ApiException as e:
            self._logger.error(f"Failed to delete clusterrolebinding {name}: {e}")

        return deleted_clusterrolebinding

    def patch(
        self, name: str, body: V1ClusterRoleBinding
    ) -> Optional[V1ClusterRoleBinding]:
        patched_clusterrolebinding = None
        try:
            patched_clusterrolebinding = self.api_client.patch_cluster_role_binding(
                name=name, body=body
            )
        except exceptions.ApiException as e:
            self._logger.error(f"Failed to patch clusterrolebinding {name}: {e}")

        return patched_clusterrolebinding

    def update(
        self, name: str, body: V1ClusterRoleBinding
    ) -> Optional[V1ClusterRoleBinding]:
        updated_clusterrolebinding = None
        try:
            updated_clusterrolebinding = self.api_client.replace_cluster_role_binding(
                name=name, body=body
            )
        except exceptions.ApiException as e:
            self._logger.error(f"Failed to update clusterrolebinding {name}: {e}")

        return updated_clusterrolebinding

    def create_from_yaml(self, yaml_file: str) -> Optional[List[V1ClusterRoleBinding]]:
        created_clusterrolebinding = None
        try:
            created_clusterrolebinding = create_from_yaml(self.api_client, yaml_file)
        except exceptions.ApiException as e:
            self._logger.error(f"Failed to create clusterrolebinding from yaml: {e}")

        return created_clusterrolebinding

    def is_ready(self, name: str) -> bool:
        clusterrolebinding = self.get(name=name)
        return clusterrolebinding is not None
