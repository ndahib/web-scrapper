EXTENSIONS = [".jpg", ".jpeg", ".png", ".gif", ".bmp"]
USER_AGENT = "42SpiderBot/1.0"
DEFAULT_PATH = "./data/"


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
