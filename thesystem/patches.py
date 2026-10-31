import os
import sys
import subprocess
 as _subprocess
from typing import Sequence, Union
try:
	from .pyi_helper import resource_path, is_frozen
except Exception:
	# Fallbacks if helper isn't available
	def is_frozen() -> bool:
		return getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS')

	def resource_path(*parts):
		base = getattr(sys, '_MEIPASS', os.path.dirname(sys.executable)) if is_frozen() else os.getcwd()
		return os.path.join(base, *parts)


def _rewrite_python_command(cmd: Sequence[Union[str, bytes]]):
	try:
		if not cmd:
			return cmd
		first = cmd[0]
		# Normalize to str for checks
		if isinstance(first, bytes):
			first_str = first.decode(errors='ignore')
		else:
			first_str = str(first)
		if first_str.lower().endswith('python') or os.path.basename(first_str).lower() in {'python', 'python.exe'}:
			# If next arg is a .py script, rewrite to use current interpreter
			if len(cmd) >= 2:
				second = cmd[1]
				second_str = second.decode(errors='ignore') if isinstance(second, bytes) else str(second)
				if second_str.lower().endswith('.py'):
					cmd = list(cmd)
					cmd[0] = sys.executable
					# If frozen and path is relative, resolve against bundled resources
					if is_frozen() and not os.path.isabs(second_str):
						second_str = second_str.replace('/', os.sep).replace('\\\\', os.sep)
						cmd[1] = resource_path(second_str)
					return cmd
	except Exception:
		return cmd
	return cmd


_orig_popen = _subprocess.Popen


class _PatchedPopen(_subprocess.Popen):
	def __init__(self, args, *p, **kw):
		if isinstance(args, (list, tuple)):
			args = _rewrite_python_command(args)
		super().__init__(args, *p, **kw)


def apply():
	if _subprocess.Popen is not _orig_popen:
		return
	_subprocess.Popen = _PatchedPopen


# Apply immediately on import
apply()


