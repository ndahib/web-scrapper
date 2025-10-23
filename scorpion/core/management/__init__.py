import sys
from argparse import ArgumentParser
from constants import color


class ManagementUtility:
    """Encapuslate the logic of scoropion and command line"""

    def __init__(self, argv=None):
        self.argv = argv or sys.argv[:]
        self.prog_name = self.argv[0]
        if self.prog_name == "__main__.py":
            self.prog_name = "python -m scorpion"
        self.settings_exception = None

    def __parse_args(self):
        parser = ArgumentParser(prog=self.prog_name)
        parser.description = "A scorpion to parse metadata of images."
        parser.add_argument(
            "FILES",
            type=str,
            help="the image or list of images to be parsed",
            nargs="+",
        )
        parser.add_argument(
            "-d",
            "--delete",
            action="store_true",
            help="delete metadata of all images",
        )
        parser.add_argument(
            "-m",
            "--modify",
            action="store_true",
            help="modify metadata of all images",
        )
        parser.add_argument(
            "-t",
            "--tag",
            type=str,
            help="the tag to be deleted or modified, if specified, -d and -m will work on this tag only",
            nargs="+",
        )
        parser.add_argument(
            "-f",
            "--file",
            type=str,
            help="the path of the image file to will be deleted or modified, if specified, -d and -m will work on this file only",
            nargs="?",
        )
        return parser, parser.parse_args()

    def excute(self):
        """Given the commande line arguments, figure out which subcommand is being run, create a parser to parse those arguments and then execute the subcommand."""
        parser, args = self.__parse_args()
        if len(self.argv) > 1 and self.argv[1] == "help":
            parser.print_help()
            sys.exit(0)

        if args.delete and args.modify and not args.tag and not args.file:
            parser.error(f"{color.WARNING}You must specify either -t (tag) or -f (file) when using -d and -m.{color.RESET}")
        try:
            from core.scorpion import Scorpion

            scorpion = Scorpion(args)
            scorpion.run()
        except ImportError:
            print("❌ Scorpion class not found. Please ensure core/scorpion.py exists and contains a Scorpion class.")
            sys.exit(1)
        except Exception as e:
            print(f"❌ {e}")
            sys.exit(1)
