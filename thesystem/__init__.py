# Ensure PyInstaller-friendly behavior for subprocess invocations
try:
	from . import patches as _subprocess_patches  # noqa: F401
except Exception:
	# Non-fatal if it fails; fall back to default behavior
	pass


