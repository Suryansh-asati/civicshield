from __future__ import annotations

import importlib
import os
from typing import Any


USING_OPENCLAW: bool = False
OPENCLAW_AVAILABLE: bool = False
OPENCLAW_CLIENT_AVAILABLE: bool = False

OpenClaw = None  # type: ignore[assignment]
AsyncOpenClaw = None  # type: ignore[assignment]


def _ensure_cmdop_timeout_error() -> None:
    """Ensure `cmdop.exceptions.TimeoutError` exists for older openclaw imports.

    Some `openclaw` releases import `TimeoutError` from `cmdop.exceptions`, but
    newer `cmdop` versions renamed it to `ConnectionTimeoutError`.

    This function adds a backwards-compatible alias before importing `openclaw`.
    """

    try:
        import cmdop.exceptions as exc
    except Exception:
        return

    if hasattr(exc, "TimeoutError"):
        return

    if hasattr(exc, "ConnectionTimeoutError"):
        exc.TimeoutError = exc.ConnectionTimeoutError  # type: ignore[attr-defined]
        return

    # Last resort: define a basic timeout error type.
    base = getattr(exc, "CMDOPError", Exception)

    class TimeoutError(base):
        pass

    exc.TimeoutError = TimeoutError  # type: ignore[attr-defined]


def _import_openclaw_agent() -> Any:
    _ensure_cmdop_timeout_error()
    module = importlib.import_module("openclaw")
    global OPENCLAW_AVAILABLE
    OPENCLAW_AVAILABLE = True
    if hasattr(module, "Agent"):
        return getattr(module, "Agent")
    raise ImportError(
        "Installed 'openclaw' package does not export 'Agent' (exports: "
        + ", ".join(sorted({name for name in (getattr(module, "__all__", []) or [])}))
        + ")"
    )


try:
    Agent = _import_openclaw_agent()
    USING_OPENCLAW = True
except Exception:
    from openclaw_shim import Agent  # type: ignore
    USING_OPENCLAW = False


def _load_openclaw_clients() -> None:
    """Best-effort load of OpenClaw client classes (for orchestration).

    The installed `openclaw` package in this environment exports `OpenClaw` and
    `AsyncOpenClaw` (not `Agent`). We still expose these for optional use.
    """

    global OPENCLAW_CLIENT_AVAILABLE, OpenClaw, AsyncOpenClaw
    try:
        _ensure_cmdop_timeout_error()
        module = importlib.import_module("openclaw")
        OpenClaw = getattr(module, "OpenClaw", None)
        AsyncOpenClaw = getattr(module, "AsyncOpenClaw", None)
        OPENCLAW_CLIENT_AVAILABLE = OpenClaw is not None
    except Exception:
        OPENCLAW_CLIENT_AVAILABLE = False


_load_openclaw_clients()


def create_openclaw_client(mode: str | None = None):
    """Create an OpenClaw client for orchestration.

    Modes:
    - local: connects to a locally running CMDOP agent (Desktop/serve)
    - remote: connects via cloud relay using CMDOP_API_KEY

    Environment:
    - OPENCLAW_MODE: local|remote (default: local)
    - CMDOP_API_KEY: required for remote mode
    - CMDOP_SERVER: optional, default grpc.cmdop.com:443
    - CMDOP_AGENT_ID: optional
    """

    if not OPENCLAW_CLIENT_AVAILABLE or OpenClaw is None:
        return None

    selected = (mode or os.getenv("OPENCLAW_MODE") or "local").strip().lower()
    if selected == "remote":
        api_key = (os.getenv("CMDOP_API_KEY") or "").strip()
        if not api_key:
            raise RuntimeError("OPENCLAW_MODE=remote requires CMDOP_API_KEY")
        server = (os.getenv("CMDOP_SERVER") or "grpc.cmdop.com:443").strip()
        agent_id = (os.getenv("CMDOP_AGENT_ID") or None)
        return OpenClaw.remote(api_key=api_key, server=server, agent_id=agent_id)

    if selected != "local":
        raise ValueError("OPENCLAW_MODE must be 'local' or 'remote'")

    return OpenClaw.local()
