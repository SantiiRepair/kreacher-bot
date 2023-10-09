import io
import os
import requests
from PIL import Image
from asyncio import sleep
from typing import List, Union
from urllib.parse import urlparse
from selenium.webdriver.common.by import By

from bot import driver


class ImageScraper:
    def __init__(
        self,
        image_path,
        search_key="kreacher",
        number_of_images=1,
        min_resolution=(0, 0),
        max_resolution=(1920, 1080),
        max_missed=10,
    ):
        image_path = os.path.join(image_path, search_key)
        if not isinstance(number_of_images, int):
            raise AttributeError("number of images must be integer value.")
        if not os.path.exists(image_path):
            os.makedirs(image_path)

        self.driver = driver
        self.search_key = search_key
        self.number_of_images = number_of_images
        self.image_path = image_path
        self.url = (
            "https://www.google.com/search?q=%s&source=lnms&tbm=isch&sa=X&ved=2ahUKEwie44_AnqLpAhUhBWMBHUFGD90Q_AUoAXoECBUQAw&biw=1920&bih=947"
            % (search_key)
        )
        self.min_resolution = min_resolution
        self.max_resolution = max_resolution
        self.max_missed = max_missed

    def find_image_urls(self) -> Union[List, None]:
        """Search and return a list of image urls based on the search key."""
        self.driver.get(self.url)
        image_urls = []
        count = 0
        missed_count = 0
        indx_1 = 0
        indx_2 = 0
        search_string = '//*[@id="islrg"]/div[1]/div[%s]/a[1]/div[1]/img'
        sleep(3)
        while self.number_of_images > count and missed_count < self.max_missed:
            if indx_2 > 0:
                try:
                    imgurl = self.driver.find_element(
                        By.XPATH, search_string % (indx_1, indx_2 + 1)
                    )
                    imgurl.click()
                    indx_2 = indx_2 + 1
                    missed_count = 0
                except Exception:
                    try:
                        imgurl = self.driver.find_element(
                            By.XPATH, search_string % (indx_1 + 1, 1)
                        )
                        imgurl.click()
                        indx_2 = 1
                        indx_1 = indx_1 + 1
                    except:
                        indx_2 = indx_2 + 1
                        missed_count = missed_count + 1
            else:
                try:
                    self.driver.find_element(
                        By.XPATH, search_string % (indx_1 + 1)
                    ).click()
                    missed_count = 0
                    indx_1 = indx_1 + 1
                except Exception:
                    try:
                        self.driver.find_element(
                            By.XPATH,
                            '//*[@id="islrg"]/div[1]/div[%s]/div[%s]/a[1]/div[1]/img'
                            % (indx_1, indx_2 + 1),
                        ).click()
                        missed_count = 0
                        indx_2 = indx_2 + 1
                        search_string = (
                            '//*[@id="islrg"]/div[1]/div[%s]/div[%s]/a[1]/div[1]/img'
                        )
                    except Exception:
                        indx_1 = indx_1 + 1
                        missed_count = missed_count + 1

            try:
                sleep(1)
                class_names = ["n3VNCb", "iPVvYb", "r48jcc", "pT0Scc"]
                images = [
                    self.driver.find_elements(By.CLASS_NAME, class_name)
                    for class_name in class_names
                    if len(self.driver.find_elements(By.CLASS_NAME, class_name)) != 0
                ][0]
                for image in images:
                    src_link = image.get_attribute("src")
                    if ("http" in src_link) and (not "encrypted" in src_link):
                        image_urls.append(src_link)
                        count += 1
                        break
            except Exception:
                return None

            try:
                if count % 3 == 0:
                    self.driver.execute_script(
                        "window.scrollTo(0, " + str(indx_1 * 60) + ");"
                    )
                self.driver.find_element(By.CLASS_NAME, "mye4qd").click()
                sleep(3)
            except Exception:
                sleep(1)
        return image_urls

    def save_images(self, image_urls: list, keep_filenames: bool) -> Union[str, None]:
        """Takes in an array of image urls and save it into the given path."""
        for i, image_url in enumerate(image_urls):
            try:
                search_string = "".join(e for e in self.search_key if e.isalnum())
                image = requests.get(image_url, timeout=5)
                if image.status_code == 200:
                    with Image.open(io.BytesIO(image.content)) as image_from_web:
                        try:
                            if keep_filenames:
                                o = urlparse(image_url)
                                image_url = o.scheme + "://" + o.netloc + o.path
                                name = os.path.splitext(os.path.basename(image_url))[0]
                                filename = "%s.%s" % (
                                    name,
                                    image_from_web.format.lower(),
                                )
                            else:
                                filename = "%s%s.%s" % (
                                    search_string,
                                    str(i),
                                    image_from_web.format.lower(),
                                )

                            image_path = os.path.join(self.image_path, filename)
                            image_from_web.save(image_path)
                            return image_path
                        except OSError:
                            rgb_im = image_from_web.convert("RGB")
                            rgb_im.save(image_path)
                            return image_path
                        image_resolution = image_from_web.size
                        if image_resolution is not None:
                            if (
                                image_resolution[0] < self.min_resolution[0]
                                or image_resolution[1] < self.min_resolution[1]
                                or image_resolution[0] > self.max_resolution[0]
                                or image_resolution[1] > self.max_resolution[1]
                            ):
                                image_from_web.close()
                                os.remove(image_path)

                        image_from_web.close()
            except Exception as e:
                return None
