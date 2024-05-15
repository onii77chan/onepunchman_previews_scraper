import os
import requests
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from time import sleep


def scrape_previews():
    tom = 1
    chapter = 1

    driver = webdriver.Firefox()
    save_directory = r"C:\Users\ToTo\PycharmProjects\my_pjs\onepunchman_preview_scraper\scrape results"

    while chapter < 87:
        url = f'https://readmanga.live/vanpanchmen/vol{tom}/{chapter}?mtr=true'
        try:
            driver.get(url)
            sleep(1.5)

            manga_preview = driver.find_element(By.ID, "mangaPicture")
            src_value = manga_preview.get_attribute("src")

            image_name = f'one_p_man_prevs_vol{tom}_chap{chapter}.jpg'
            save_path = os.path.join(save_directory, image_name)

            manga_preview_data = requests.get(src_value).content
            with open(save_path, 'wb') as handler:
                handler.write(manga_preview_data)
            print(f'Изображение успешно скачано! {image_name}')
            chapter += 1

        except NoSuchElementException:
            print(f'Глава {chapter} тома {tom} не найдена, переход к следующей главе или тому...')
            chapter += 1
            try:
                driver.get(f'https://readmanga.live/vanpanchmen/vol{tom}/{chapter}?mtr=true')
                sleep(1.5)
                driver.find_element(By.ID, "mangaPicture")
            except NoSuchElementException:
                chapter -= 1
                tom += 1
                try:
                    driver.get(f'https://readmanga.live/vanpanchmen/vol{tom}/{chapter}?mtr=true')
                    sleep(1.5)
                    driver.find_element(By.ID, "mangaPicture")
                except NoSuchElementException:

                    print("Достигнут последний том манги. Скрапинг завершен.")
                    break


if __name__ == '__main__':
    scrape_previews()
