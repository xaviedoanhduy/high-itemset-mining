from __future__ import annotations

from dataclasses import dataclass, field

from bitarray import bitarray


@dataclass
class Individual:
    bits: bitarray
    fitness: int = 0


@dataclass
class Transaction:
    tran_bits: bitarray
    value_items: dict[int, int] = field(default_factory=dict)
