# Pyright builtins augmentation.
#
# src/translate.py installs the gettext-style translation function "_"
# into builtins at startup, so modules use it without importing it.
# This stub tells Pyright about it.

def _(message: str) -> str: ...
