"""This specially named module makes the package runnable."""

from ViewController import ViewController
from models.Environement import Environment
import dotenv

from utils import get_urls

dotenv.load_dotenv('dev.env')

teams = ["red", "blue"]


def main() -> None:
    clients = get_urls(teams)

    if len(clients) != len(teams):
        raise ValueError(f"Just {len(clients)} clients are registered in {len(teams)} teams.")

    """Entrypoint of simulation."""
    model = Environment(clients=clients)
    vc = ViewController(model)
    vc.start_simulation()


if __name__ == "__main__":
    main()
