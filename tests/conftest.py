import pytest
from agent.installer import install, uninstall

TEST_KEY = r"Software\EndpointAgentTests\TestRun"


@pytest.fixture
def installed_agent(tmp_path):
    install_dir = tmp_path / "agent"
    install(install_dir, key_path=TEST_KEY)                          # setup: install
    yield {"install_dir": install_dir, "key_path": TEST_KEY}         # give the test what it needs
    uninstall(install_dir, key_path=TEST_KEY)                        # teardown: uninstall