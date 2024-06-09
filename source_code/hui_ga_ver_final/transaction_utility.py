from bitarray import bitarray


class TransactionUtilities:
    def __init__(self, tran_bits, value_items, length=0):
        bits = bitarray(length)
        bits.setall(0)
        self.tran_bits = tran_bits if tran_bits else bits
        self.value_items = value_items if value_items else {}

