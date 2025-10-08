import sys
from core.management import execute_from_command_line


def main():
    """Main function to run the web scraper."""
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
