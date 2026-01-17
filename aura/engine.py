"""
Compatibility layer so any old code that uses:
    from aura import engine
    engine.execute("command", min_confidence=0.2)
continues to work.
"""

from aura.command_engine import get_engine as _get_engine


def get_engine():
    return _get_engine()


def execute(text: str, *args, **kwargs) -> str:
    """
    Legacy API. Extra args/kwargs (like min_confidence) are ignored.
    """
    engine = _get_engine()
    result = engine.execute_command(text)
    return result.get("message", "Done.")


def handle_command(text: str) -> str:
    """Preferred helper used by wake_word_listener."""
    return execute(text)
