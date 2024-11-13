Graduation Essay 2024
# Mining High Utility Itemsets Using Genetic Algorithms

Improving speed and memory in the field of data mining such as mining highly useful itemsets using genetic algorithms helps improve the above problems that classical algorithms easily encounter.





## Authors

- Do Anh Duy - [@xaviedoanhduy](https://www.github.com/xaviedoanhduy)
- Pham Duc Thanh - phamducthanh@huflit.edu.vn

## Tech Stack

Python, bitarray, multiprocessing


## Examples

### Input file format

*The input file format of high utility itemsets is defined as follows. It is a text file. Each lines represents a transaction. Each line is composed of three sections, as follows:
- First, the items contained in the transaction are listed. An item is represented by a positive integer. Each item is separated from the next item by a single space. It is assumed that all items within a same transaction (line) are sorted according to a total order (e.g. ascending order) and that no item can appear twice within the same transaction.
- Second, the symbol ":" appears and is followed by the transaction utility (an integer).
- Third, the symbol ":" appears and is followed by the utility of each item in this transaction (an integer), separated by single spaces.

for example, the input file is defined as follows:
```2 3 4:9:2 2 5
1 2 3 4 5:18:4 2 3 5 4
1 3 4:11:4 2 5
3 4 5:11:2 5 4
1 2 4 5:22:5 4 5 8
1 2 3 4:17:3 8 1 5
4 5:9:5 4
```

*Each line of the database is:
 - A set of items (the first column of the table)
 - The sum of the utilities (e.g. profit) of these items in this transaction (the second column of the table)
 - The utility of each item for this transaction (e.g. profit generated by this item for this transaction)(the third column of the table)

### Output file format

The output file format of high utility itemsets is defined as follows. It is a text file, each following line represents a high utility itemset. On each line, the items of the itemset are first listed. Each item is represented by an integer, followed by a single space. After, all the items, the keyword " #UTILITY: " appears and is followed by the utility of the itemset. For example, we show below the output file for this example
```
4 5 #UTIL: 40
1 2 4 #UTIL: 41
```
For example, the first line indicates that the itemset {4, 5} is a high utility itemset which has utility equals to 41. The following lines follows the same format.


## Documentation

[Final Report](https://github.com/xaviedoanhduy/high-itemset-mining/blob/main/my-documents/KLTN_20DH111943_DoAnhDuy.pdf)

[Powerpoint](https://github.com/xaviedoanhduy/high-itemset-mining/blob/main/my-documents/seminar-full.pptx)

[Reference Documents](https://github.com/xaviedoanhduy/high-itemset-mining/tree/main/documents-reference)



## Algorithms

[Example of solving quadratic equations](https://github.com/xaviedoanhduy/high-itemset-mining/blob/main/source_code/solve_quadratic_equations/genethic_algorithms_solve_quadratic_equations.py)

[FHM Algorithm](https://github.com/xaviedoanhduy/high-itemset-mining/tree/main/source_code/hui_ga_ver_final)

[HUI-Miner Algorithm](https://github.com/xaviedoanhduy/high-itemset-mining/tree/main/source_code/hui_miner_ver_1)

[Genetic Algorithm](https://github.com/xaviedoanhduy/high-itemset-mining/tree/main/source_code/hui_ga_ver_final)

[GUI](https://github.com/xaviedoanhduy/high-itemset-mining/tree/main/source_code/application)

[Multi-threaded parallel programming example](https://github.com/xaviedoanhduy/high-itemset-mining/blob/main/source_code/solve_quadratic_equations/parallel_1.py)

[Multiprocessing example](https://github.com/xaviedoanhduy/high-itemset-mining/blob/main/source_code/solve_quadratic_equations/parallel_3.py)


## Screenshots

![image](https://github.com/xaviedoanhduy/high-itemset-mining/assets/90429015/fd837bd1-5e6e-4593-bc40-4d86ecf7cd85)




## License

[HUFLIT](https://huflit.edu.vn/)
