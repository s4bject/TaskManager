from src.storage import JSONPersistence
from src.manager import Manager
from src.cli import TaskManagerCLI

if __name__ == "__main__":
    persistence = JSONPersistence()
    library = Manager(persistence)
    cli = TaskManagerCLI(library)
    cli.run()
