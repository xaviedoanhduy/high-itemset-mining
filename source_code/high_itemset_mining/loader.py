from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from bitarray import bitarray

from .models import Transaction


def _is_comment(line: str) -> bool:
    return line.startswith(("#", "%", "@"))


def calculate_twu(path: Path, min_utility: int) -> set[int]:
    """First pass: return items whose Transaction-Weighted Utility >= min_utility."""
    item_to_twu: dict[int, int] = {}

    with path.open() as f:
        for raw in f:
            line = raw.strip()
            if not line or _is_comment(line):
                continue
            parts = line.split(":")
            items = [int(x) for x in parts[0].split()]
            tu = int(parts[1])
            for item in items:
                item_to_twu[item] = item_to_twu.get(item, 0) + tu

    return {item for item, twu in item_to_twu.items() if twu >= min_utility}


def load_transactions(path: Path) -> tuple[list[Transaction], int]:
    """Second pass: load all transactions. Returns (transactions, biggest_item)."""
    items_list: list[list[int]] = []
    utilities_list: list[list[int]] = []
    biggest_item = 0

    with path.open() as f:
        for raw in f:
            line = raw.strip()
            if not line or _is_comment(line):
                continue
            parts = line.split(":")
            items = [int(x) for x in parts[0].split()]
            utilities = [int(x) for x in parts[2].split()]
            items_list.append(items)
            utilities_list.append(utilities)
            biggest_item = max(biggest_item, max(items))

    def make_transaction(items: list[int], utilities: list[int]) -> Transaction:
        bits = bitarray(biggest_item)
        bits.setall(0)
        for item in items:
            bits[item - 1] = 1
        return Transaction(tran_bits=bits, value_items=dict(zip(items, utilities, strict=True)))

    with ThreadPoolExecutor() as executor:
        transactions = list(executor.map(make_transaction, items_list, utilities_list))

    return transactions, biggest_item
