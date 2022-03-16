from selenium import webdriver
import requests


def search_amazon(driver, item):
    if not item:
        raise Exception("Missing item")

    # Navigate to Amazon
    driver.get("http://amazon.com")
    # Find search box and input item and search
    search_box = driver.find_element_by_id(
        'twotabsearchtextbox').send_keys(item)
    search_button = driver.find_element_by_id("nav-search-submit-text").click()
    driver.implicitly_wait(3)
    print("Search page succesfully loaded")
    items = driver.find_elements_by_xpath(
        '//div[@class="a-section a-spacing-base"]')
    print(items[0].get_attribute("innerHTML"))
    for item in items:
        name = item.find_element_by_xpath(
            './/span[contains(@class, "a-size-base-plus")]')
        print(name.text)
    #     # click_next = driver.find_element_by_class_name('a-last').click()
    return driver.current_url


def get_content(driver, url):
    print("URL: ", url)
    headers = {
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://www.amazon.com/',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }
    r = requests.get(url, headers=headers)
    print(r)
    return r.status_code


def test_one(driver, item):
    url = search_amazon(driver, item)
    assert(get_content(driver, url) == 200)


def main():
    driver = webdriver.Chrome(executable_path=r'/usr/bin/chromedriver.exe')
    test_one(driver, "Mickey Mouse")
    driver.quit()
    return 1


if __name__ == "__main__":
    main()
