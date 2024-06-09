from bitarray import bitarray

if __name__ == "__main__":
    transactions = [
        (1, 0, 1, 1, 0, 0, 0),
        (1, 0, 1, 0, 1, 0, 1),
        (1, 1, 1, 1, 1, 1, 0),
        (0, 1, 1, 1, 1, 0, 0),
        (0, 1, 1, 0, 1, 0, 1),
        (1, 0, 1, 1, 0, 0, 0),
        (1, 1, 1, 1, 0, 1, 0),
        (1, 1, 1, 0, 1, 1, 0),
    ]

    transactions_bit = []
    for transaction in transactions:
        tran_bits = bitarray(len(transaction))
        tran_bits.setall(0)
        for i, bit in enumerate(transaction):
            if bit == 1:
                tran_bits[i] = 1

        transactions_bit.append(tran_bits)

    c_1 = (1, 0, 0, 0, 0, 0, 0)
    c_2 = (1, 1, 0, 0, 0, 0, 0)
    c_3 = (1, 0, 0, 0, 0, 1, 0)
    c_4 = (0, 1, 0, 0, 0, 0, 0)
    c_5 = (1, 0, 1, 0, 0, 0, 0)
    c_6 = (1, 0, 1, 1, 0, 0, 0)
    c_7 = (0, 1, 1, 0, 0, 0, 0)
    c_8 = (0, 1, 0, 1, 0, 0, 0)
    candidates = [c_1, c_2, c_3, c_4, c_5, c_6, c_7, c_8]

    candidates_bits =[]
    for candidate in candidates:
        candidate_bits = bitarray(len(candidate))
        candidate_bits.setall(0)
        for i, bit in enumerate(candidate):
            if bit == 1:
                candidate_bits[i] = 1

        candidates_bits.append(candidate_bits)

    for i, transaction in enumerate(transactions_bit):
        mask = transaction & candidates_bits[7]
        list_mask = mask.tolist()
        str_mask = "\t".join(map(str, list_mask))
        isValid = mask == candidates_bits[7]

        # print(f"T{i + 1}: [{str_mask}] - {isValid}")
        if isValid:
            print(str_mask)
        # print(str_mask)
