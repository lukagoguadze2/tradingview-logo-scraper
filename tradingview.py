from bs4 import BeautifulSoup
import csv
import requests
import os
import cairosvg

url = "https://www.tradingview.com/symbols/"

with open('input.csv', 'r') as file:
    reader = csv.DictReader(file)

    for row in reader:
        try:
            folder_path = row["Foldername"]
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

            response = requests.get(url + str(row["Input"]))

            svg_url = BeautifulSoup(response.text, "html.parser").find("div", class_="container-xoKMfU7r logo-pAUXADuj").find_all("img", limit=2)[-1]['src']

            image_name = row["Input"] + ".svg"

            response = requests.get(svg_url)
            if response.status_code == 200:
                image_path = os.path.join(folder_path, image_name)
                with open(image_path, 'wb') as image_file:
                    scale_factor = 5.0
                    cairosvg.svg2png(url=response.url, write_to=image_file, scale=scale_factor)

                print(f"Image saved to: {image_path}")

        except:
            print("Image not found")

