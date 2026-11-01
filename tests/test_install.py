import json
import winreg


def test_install_creates_config_file(installed_agent):
    config_file = installed_agent["install_dir"] / "config.json"
    assert config_file.exists()

def test_install_creates_log_with_installed_message(installed_agent):
    agent_file = installed_agent["install_dir"] / "agent.log"
    assert agent_file.exists()
    content = agent_file.read_text()
    assert "Agent installed" in content

def test_config_file_contents_correct_version_and_mode(installed_agent):
    config_file = installed_agent["install_dir"] / "config.json"
    config = json.loads(config_file.read_text())
    assert config["version"] == "1.0.0"
    assert config["mode"] == "protect"

def test_intall_writes_version_as_string(installed_agent):
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, installed_agent["key_path"]) as key:
        value, value_type = winreg.QueryValueEx(key, "Version")
    assert value == "1.0.0"
    assert value_type == winreg.REG_SZ 

def test_install_writes_enabled_as_true(installed_agent):
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, installed_agent["key_path"]) as key:
        value, value_type = winreg.QueryValueEx(key, "Enabled")
    assert value == 1
    assert value_type == winreg.REG_DWORD 

def test_install_writes_install_dir_to_registry(installed_agent):
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, installed_agent["key_path"]) as key:
        value, _ = winreg.QueryValueEx(key, "InstallDir")
    assert value == str(installed_agent["install_dir"]) 
 