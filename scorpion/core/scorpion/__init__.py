from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from constants import color, EXTENSIONS
from prettytable import PrettyTable
import os
from pathlib import Path


class Scorpion:
    def __init__(self, args):
        self.args = args
        self.table = PrettyTable()
        self.table.field_names = ["Tag", "Value"]
        self.count = 0

    def _get_general_info(self, image: Image.Image) -> None:
        width, height = image.size
        self.table.add_row(["Width", width])
        self.table.add_row(["Height", height])
        formt = image.format
        self.table.add_row(["Format", formt])
        Mode = image.mode
        self.table.add_row(["Mode", Mode])

    def _get_exif(self, file: Path) -> None:
        try:
            image = Image.open(file)
            self._get_general_info(image)
        except FileNotFoundError as e:
            print(f"File not found: {e}")
        exif_data = image.getexif()

        if not exif_data:
            self.table.add_row([f"{color.WARNING}No EXIF data found{color.RESET}", ""])

        for tag_id, value in exif_data.items():
            tag = TAGS.get(tag_id, tag_id)
            if tag == "GPSInfo":
                gps_info = {}
                for gps_tag_id, gps_value in value.items():
                    gps_tag = GPSTAGS.get(gps_tag_id, gps_tag_id)
                    gps_info[gps_tag] = gps_value
                self.table.add_row(["GPSInfo", gps_info])
            else:

                self.table.add_row([tag, value])

    def _get_file_info(self, file: Path) -> None:
        path_file = Path(file)
        self.table.add_row(["File", os.path.basename(file)])
        self.table.add_row(["Directory", os.path.dirname(path_file.resolve())])
        self.table.add_row(["File Size", os.path.getsize(file)])
        self.table.add_row(["Creation Date", os.path.getctime(file)])
        self.table.add_row(["Modification Date", os.path.getmtime(file)])
        self.table.add_row(["Access Date", os.path.getatime(file)])
        self.table.add_row(["File Permissions", os.stat(file).st_mode])

    def _check_file(self, file) -> bool:
        if file.startswith("http://") or file.startswith("https://"):
            print(f"{color.WARNING}Skipping URL: {file}{color.RESET}")
            return False
        file_extension = os.path.splitext(file)[-1].lower()
        if file_extension not in EXTENSIONS:
            print(f"Skipping unsupported image extension: {file_extension}")
            return False
        return True

    def _print_info(self):
        for file in self.args.FILES:
            if not self._check_file(file):
                continue
            self._check_file(file)
            self._get_file_info(file)
            self._get_exif(file)
            self.table.add_divider()
            self.count += 1

        if self.table.rows != []:
            print(self.table)
            print(f"{color.SUCCESS}Total files processed: {self.count}{color.RESET}")

    def _handle_delete(self):
        pass

    def _handle_modify(self):
        file = self.args.file
        arguments_tags = self.args.tag

        check = self._check_file(file)
        if not check:
            return
        try:
            image = Image.open(file)
        except FileNotFoundError as e:
            print(f"File not found: {e}")
        exif_data = image.getexif()
        for tag_id, value in exif_data.items():
            exif_tag = TAGS.get(tag_id, tag_id)
            for argument_tag in arguments_tags:
                if argument_tag == exif_tag:
                    exif_data[tag_id] = [argument_tag("=")[1]]
                    break

    def run(self):
        self._print_info()
        if self.args.delete:
            self._handle_delete()
        if self.args.modify:
            self._handle_modify()
