"""DUB.SAR 1.0 — Error definitions.

As defined in Section 19 of the DUB.SAR 1.0 Specification:
A conforming implementation MUST distinguish at least:
- SyntaxError — malformed source;
- NameError — unknown name;
- UnitError — incompatible dimensions;
- DivisionByZero — zero divisor;
- RangeError — invalid repetition range;
- InputError — invalid numeric input;
- ReturnError — procedure does not return the declared result shape.
"""

from typing import Optional


class DubSarError(Exception):
    """Base exception for all DUB.SAR language errors."""

    def __init__(
        self,
        message: str,
        line: Optional[int] = None,
        col: Optional[int] = None,
        source_file: Optional[str] = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.line = line
        self.col = col
        self.source_file = source_file

    def __str__(self) -> str:
        loc = []
        if self.source_file:
            loc.append(self.source_file)
        if self.line is not None:
            loc.append(f"line {self.line}")
        if self.col is not None:
            loc.append(f"col {self.col}")
        loc_str = f" ({', '.join(loc)})" if loc else ""
        return f"{self.__class__.__name__}{loc_str}: {self.message}"


class DubSarSyntaxError(DubSarError):
    """Malformed source."""
    pass


class DubSarNameError(DubSarError):
    """Unknown or undefined name."""
    pass


class DubSarUnitError(DubSarError):
    """Incompatible dimensions or invalid unit conversion."""
    pass


class DubSarDivisionByZero(DubSarError):
    """Division or modulo by zero divisor."""
    pass


class DubSarRangeError(DubSarError):
    """Invalid repetition range (e.g. non-integer or negative bound)."""
    pass


class DubSarInputError(DubSarError):
    """Invalid numeric input from user/environment."""
    pass


class DubSarReturnError(DubSarError):
    """Procedure does not return the declared result shape."""
    pass


class DubSarTypeError(DubSarError):
    """Invalid operand or argument type."""
    pass


class DubSarDomainError(DubSarError):
    """Invalid finite mathematical domain."""
    pass


class DubSarRecipeError(DubSarError):
    """Recipe definition, invocation, or determination error."""
    pass


class DubSarDeterminationError(DubSarError):
    """Invalid determination record, field access, or retention error."""
    pass


# ==============================================================================
# Tablet Archive Errors (§44)
# ==============================================================================

class DubSarArchiveError(DubSarError):
    """Base error for all tablet archive operations."""
    pass


class DubSarTabletNotFoundError(DubSarArchiveError):
    """Requested tablet was not found in the archive."""
    pass


class DubSarTabletVersionNotFoundError(DubSarArchiveError):
    """Requested version of tablet was not found in the archive."""
    pass


class DubSarTabletExistsError(DubSarArchiveError):
    """Tablet already exists in the archive."""
    pass


class DubSarArchiveConflictError(DubSarArchiveError):
    """Concurrent modification or version revision conflict."""
    pass


class DubSarArchiveCorruptError(DubSarArchiveError):
    """Archive database or tablet payload is corrupted."""
    pass


class DubSarInvalidTabletError(DubSarArchiveError):
    """Invalid tablet structure, shape, or format."""
    pass


class DubSarInvalidEntryError(DubSarArchiveError):
    """Invalid key or entry access in tablet."""
    pass


class DubSarConsultationError(DubSarArchiveError):
    """Error consulting persistent tablet."""
    pass


class DubSarInscriptionError(DubSarArchiveError):
    """Error inscribing working tablet into persistent archive."""
    pass


# Export standard names matching Section 19, Section 44, Section 59
SyntaxError = DubSarSyntaxError
NameError = DubSarNameError
UnitError = DubSarUnitError
TypeError = DubSarTypeError
DivisionByZero = DubSarDivisionByZero
RangeError = DubSarRangeError
DomainError = DubSarDomainError
InputError = DubSarInputError
ReturnError = DubSarReturnError
RecipeError = DubSarRecipeError
DeterminationError = DubSarDeterminationError

ArchiveError = DubSarArchiveError
TabletNotFoundError = DubSarTabletNotFoundError
TabletVersionNotFoundError = DubSarTabletVersionNotFoundError
TabletExistsError = DubSarTabletExistsError
ArchiveConflictError = DubSarArchiveConflictError
ArchiveCorruptError = DubSarArchiveCorruptError
InvalidTabletError = DubSarInvalidTabletError
InvalidEntryError = DubSarInvalidEntryError
ConsultationError = DubSarConsultationError
InscriptionError = DubSarInscriptionError

__all__ = [
    "DubSarError",
    "DubSarSyntaxError",
    "DubSarNameError",
    "DubSarUnitError",
    "DubSarTypeError",
    "DubSarDivisionByZero",
    "DubSarRangeError",
    "DubSarDomainError",
    "DubSarInputError",
    "DubSarReturnError",
    "DubSarRecipeError",
    "DubSarDeterminationError",
    "DubSarArchiveError",
    "DubSarTabletNotFoundError",
    "DubSarTabletVersionNotFoundError",
    "DubSarTabletExistsError",
    "DubSarArchiveConflictError",
    "DubSarArchiveCorruptError",
    "DubSarInvalidTabletError",
    "DubSarInvalidEntryError",
    "DubSarConsultationError",
    "DubSarInscriptionError",
    "SyntaxError",
    "NameError",
    "UnitError",
    "TypeError",
    "DivisionByZero",
    "RangeError",
    "DomainError",
    "InputError",
    "ReturnError",
    "RecipeError",
    "DeterminationError",
    "ArchiveError",
    "TabletNotFoundError",
    "TabletVersionNotFoundError",
    "TabletExistsError",
    "ArchiveConflictError",
    "ArchiveCorruptError",
    "InvalidTabletError",
    "InvalidEntryError",
    "ConsultationError",
    "InscriptionError",
]
