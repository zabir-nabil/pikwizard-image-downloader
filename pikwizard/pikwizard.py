"""
An image downloader for https://pikwizard.com using Selenium.
Download royalty free and safe for commercial use images, with no attribution required!
author: https://github.com/zabir-nabil
"""

import re
import os
import logging
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
from urllib.request import Request, urlopen
import numpy as np
import cv2
from selenium import webdriver
from selenium.webdriver.firefox.options import Options


class Pikwizard:
    def __init__(self, search = "cute cats", num_images = 5, path = "downloads", num_workers = 8, height = -1, width = -1, verbose = True, **kwargs):
        """
        """
        self.search = search
        self.num_images = num_images
        self.path = path
        self.num_workers = num_workers
        self.height = height
        self.width = width
        self.verbose = verbose

        browser_options = Options()
        browser_options.add_argument("--headless")
        browser_options.add_argument('--no-sandbox')
        self.driver = webdriver.Firefox(options=browser_options) # keep the webdriver in the same directory

        # logging.basicConfig(level = print)

    def url_to_image(self, url):
        """
        download image from url
        """
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        resp = urlopen(req).read()
        image = np.asarray(bytearray(resp), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)

        return image

    def download(self):
        image_urls = []
        for page in range(1, 100):
            self.driver.get(f"https://pikwizard.com/?q={self.search}&perpage=100&page={page}")
            # hardcoded
            pat = r'"url_large"\:[^,]+'
            urls = ['https://pikwizard.com' + url.replace('"url_large":', '').replace('"', '') for url in re.findall(pat, self.driver.page_source)]

            image_urls.extend(urls)
            if len(urls) == 0 or len(image_urls) >= 2 * self.num_images:
                break

        total_downloads = 0
        failed_downloads = []

        os.makedirs(self.path, exist_ok=True)

        for _ in tqdm(range(self.num_images)):
            url = image_urls[total_downloads]
            # TO-DO: multi-threading
            try:
                h = self.height
                w = self.width
                img = self.url_to_image(url)
                h_, w_ = img.shape[:2]
                h = h_ if h == -1 else h
                w = w_ if w == -1 else w
                cv2.imwrite(os.path.join(self.path, f"{self.search.replace(' ', '_')}_{total_downloads+1}.jpg"), img)
                total_downloads += 1
            except Exception as e:
                failed_downloads.append((url, e))

        if self.verbose:
            print("Summary:")
            print("----------------------------------------------------")
            print(f"Total downloaded images: {total_downloads}")
            print(f"Failed images: {len(failed_downloads)}")
            if len(failed_downloads) > 0:
                for f_d, e in failed_downloads:
                    print(f"{f_d} failed! {e}")

if __name__ == "__main__":
    pik = Pikwizard(search = "cute cats", num_images = 5, path = "downloads", num_workers = 8, height = -1, width = -1, verbose = True)
    pik.download()
    










