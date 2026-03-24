Graduation Essay 2024
# Mining High Utility Itemsets Using Genetic Algorithms

Improving speed and memory in the field of data mining — specifically mining high utility itemsets using genetic algorithms — to address the performance problems that classical algorithms commonly encounter.

## Authors

- Do Anh Duy — [@xaviedoanhduy](https://github.com/xaviedoanhduy)
- Pham Duc Thanh — phamducthanh@huflit.edu.vn

## Tech Stack

Python, bitarray, psutil, Typer, uv

## Dataset Format

Each line represents a transaction with three colon-separated sections:

```
<items> : <transaction_utility> : <item_utilities>
```

- **Items**: space-separated positive integers, sorted in ascending order, no duplicates
- **Transaction utility**: sum of all item utilities in this transaction
- **Item utilities**: utility of each item in the same order as the items

Example input file:

```
2 3 4:9:2 2 5
1 2 3 4 5:18:4 2 3 5 4
1 3 4:11:4 2 5
3 4 5:11:2 5 4
1 2 4 5:22:5 4 5 8
1 2 3 4:17:3 8 1 5
4 5:9:5 4
```

## Output Format

Each line represents one high-utility itemset:

```
<items> #UTIL: <utility>
```

Example:

```
4 5 #UTIL: 40
1 2 4 #UTIL: 41
```

## Algorithms

[Genetic Algorithm (GA-HUI)](https://github.com/xaviedoanhduy/high-itemset-mining/tree/main/source_code/high_itemset_mining)

[FHM Algorithm](https://github.com/xaviedoanhduy/high-itemset-mining/tree/main/source_code/hui_ga_ver_final)

[GUI Application](https://github.com/xaviedoanhduy/high-itemset-mining/tree/main/source_code/application)

## Documentation

[Final Report](https://github.com/xaviedoanhduy/high-itemset-mining/blob/main/my-documents/KLTN_20DH111943_DoAnhDuy.pdf)

[Powerpoint](https://github.com/xaviedoanhduy/high-itemset-mining/blob/main/my-documents/seminar-full.pptx)

[Reference Documents](https://github.com/xaviedoanhduy/high-itemset-mining/tree/main/documents-reference)

## Screenshots

![image](https://github.com/xaviedoanhduy/high-itemset-mining/assets/90429015/fd837bd1-5e6e-4593-bc40-4d86ecf7cd85)

## License

[HUFLIT](https://huflit.edu.vn/)
