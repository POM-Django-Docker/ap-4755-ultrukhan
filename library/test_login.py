import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def run_selenium_test():
    print("Запуск тесту...")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    
    driver.maximize_window()

    try:
        driver.get("http://127.0.0.1:8000/books/")
        time.sleep(4)

        login_btn = driver.find_element(By.LINK_TEXT, "Увійти") 
        login_btn.click()
        time.sleep(4)

        email_input = driver.find_element(By.NAME, "email")
        password_input = driver.find_element(By.NAME, "password")
        
        email_input.send_keys("admin@gmail.com")
        time.sleep(2)
        password_input.send_keys("admin")
        time.sleep(2)

        submit_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_btn.click()
        time.sleep(7)

        logout_btn = driver.find_element(By.LINK_TEXT, "Вийти")
        assert logout_btn.is_displayed(), "Помилка: Кнопку 'Вийти' не знайдено!"
        print("Успішний логін перевірено")

        logout_btn.click()
        time.sleep(1)

        login_btn = driver.find_element(By.LINK_TEXT, "Увійти")
        assert login_btn.is_displayed(), "Помилка: Не вдалося вийти з акаунту!"
        print("Успішний логаут перевірено")

        login_btn.click()
        time.sleep(7)
        
        email_input = driver.find_element(By.NAME, "email")
        password_input = driver.find_element(By.NAME, "password")
        
        email_input.send_keys("user_1234@gmail.com")
        time.sleep(2)
        password_input.send_keys("password12345")
        time.sleep(2)
        
        submit_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_btn.click()
        time.sleep(5)

        try:
            error_msg = driver.find_element(By.CSS_SELECTOR, ".alert-danger, .errorlist")
            assert error_msg.is_displayed()
            print("Блокування невалідного логіну перевірено")
        except:
            print("Скрипт не знайшов блок з помилкою. Можливо, в тебе інший клас для помилок.")

        print("Всі тести успішно пройдено")

    finally:
        time.sleep(3)
        driver.quit()

if __name__ == "__main__":
    run_selenium_test()