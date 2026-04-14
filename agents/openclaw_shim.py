from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Iterable, Optional


ToolFn = Callable[..., Any]


@dataclass
class Agent:
    model: Optional[str] = None
    base_url: Optional[str] = None
    tools: Optional[Iterable[ToolFn]] = None
    system_prompt: str = ""

    def run(self, prompt: str) -> dict:
        """A minimal local Agent implementation.

        This is a fallback to keep the repository runnable if the external
        `openclaw` package isn't installed or is incompatible with the installed
        `cmdop` SDK.

        Expected tools (by function name) for the current repo:
        - fetch_data() -> iterable of strings
        - analyze_text(text: str) -> dict with at least a label
        - alert_authority(data: Any) -> None
        """

        tool_map: dict[str, ToolFn] = {}
        for tool in self.tools or []:
            name = getattr(tool, "__name__", None)
            if name:
                tool_map[name] = tool

        fetch_data = tool_map.get("fetch_data")
        analyze_text = tool_map.get("analyze_text")
        alert_authority = tool_map.get("alert_authority")

        if fetch_data is None or analyze_text is None:
            raise RuntimeError(
                "Missing required tools. Provide fetch_data and analyze_text (and optionally alert_authority)."
            )

        findings: list[dict[str, Any]] = []
        for item in fetch_data() or []:
            analysis = analyze_text(item)
            record = {"text": item, "analysis": analysis}
            findings.append(record)

            label = str(analysis.get("label", "")).lower()
            if alert_authority is not None and label in {"hate", "harmful", "offensive"}:
                alert_authority(record)

        result: dict[str, Any] = {
            "prompt": prompt,
            "count": len(findings),
            "findings": findings,
        }

        llm_summary = self._maybe_summarize_with_ollama(prompt, findings)
        if llm_summary:
            result["llm_summary"] = llm_summary

        return result

    def _maybe_summarize_with_ollama(
        self, prompt: str, findings: list[dict[str, Any]]
    ) -> str | None:
        if not self.base_url or not self.model:
            return None

        model_name = self.model
        if model_name.startswith("ollama/"):
            model_name = model_name.split("/", 1)[1]

        try:
            import httpx

            payload = {
                "model": model_name,
                "prompt": (
                    (self.system_prompt or "").strip()
                    + "\n\nUser task: "
                    + (prompt or "")
                    + "\n\nFindings: "
                    + str(findings)
                    + "\n\nWrite a short summary and recommended action." 
                ),
                "stream": False,
            }

            url = self.base_url.rstrip("/") + "/api/generate"
            with httpx.Client(timeout=10.0) as client:
                resp = client.post(url, json=payload)
                resp.raise_for_status()
                data = resp.json()
                text = data.get("response")
                if isinstance(text, str) and text.strip():
                    return text.strip()
        except Exception:
            return None

        return None
