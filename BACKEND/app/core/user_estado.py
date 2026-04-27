"""Estado de cuenta en BD legada (p. ej. Activo / Inactivo) y en el ORM nuevo (activo / inactivo)."""


def estado_indica_inactivo(estado: str | None) -> bool:
    e = (estado or "").strip().lower()
    return e in ("inactivo", "inactiva", "bloqueado", "suspendido")
