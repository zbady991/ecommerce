from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import pytest

@pytest.fixture
def browser():
    options = Options()
    options.add_argument('--headless')  # Run tests in headless mode
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    try:
        driver = webdriver.Chrome(options=options)
    except Exception as e:
        pytest.fail(f"WebDriver initialization failed: {e}")
    driver.implicitly_wait(10)
    try:
        yield driver
    finally:
        driver.quit()

def test_home_page(browser):
    browser.get('http://localhost:5000/')
    assert 'E-Commerce Store' in browser.title
    assert 'Welcome to Our E-Commerce Store' in browser.page_source

def test_registration(browser):
    browser.get('http://localhost:5000/auth/register')
    
    # Fill out the form
    browser.find_element(By.ID, 'username').send_keys('newuser')
    browser.find_element(By.ID, 'email').send_keys('new@example.com')
    browser.find_element(By.ID, 'password').send_keys('testpass123')
    browser.find_element(By.ID, 'confirm_password').send_keys('testpass123')
    browser.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    
    # Verify success message and redirection
    try:
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'alert-success'))
        )
        assert 'Registration successful' in browser.page_source
        assert 'Login' in browser.page_source
    except TimeoutException:
        pytest.fail("Registration success message not found within the timeout period")

def test_product_flow(browser):
    # Login first
    browser.get('http://localhost:5000/auth/login')
    browser.find_element(By.ID, 'username').send_keys('testuser')
    browser.find_element(By.ID, 'password').send_keys('testpass')
    browser.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    
    # Go to products
    browser.get('http://localhost:5000/products')
    product_link = browser.find_element(By.LINK_TEXT, 'View Details')
    product_link.click()
    
    # Add to cart
    browser.find_element(By.NAME, 'quantity').clear()
    browser.find_element(By.NAME, 'quantity').send_keys('1')
    browser.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    
    # Verify cart
    assert 'Product added to cart' in browser.page_source
    assert 'Test Product' in browser.page_source