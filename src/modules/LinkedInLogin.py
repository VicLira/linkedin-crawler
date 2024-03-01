from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LinkedInLogin:
    def __init__(self, email, password, driver):
        self.email = email
        self.password = password
        self.driver = driver

    def wait_for_redirection(self):
        WebDriverWait(self.driver, 20).until(EC.url_contains("linkedin.com/feed"))

    def login_successful(self):
        return "linkedin.com/feed" in self.driver.current_url

    def login(self):
        self.driver.get("https://www.linkedin.com/login")

        try:
            email_field = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.ID, "username")))
            email_field.send_keys(self.email)

            password_field = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.ID, "password")))
            password_field.send_keys(self.password)

            password_field.send_keys(Keys.RETURN)

            self.wait_for_redirection()

            if self.login_successful():
                print("Login bem-sucedido")
            else:
                print("Falha no login: Redirecionamento incorreto")
        except Exception as e:
            print(f"Falha no login: {str(e)}")

    def close(self):
        self.driver.quit()
