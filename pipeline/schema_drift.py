from __future__ import annotations

from dataclasses import dataclass, field


class SchemaDriftError(RuntimeError):
    """Upstream columns were renamed or removed."""


@dataclass
class SchemaReport:
    file_key: str
    path: str
    present: list[str]
    missing: list[str]
    extra: list[str]
    schema_hash: str

    @property
    def ok(self) -> bool:
        return not self.missing


@dataclass
class ValidationResult:
    reports: list[SchemaReport] = field(default_factory=list)
    skipped_missing_files: list[str] = field(default_factory=list)

    def fail_if_drift(self) -> None:
        bad = [r for r in self.reports if not r.ok]
        if not bad:
            return
        lines = ["Schema drift detected (required columns missing):"]
        for r in bad:
            lines.append(f"  {r.path}")
            lines.append(f"    missing: {r.missing}")
            lines.append(f"    present: {r.present}")
        raise SchemaDriftError("\n".join(lines))
