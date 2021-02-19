from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
import logging
from pyvirtualdisplay import Display

options = ChromeOptions()
    #options.add_argument("--no-sandbox")
options.add_argument("--headless") 
driver = webdriver.Chrome(options=options)
display = Display(visible=0, size=(800, 800))  
display.start()
driver = webdriver.Chrome()

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

def login (username, password):
    logging.info('Starting the browser...')
    url = 'https://www.saucedemo.com/'
    param = ChromeOptions()
    param.add_argument("--headless") 

    driver = webdriver.Chrome(options=param)

    logging.info('Opening login page for login')

    driver.get(url)

    # login
    logging.info('Logging the user ' + username + ' in')
    driver.find_element_by_css_selector('input#password').send_keys(password)

    driver.find_element_by_css_selector('input#user-name').send_keys(username)
    driver.find_element_by_css_selector('input[value=LOGIN]').click()

    products = driver.find_element_by_css_selector('#inventory_filter_container > .product_label').text


    assert products == 'Products', 'Login is unsuccessful'


    logging.info('Login successful with user ' + username)

    # add to cart
    logging.info('Add items to cart')
    inventory_items = driver.find_elements_by_css_selector('.inventory_item')

    # loop through all items in the inventry

    for product in inventory_items:

        product_name = product.find_element_by_css_selector('.inventory_item_name').text
        product.find_element_by_css_selector('button.btn_inventory').click()

        logging.info('Item add success: ' +product_name)
    
    # number on badge
    cart_badge = driver.find_element_by_css_selector('#shopping_cart_container .shopping_cart_badge').text

    assert cart_badge == str(len(inventory_items)), 'The cart has not been filled'

    logging.info('Oops! Cart is full')    

    # cart page
    logging.info('Navigating to cart page')    
    driver.find_element_by_css_selector('a.shopping_cart_link').click()

    assert '/cart.html' in driver.current_url, 'Failed to open cart page'

    # remove from cart
    logging.info('Removing items from cart')
    cart_items = driver.find_elements_by_css_selector('.cart_item')

    remove_btn = 'button.cart_button'
    item_name_selector = '.inventory_item_name'

    for product in cart_items:
        product_name = product.find_element_by_css_selector(item_name_selector).text
        product.find_element_by_css_selector(remove_btn).click()
        logging.info('Item remove success' + product_name)
    
    cart_badge = driver.find_elements_by_css_selector('#shopping_cart_container .shopping_cart_badge')

    assert len(cart_badge) == 0, 'cart not empty yet'
    
    logging.info('Cart is now empty')

login('standard_user', 'secret_sauce')