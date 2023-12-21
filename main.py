import json
import os
import requests

from PIL import Image
from haralyzer import HarParser, HarPage

PDF_NAME = "dergez.pdf"

def get_har_parser(file_name: str) -> HarParser:
    file_path = os.path.join("har_files", file_name)
    if not os.path.exists(file_path):
        raise FileNotFoundError
    with open(file_path, "r") as reader:
        return HarParser(json.loads(reader.read()))


def extract_images(har_parser: HarParser) -> list[str]:
    data = har_parser.har_data["entries"]
    image_urls = []
    for entry in data:
        if entry["response"]["content"]["mimeType"].find("image/") != 0:
            continue
        image_url = entry["request"]["url"]
        if "Katalog" in image_url or "katalog" in image_url:
            image_urls.append(image_url)
    return image_urls


def save_image_urls(image_urls: list[str]):
    with open('links.txt', 'w') as f:
        for link in image_urls:
            f.write("%s\n" % link)


def download_images(image_urls: list[str]):
    for index, image_url in enumerate(image_urls):
        formatted_number = f"{index:02d}"
        img_data = requests.get(image_url).content
        image_path = os.path.join("images", f'{formatted_number}-image.jpg')
        with open(image_path, 'wb') as handler:
            handler.write(img_data)


def get_images_from_folder(folder_name: str) -> list[Image]:
    images = []
    folder_elements = os.listdir(folder_name)
    folder_elements.sort()
    for folder_element in folder_elements:
        full_path = os.path.join(folder_name, folder_element)
        images.append(Image.open(full_path))
    return images


def compress_images(folder_name: str):
    folder_elements = os.listdir(folder_name)
    for folder_element in folder_elements:
        full_path = os.path.join(folder_name, folder_element)
        img = Image.open(full_path)
        width = int(img.size[0] * .65)
        height = int(img.size[1] * .65)
        img = img.resize((width, height))
        img.save(full_path, optimize=True, quality=90)


def create_pdf_from_images(images: list[Image], pdf_name: str):
    images[0].save(
        pdf_name, "PDF", resolution=100.0, save_all=True, append_images=images[1:]
    )


parser = get_har_parser("file.har")
extracted_urls = extract_images(parser)
save_image_urls(extracted_urls)
download_images(extracted_urls)
compress_images("images")
extracted_images = get_images_from_folder("images")
create_pdf_from_images(extracted_images, PDF_NAME)


