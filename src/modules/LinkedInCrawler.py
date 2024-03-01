from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LinkedInCrawler:
    def __init__(self, driver):
        self.driver = driver
        self.base_url = 'https://www.linkedin.com/jobs/search/'
        self.max_vacancies = 50

    def extract_job_vacancies(self, preferences):
        try:
            self.driver.get(self.base_url)

            job_vacancies = []

            while len(job_vacancies) < self.max_vacancies:
                job_vacancies.extend(self.extract_job_info())

                # Verifica se o número de vagas coletadas atingiu o limite máximo
                if len(job_vacancies) >= self.max_vacancies:
                    break

                # Procura pelo botão de próxima página e clica nele se estiver disponível
                try:
                    next_page_button = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[aria-label="Próxima página"]'))
                    )
                    next_page_button.click()
                except:
                    break  # Sai do loop se não houver mais páginas

            return job_vacancies
        finally:
            self.driver.quit()

    def extract_job_info(self):
        job_vacancies = []

        job_elements = self.driver.find_elements(By.CLASS_NAME, "job-card-container")

        for job_element in job_elements:
            title = job_element.find_element(By.CLASS_NAME, 'ember-view.job-card-container__link.job-card-list__title').text.strip() 
            company = job_element.find_element(By.CLASS_NAME, 'job-card-container__primary-description').text.strip()
            location = job_element.find_element(By.CLASS_NAME , 'job-card-container__metadata-item').text.strip()

            job_vacancy = {
                'title': title,
                'company': company,
                'location': location
            }
            job_vacancies.append(job_vacancy)

            if len(job_vacancies) >= self.max_vacancies:
                break

        return job_vacancies
