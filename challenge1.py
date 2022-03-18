from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import requests


def search_and_submit(driver, item):
    # Navigate to Amazon
    driver.get("http://amazon.com")
    # Find search box and input item and search
    driver.find_element_by_id(
        'twotabsearchtextbox').send_keys(item)
    driver.find_element_by_id("nav-search-submit-text").click()
    driver.implicitly_wait(3)

    # Ensure we are on the results page
    results_text = driver.find_element_by_xpath(
        '//span[contains(@class, "a-size-medium-plus a-color-base a-text-normal")]')
    assert(results_text.text == "RESULTS")
    print("Search page succesfully loaded")
    return


def get_content(url):
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


def scrape_search_items(items):
    products = []
    for item in items:
        name = item.find_element_by_xpath(
            './/span[contains(@class, "a-size-base-plus")]')
        price = item.find_elements_by_class_name('a-price-whole')
        is_prime = item.find_elements_by_xpath(
            './/i[contains(@class, "a-icon a-icon-prime a-icon-medium")]')
        products.append({
            'Name': name.text,
            'Price': price[0].text if price else "N/A",
            'Prime?': 'YES' if is_prime else 'NO'
        })
    return products


def test_search(driver, item):
    if not item:
        raise Exception("Missing item")

    search_and_submit(driver, item)

    # Find all products by scraping for name, price, and if it offers prime shipping.
    items = driver.find_elements_by_xpath(
        '//div[@class="a-section a-spacing-base"]')
    products = scrape_search_items(items[:10])
    assert(len(products) > 5)
    # assert(get_content(url) == 200)
    return


def test_cart(driver, search_keyword):
    search_and_submit(driver, search_keyword)
    # Target first search result to add to cart (save product_name_text for verification purposes)
    product_info = driver.find_element_by_xpath(
        '//a[contains(@class, "a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal")]')
    product_link = product_info.get_attribute("href")
    product_name_text = product_info.find_element_by_xpath('.//span').text

    # Go to target's page and add to cart
    driver.get(product_link)
    driver.find_element_by_id(
        "add-to-cart-button").click()

    # Once we add to cart, we are sent to a smart-wagon page
    added_to_cart_text = driver.find_element_by_xpath(
        '//span[contains(@class, "a-size-medium-plus a-color-base sw-atc-text a-text-bold")]')
    assert(added_to_cart_text.text == "Added to Cart")

    # Let's go to cart and verify the correct product was added
    driver.find_element_by_id("sw-gtc").click()
    item_in_cart = driver.find_element_by_xpath(
        './/span[contains(@class, "a-size-medium a-color-base sc-product-title")]')
    item_name = item_in_cart.find_element(By.CLASS_NAME, 'a-truncate-cut')
    assert(item_name.text[:-2] in product_name_text)
    return


def test_password(driver, email="mickey@disney.com", password="hunter123"):
    # Navigate to Amazon
    driver.get("http://amazon.com")
    sign_in_nav = driver.find_element(By.ID, 'nav-link-accountList')
    ActionChains(driver).move_to_element(sign_in_nav).perform()
    driver.find_element(By.CLASS_NAME, 'nav-action-button').click()

    # Enter email and click continue
    email_field = driver.find_element(By.ID, 'ap_email')
    email_field.send_keys(email)
    driver.find_element(By.ID, 'continue').click()

    # Enter password and click Sign-in
    password_field = driver.find_element(By.ID, 'ap_password')
    password_field.send_keys(password)
    driver.find_element(By.ID, 'signInSubmit').click()

    # Verify auth error is shown
    auth_error = driver.find_element(By.ID, 'auth-error-message-box')
    auth_error_message = auth_error.find_element(By.CLASS_NAME, 'a-list-item')
    assert("password" in auth_error_message.text)
    assert("incorrect" in auth_error_message.text)
    print(auth_error_message.text)
    return


def main():
    driver = webdriver.Chrome(executable_path=r'/usr/bin/chromedriver.exe')
    # test_search(driver, "")
    test_search(driver, "Mickey Mouse doll")
    test_search(driver, "Finding Nemo cat toy")
    test_cart(driver, "Mickey Mouse")
    test_password(driver, "mickey@disney.com", "testpassword")
    test_password(driver, "mickey@disney.com", "dory123!")
    driver.quit()
    print("All tests passed successfully!")


if __name__ == "__main__":
    main()
