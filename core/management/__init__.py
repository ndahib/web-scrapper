import sys
from argparse import ArgumentParser


class SubcommandChoices:
    """
    Class constants for subcommand choices
    """

    IMAGES = "images"
    LINKS = "links"
    EMAILS = "emails"
    PHONES = "phones"
    ADDRESS = "address"
    ALL = "all"

    @classmethod
    def get_choices(cls):
        """Return all subcommand choices in a list."""
        return [getattr(cls, name) for name in vars(cls) if not name.startswith("_") and not callable(getattr(cls, name))]


class ManagementUtility:
    """Encapuslate the logic of web scrapper and command line"""

    def __init__(self, argv=None):
        self.argv = argv or sys.argv[:]
        self.prog_name = self.argv[0]
        if self.prog_name == "__main__.py":
            self.prog_name = "python -m web_scraper"
        self.settings_exception = None

    def __prompt_for_subcommand(self):
        while True:
            user_choice = (
                input(f"Choose a subcommand to run ({', '.join(SubcommandChoices.get_choices())}), or type 'exit' to quit:\n> ").strip().lower()
            )

            if user_choice == "exit":
                sys.exit(0)
            elif user_choice in SubcommandChoices.get_choices():
                return user_choice
            else:
                print("❌ Invalid choice. Try again.\n")

    def __parse_args(self):
        parser = ArgumentParser(prog=self.prog_name)
        parser.description = "A web scraper tool to scrape images, links, emails, phone numbers, and addresses from a given URL."

        parser.add_argument(
            "subcommand",
            help="Subcommand to run",
            choices=["images", "links", "emails", "phones", "address", "all"],
            nargs="?",
        )

        parser.add_argument(
            "URL",
            type=str,
            help="the URL of the website to scrape",
        )
        parser.add_argument(
            "-r",
            "--recursive",
            help="scrape links recursively",
            nargs="?",
        )
        parser.add_argument(
            "-l",
            "--level",
            type=int,
            help="the level of recursion if not specified, the default is 5",
            default=5,
            nargs="?",
        )
        parser.add_argument(
            "-p",
            "--path",
            type=str,
            help="the path to save the output file",
            default="./data/",
            nargs="?",
        )
        args = parser.parse_args(self.argv[1:])
        return parser, args

    def execute(self):
        """Given the commande line arguments, figure out which subcommand is being run, create a parser to parse those arguments and then execute the subcommand."""

        # handle images only right now then add link , numbers of telephones, emails, address, etc
        parser, args = self.__parse_args()
        if not args.subcommand:
            subcommand = self.__prompt_for_subcommand()
            # Inject the subcommand into argv and re-parse
            new_argv = [self.argv[0], subcommand] + self.argv[1:]
            parser.set_defaults(subcommand=subcommand)
            args = parser.parse_args(new_argv[1:])

        if args.subcommand == SubcommandChoices.IMAGES:
            # handle_images(args)
            pass


def execute_from_command_line(argv=None):
    """A simple method that runs ManagementUtility."""
    utility = ManagementUtility(argv)
    utility.execute()
