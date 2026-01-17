"""
Package entry point used by aura_panel and other modules.
get_engine() returns a wrapper object that HAS .execute(...)
with a backward‑compatible signature.
"""

from aura.engine import get_engine as _get_engine


class AURAEngineWrapper:
    def __init__(self):
        self._engine = _get_engine()

    def execute(self, text: str, *args, **kwargs):
        result = self._engine.execute_command(text)
        return result.get("message", "Done.")

    def execute_command(self, text: str):
        return self._engine.execute_command(text)

    def get_history(self, limit: int = 20):
        return self._engine.get_history(limit)


def get_engine():
    return AURAEngineWrapper()
