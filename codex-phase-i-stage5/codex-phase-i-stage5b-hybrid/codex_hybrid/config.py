"""Configuration for the hybrid synthesis engine."""

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class EngineConfig:
    """Immutable runtime configuration."""

    # LLM endpoints (OpenAI-compatible chat completions).
    llm_base: str = "http://localhost:11434/v1"
    llm_model: str = "kimi-k2.7-code:cloud"
    llm_timeout: float = 120.0
    llm_api_key: str | None = None

    # Engine behaviour.
    deterministic_only: bool = True  # mirror of CLI: default OFF for LLM.
    dry_run: bool = False
    min_message_length: int = 10
    max_llm_body_chars: int = 4000
    min_llm_body_chars: int = 400  # floor for substantial synthesis body

    @classmethod
    def from_env(cls, use_llm: bool = False) -> "EngineConfig":
        """Build config from environment with explicit LLM override."""
        return cls(
            llm_base=os.getenv("SOLBIAN_LLM_BASE", "http://localhost:11434/v1"),
            llm_model=os.getenv("SOLBIAN_LLM_MODEL", "kimi-k2.7-code:cloud"),
            llm_timeout=float(os.getenv("SOLBIAN_LLM_TIMEOUT", "120")),
            llm_api_key=os.getenv("SOLBIAN_LLM_API_KEY") or None,
            deterministic_only=not use_llm,
            dry_run=os.getenv("SOLBIAN_DRY_RUN", "").lower() in ("1", "true", "yes"),
            min_llm_body_chars=int(os.getenv("SOLBIAN_LLM_MIN_BODY", "400")),
        )

    @staticmethod
    def default_living_db() -> str:
        """Return default living DB path.

        CLI ``--db`` always wins when present.  When absent, the engine falls back
        to ``SOLBIAN_LIVING_DB`` and then to the Stage 4 living-store default.
        """
        return os.getenv(
            "SOLBIAN_LIVING_DB",
            "/Users/archcore/solbian/codex-phase-i-stage4/data/codex_phase_i.sqlite",
        )

    @staticmethod
    def historical_corpus_roots() -> tuple[Path, ...]:
        """Directory roots for the historical read-only corpus (exact tree match)."""
        return (
            Path("/Users/archcore/solbian/codex"),
            Path.home() / "solbian" / "codex",
        )
