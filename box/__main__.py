import os
import click
import logging
import shutil
from pathlib import Path
from rich.progress import MofNCompleteColumn, Progress, TimeRemainingColumn

LOGGER: logging.Logger = logging.getLogger(name=__name__)
logging.basicConfig(level=logging.INFO)

def evict(path: Path):
    LOGGER.info(f"Evicting {path}")


def materialize(path: Path):
    LOGGER.info(f"Materializing {path}")
    file_items: List[Path] = [path] if path.is_file() else list(path.rglob("**/*"))
    total_items: n = len(file_items)

    with Progress(*Progress.get_default_columns(), MofNCompleteColumn(), TimeRemainingColumn()) as prog:
        task = prog.add_task(description="Materializing Data", total=total_items)
        for file_item in file_items:
            if file_item.is_file():
                result = os.system(f"fileproviderctl materialize \"{str(file_item)}\"")
                if result != 0:
                    return

            prog.update(task, advance=1)
            prog.refresh()

@click.command()
@click.argument("command")
@click.argument("path_str")
def main(command: str, path_str: str):
    path: Path = Path(path_str)
    assert path.exists(), "Path must exist"

    commands: Dict = {
        "evict": evict,
        "materialize": materialize
    }
    command_fn: Callable = commands[command]
    command_fn(path)

if __name__ == "__main__":
    main()
