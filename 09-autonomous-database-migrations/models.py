"""
Application Data Models
Target schema state used for autonomous drift detection.
Part 9 of Autonomous Developer Workflows Series (@SystemZeroTech)
"""

from dataclasses import dataclass, field
from typing import Optional, List

@dataclass
class ColumnDef:
    name: str
    type: str  # TEXT, INTEGER, BOOLEAN, TIMESTAMP
    nullable: bool = True
    default: Optional[str] = None
    is_primary_key: bool = False
    is_indexed: bool = False

@dataclass
class TableDef:
    name: str
    columns: List[ColumnDef] = field(default_factory=list)

# TARGET SCHEMA: The desired state defined in application codebase
TARGET_SCHEMA = {
    "users": TableDef(
        name="users",
        columns=[
            ColumnDef(name="id", type="INTEGER", nullable=False, is_primary_key=True),
            ColumnDef(name="email", type="TEXT", nullable=False, is_indexed=True),
            ColumnDef(name="full_name", type="TEXT", nullable=True),
            ColumnDef(name="mfa_enabled", type="BOOLEAN", nullable=False, default="0"),  # Newly added field!
            ColumnDef(name="stripe_customer_id", type="TEXT", nullable=True, is_indexed=True),  # Newly added field!
            ColumnDef(name="created_at", type="TEXT", nullable=False, default="CURRENT_TIMESTAMP")
        ]
    ),
    "organizations": TableDef(
        name="organizations",
        columns=[
            ColumnDef(name="id", type="INTEGER", nullable=False, is_primary_key=True),
            ColumnDef(name="slug", type="TEXT", nullable=False, is_indexed=True),
            ColumnDef(name="billing_tier", type="TEXT", nullable=False, default="'free'")
        ]
    )
}
