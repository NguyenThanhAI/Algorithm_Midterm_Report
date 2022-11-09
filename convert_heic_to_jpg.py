import os
from tqdm import tqdm
from PIL import Image, ExifTags
from pillow_heif import register_heif_opener
from datetime import datetime
import piexif
import re
register_heif_opener()



def convert(images_dir: str, save_dir: str):

    if not os.path.exists(save_dir):
        os.makedirs(save_dir, exist_ok=True)
    
    images_list = []
    for dirs, _, files in os.walk(images_dir):
        for file in files:
            if file.endswith(("heic", "HEIC")):
                images_list.append(os.path.join(dirs, file))

    #print(images_list)

    for image_path in tqdm(images_list):
        image = Image.open(image_path)

        image_exif = image.getexif()
        if image_exif:
            # Make a map with tag names and grab the datetime
            exif = { ExifTags.TAGS[k]: v for k, v in image_exif.items() if k in ExifTags.TAGS and type(v) is not bytes }
            date = datetime.strptime(exif['DateTime'], '%Y:%m:%d %H:%M:%S') 
            # Load exif data via piexif
            exif_dict = piexif.load(image.info["exif"])     
            # Update exif data with orientation and datetime
            exif_dict["0th"][piexif.ImageIFD.DateTime] = date.strftime("%Y:%m:%d %H:%M:%S")
            exif_dict["0th"][piexif.ImageIFD.Orientation] = 1
            exif_bytes = piexif.dump(exif_dict)     
            # Save image as jpeg
            image.save(os.path.join(save_dir, os.path.basename(image_path)), "jpeg", exif= exif_bytes)
        else:
            print(f"Unable to get exif data for {image_path}")


if __name__ == "__main__":

    images_dir = r"F:\job_images"
    save_dir = r"F:\heic_to_jpeg"
    convert(images_dir=images_dir, save_dir=save_dir)
