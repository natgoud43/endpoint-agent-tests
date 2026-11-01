"""Simulated endpoint agent installer: the system under test.

install() writes registry settings and files the way a real agent installer would.
uninstall() is expected to remove all of them.
"""
import json
import os
import winreg

DEFAULT_KEY = r"Software\FakeEndpointAgent"
VERSION = "1.0.0"
VALID_MODES = ("protect", "audit")


def install(install_dir, key_path=DEFAULT_KEY, mode="protect"):
    if mode not in VALID_MODES:
        raise ValueError(f"Invalid mode: {mode}")

    # Files: config and log
    os.makedirs(install_dir, exist_ok=True)
    with open(os.path.join(install_dir, "config.json"), "w") as f:
        json.dump({"version": VERSION, "mode": mode}, f)
    with open(os.path.join(install_dir, "agent.log"), "w") as f:
        f.write("Agent installed\n")

    # Registry settings
    with winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path) as key:
        winreg.SetValueEx(key, "Version", 0, winreg.REG_SZ, VERSION)
        winreg.SetValueEx(key, "InstallDir", 0, winreg.REG_SZ, str(install_dir))
        winreg.SetValueEx(key, "Mode", 0, winreg.REG_SZ, mode)
        winreg.SetValueEx(key, "Enabled", 0, winreg.REG_DWORD, 1)


def uninstall(install_dir, key_path=DEFAULT_KEY):
    for name in ("config.json", "agent.log"):
        path = os.path.join(install_dir, name)
        if os.path.exists(path):
            os.remove(path)
    if os.path.isdir(install_dir) and not os.listdir(install_dir):
        os.rmdir(install_dir)

    try:
        winreg.DeleteKey(winreg.HKEY_CURRENT_USER, key_path)
    except FileNotFoundError:
        pass  # already gone