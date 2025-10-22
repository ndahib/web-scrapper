import sys
from core.management import ManagementUtility


class Scropion:
    """Scorpion class Receive images and parse them to extract metadata"""

    def __init__(self, links):
        pass


def main():
    manager = ManagementUtility(sys.argv[1:])
    manager.excute()


if __name__ == "__main__":
    main()
