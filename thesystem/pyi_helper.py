import os
import sys
from pathlib import Path
from typing import Callable, Iterable, List


def is_frozen() -> bool:
	return getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS')


def base_path() -> str:
	# When frozen by PyInstaller onefile, data is extracted to sys._MEIPASS
	# For onedir, resources are next to the executable
	if is_frozen():
		return getattr(sys, '_MEIPASS', os.path.dirname(sys.executable))
	return os.path.dirname(os.path.abspath(__file__))


def resource_path(*relative_parts: Iterable[str]) -> str:
	return os.path.join(base_path(), *relative_parts)


def ensure_dir(path: str) -> None:
	parent_dir = os.path.dirname(path)
	if parent_dir and not os.path.exists(parent_dir):
		os.makedirs(parent_dir, exist_ok=True)


def relative_to_assets_from_module(module_file: str, assets_rel_dir: str) -> Callable[[str], Path]:
	# Returns a function that resolves assets relative to the module while supporting PyInstaller
	assets_rel_dir_norm = assets_rel_dir.replace('/', os.sep).replace('\\', os.sep)

	def _resolver(filename: str) -> Path:
		if is_frozen():
			return Path(resource_path(assets_rel_dir_norm, filename))
		module_dir = os.path.dirname(os.path.abspath(module_file))
		return Path(os.path.join(module_dir, assets_rel_dir_norm, filename))

	return _resolver


def run_py(script_rel_path: str, args: List[str] = None, detached: bool = True):
	"""Launch another script.

	- In dev: uses system 'python' on the .py file path relative to project root/module.
	- In frozen: uses embedded interpreter (sys.executable) and a .py file placed as data next to the exe.
	"""
	import subprocess

	args = args or []
	if is_frozen():
		script_abs = resource_path(script_rel_path)
		cmd = [sys.executable, script_abs, *args]
	else:
		# Best effort: resolve relative to current working directory
		cmd = ['python', script_rel_path, *args]
	creationflags = 0
	if detached and os.name == 'nt':
		# CREATE_NEW_CONSOLE
		creationflags = 0x00000010
	return subprocess.Popen(cmd, creationflags=creationflags)


