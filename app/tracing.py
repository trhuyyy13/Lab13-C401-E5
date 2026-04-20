from __future__ import annotations

import functools
import inspect
import os
from pathlib import Path
from typing import Any

try:
    from langfuse import get_client as _langfuse_get_client
except Exception:  # pragma: no cover
    _langfuse_get_client = None


def _load_langfuse_env_from_dotenv() -> None:
    if os.getenv("LANGFUSE_PUBLIC_KEY") and os.getenv("LANGFUSE_SECRET_KEY"):
        return

    env_path = Path.cwd() / ".env"
    if not env_path.exists():
        return

    for line in env_path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        key = key.strip()
        if key in {"LANGFUSE_PUBLIC_KEY", "LANGFUSE_SECRET_KEY", "LANGFUSE_HOST"} and not os.getenv(key):
            os.environ[key] = value.strip()


def _get_client():
    if _langfuse_get_client is None:
        return None
    _load_langfuse_env_from_dotenv()
    return _langfuse_get_client()


def observe(func=None, **kwargs: Any):
    def _decorate(target):
        span_name = kwargs.get("name") or target.__name__

        if inspect.iscoroutinefunction(target):
            @functools.wraps(target)
            async def _async_wrapped(*args: Any, **inner_kwargs: Any):
                client = _get_client()
                if client is None:
                    return await target(*args, **inner_kwargs)
                with client.start_as_current_span(name=span_name):
                    return await target(*args, **inner_kwargs)

            return _async_wrapped

        @functools.wraps(target)
        def _wrapped(*args: Any, **inner_kwargs: Any):
            client = _get_client()
            if client is None:
                return target(*args, **inner_kwargs)
            with client.start_as_current_span(name=span_name):
                return target(*args, **inner_kwargs)

        return _wrapped

    if callable(func):
        return _decorate(func)
    return _decorate


class _LangfuseContextAdapter:
    def update_current_trace(self, **kwargs: Any) -> None:
        client = _get_client()
        if client is None:
            return None
        client.update_current_trace(**kwargs)

    def update_current_observation(self, **kwargs: Any) -> None:
        client = _get_client()
        if client is None:
            return None

        metadata = kwargs.get("metadata")
        usage_details = kwargs.get("usage_details")

        merged_metadata: dict[str, Any] = {}
        if isinstance(metadata, dict):
            merged_metadata.update(metadata)
        if isinstance(usage_details, dict):
            merged_metadata["usage_details"] = usage_details

        client.update_current_span(metadata=merged_metadata or None)


langfuse_context = _LangfuseContextAdapter()


def tracing_enabled() -> bool:
    return bool(os.getenv("LANGFUSE_PUBLIC_KEY") and os.getenv("LANGFUSE_SECRET_KEY"))

