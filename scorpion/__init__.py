from PIL import Image
from PIL.ExifTags import TAGS


class Scorpion:
    def __init__(self, args):
        self.args = args

    def __get_exif(self, file):
        image = Image.open(file)
        exif_data = image.getexif()

        if not exif_data:
            print(f"No EXIF data found in {file}")
            return {}

        exif = {}
        for tag_id, value in exif_data.items():
            tag = TAGS.get(tag_id, tag_id)
            exif[tag] = value

        return exif

    def run(self):
        files = self.args.FILES
        for file in files:
            exif = self.__get_exif(file)
            for tag, value in exif.items():
                print(f"{tag}: {value}")
