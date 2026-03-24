from __future__ import annotations

import multiprocessing
from concurrent.futures import ThreadPoolExecutor, as_completed

from bitarray import bitarray

from .models import Transaction


def _calc_single(transaction: Transaction, individual_bits: bitarray) -> int:
    if transaction.tran_bits & individual_bits != individual_bits:
        return 0
    return sum(transaction.value_items.get(pos + 1, 0) for pos in range(len(individual_bits)) if individual_bits[pos])


def _process_segment(segment: list[Transaction], individual_bits: bitarray) -> int:
    return sum(_calc_single(t, individual_bits) for t in segment)


def calculate_fitness(transactions: list[Transaction], individual_bits: bitarray) -> int:
    """Calculate total utility of an itemset across all transactions (parallel)."""
    num_workers = max(1, multiprocessing.cpu_count() // 2)
    n = len(transactions)
    segment_size = (n + num_workers - 1) // num_workers

    segments = [
        transactions[i * segment_size : (i + 1) * segment_size] for i in range(num_workers) if i * segment_size < n
    ]

    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        futures = [executor.submit(_process_segment, seg, individual_bits) for seg in segments]
        return sum(f.result() for f in as_completed(futures))
