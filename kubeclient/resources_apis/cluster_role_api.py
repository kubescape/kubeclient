from typing import List, Optional

from kubernetes.client import (
    RbacAuthorizationV1Api,
    V1ClusterRole,
    V1ClusterRoleList,
    exceptions,
)
from kubernetes.utils import create_from_yaml

from .resource_api import ResourceApi


class ClusterRole(ResourceApi[RbacAuthorizationV1Api]):
    """
    A class to manage the Kubernetes ClusterRole resource.
    """

    api_client_type = RbacAuthorizationV1Api

    def get(self, name: str) -> Optional[V1ClusterRole]:
        clusterrole = None
        try:
            clusterrole = self.api_client.read_cluster_role(name=name)
        except exceptions.ApiException as e:
            self._logger.error(f"Failed to get clusterrole {name}: {e}")

        return clusterrole

    def list(self) -> Optional[V1ClusterRoleList]:
        clusterroles = None
        try:
            clusterroles = self.api_client.list_cluster_role()
        except exceptions.ApiException as e:
            self._logger.error(f"Failed to list clusterroles: {e}")

        return clusterroles

    def create(self, body: V1ClusterRole) -> Optional[V1ClusterRole]:
        created_clusterrole = None
        try:
            created_clusterrole = self.api_client.create_cluster_role(body=body)
        except exceptions.ApiException as e:
            self._logger.error(
                f"Failed to create clusterrole {body.metadata.name}: {e}"
            )

        return created_clusterrole

    def delete(self, name: str) -> Optional[V1ClusterRole]:
        deleted_clusterrole = None
        try:
            deleted_clusterrole = self.api_client.delete_cluster_role(name=name)
        except exceptions.ApiException as e:
            self._logger.error(f"Failed to delete clusterrole {name}: {e}")

        return deleted_clusterrole

    def patch(self, name: str, body: V1ClusterRole) -> Optional[V1ClusterRole]:
        patched_clusterrole = None
        try:
            patched_clusterrole = self.api_client.patch_cluster_role(
                name=name, body=body
            )
        except exceptions.ApiException as e:
            self._logger.error(f"Failed to patch clusterrole {name}: {e}")

        return patched_clusterrole

    def update(self, name: str, body: V1ClusterRole) -> Optional[V1ClusterRole]:
        updated_clusterrole = None
        try:
            updated_clusterrole = self.api_client.replace_cluster_role(
                name=name, body=body
            )
        except exceptions.ApiException as e:
            self._logger.error(f"Failed to update clusterrole {name}: {e}")

        return updated_clusterrole

    def create_from_yaml(self, yaml_file: str) -> Optional[List[V1ClusterRole]]:
        created_clusterrole = None
        try:
            created_clusterrole = create_from_yaml(self.api_client, yaml_file)
        except exceptions.ApiException as e:
            self._logger.error(f"Failed to create clusterrole from yaml: {e}")

        return created_clusterrole

    def is_ready(self, name: str) -> bool:
        clusterrole = self.get(name)
        return clusterrole is not None
