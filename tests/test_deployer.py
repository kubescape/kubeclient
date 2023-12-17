from pathlib import Path

from kubeclient import Deployer, KubernetesApiClient, resources_apis

YAML = Path(__file__).parent / "deployments" / "pod-with-host-mount.yaml"


def test_deployer():
    client = KubernetesApiClient()
    deployer = Deployer(client)
    deployer.create_from_yaml(YAML)

    pod_api = resources_apis.Pod(client)
    if pod_api.wait_for_ready("default", "host-mount-pod", 10, 0.5):
        pod = pod_api.get("default", "host-mount-pod")
        assert pod.status.phase == "Running"

    assert deployer.delete_from_yaml(YAML)
    assert not pod_api.wait_for_ready("default", "host-mount-pod", 5, 0.5)
