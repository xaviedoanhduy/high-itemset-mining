# high-itemset-mining

High Utility Itemset Mining (HUI) using a Genetic Algorithm (GA).

This package implements a GA-based approach to discover itemsets whose total utility (e.g. profit) across all transactions meets a minimum threshold. It combines TWU-based item pruning for efficiency with adaptive ranked mutation and multiple selection/crossover strategies for search quality.

## Installation

With [`uv`](https://docs.astral.sh/uv/) (recommended):

```bash
uv tool install high-itemset-mining
```

With `pip`:

```bash
pip install high-itemset-mining
```

## Usage

```bash
high-itemset-mining <dataset> [OPTIONS]
```

### Arguments

| Argument  | Description                        |
|-----------|------------------------------------|
| `dataset` | Path to the input dataset file     |

### Options

| Option                         | Default | Description                        |
|--------------------------------|---------|------------------------------------|
| `-u`, `--min-utility`          | `10`    | Minimum utility threshold          |
| `-p`, `--population-size`      | `50`    | GA population size                 |
| `-g`, `--generations`          | `10`    | Number of generations              |
| `-c`, `--crossover-prob`       | `0.8`   | Crossover probability (0–1)        |
| `-m`, `--mutation-prob`        | `0.2`   | Mutation probability (0–1)         |

### Example

```bash
high-itemset-mining datasets/db_utility.txt --min-utility 20 --generations 50
```

Results are saved to `output/<dataset_name>.txt`.

## Dataset Format

Each line represents a transaction with three colon-separated sections:

```
<items> : <transaction_utility> : <item_utilities>
```

Example:

```
2 3 4:9:2 2 5
1 2 3 4 5:18:4 2 3 5 4
1 3 4:11:4 2 5
```

- **Items**: space-separated positive integers, sorted in ascending order
- **Transaction utility**: sum of all item utilities in the transaction
- **Item utilities**: utility of each item in the same order as the items

## Output Format

Each line in the output file represents one high-utility itemset:

```
<items> #UTIL: <utility>
```

Example:

```
4 5 #UTIL: 40
1 2 4 #UTIL: 41
```

## Development

```bash
make install   # Install dependencies + pre-commit hooks
make check     # Run linter and formatter (ruff)
make test      # Run test suite (pytest)
```

## Authors

- Do Anh Duy — [@xaviedoanhduy](https://github.com/xaviedoanhduy)
- Pham Duc Thanh — phamducthanh@huflit.edu.vn

## License

AGPL-3.0
