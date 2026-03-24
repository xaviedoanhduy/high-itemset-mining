from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer

from .ga import GeneticAlgorithm

app = typer.Typer(help="High Utility Itemset Mining using Genetic Algorithm.")


@app.command()
def run(
    dataset: Annotated[Path, typer.Argument(help="Path to the dataset file (.txt)")],
    min_utility: Annotated[int, typer.Option("--min-utility", "-u", help="Minimum utility threshold")] = 10,
    population_size: Annotated[int, typer.Option("--population-size", "-p", help="GA population size")] = 50,
    generations: Annotated[int, typer.Option("--generations", "-g", help="Number of GA generations")] = 10,
    crossover_prob: Annotated[float, typer.Option("--crossover-prob", "-c", help="Crossover probability (0-1)")] = 0.8,
    mutation_prob: Annotated[float, typer.Option("--mutation-prob", "-m", help="Mutation probability (0-1)")] = 0.2,
) -> None:
    if not dataset.exists():
        typer.echo(f"Error: dataset file '{dataset}' not found.", err=True)
        raise typer.Exit(code=1)

    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / f"{dataset.stem}.txt"

    ga = GeneticAlgorithm(
        dataset_path=dataset,
        min_utility=min_utility,
        population_size=population_size,
        generations=generations,
        crossover_prob=crossover_prob,
        mutation_prob=mutation_prob,
        output=output_path,
    )
    ga.execute()

    typer.echo(f"Results saved to: {output_path}")


if __name__ == "__main__":
    app()
