from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from django.contrib.auth.models import User
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginTest(LiveServerTestCase):
    def setUp(self):
        # Configurar o Chrome para modo headless (opcional)
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(10)  # Espera implícita de 10 segundos

        # Criar um utilizador de teste
        User.objects.create_user(username='testuser', password='testpass')

    def tearDown(self):
        self.driver.quit()

    def test_login(self):
        driver = self.driver
        driver.get('%s%s' % (self.live_server_url, '/login/'))  # URL da página de login

        # Encontrar campos de entrada e botão de submissão
        username_input = driver.find_element(By.NAME, 'username')
        password_input = driver.find_element(By.NAME, 'password')
        login_button = driver.find_element(By.XPATH, '//button[@type="submit"]')

        # Inserir credenciais
        username_input.send_keys('testuser')
        password_input.send_keys('testpass')

        # Submeter o formulário
        login_button.click()

        # Verificar se o login foi bem-sucedido
        welcome_message = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'welcome-message'))
        )
        self.assertIn('Bem-vindo, testuser', welcome_message.text)

    def test_create_topic(self):
        driver = self.driver
        self.test_login()  # Reutilizar o método de login

        driver.get('%s%s' % (self.live_server_url, '/topics/new/'))  # Página de novo tópico

        # Encontrar campos e botão de submissão
        title_input = driver.find_element(By.NAME, 'title')
        content_input = driver.find_element(By.NAME, 'content')
        submit_button = driver.find_element(By.XPATH, '//button[@type="submit"]')

        # Inserir dados do tópico
        title_input.send_keys('Título de Teste')
        content_input.send_keys('Conteúdo do tópico de teste.')
        submit_button.click()

        # Verificar se o tópico foi criado com sucesso
        topic_title = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'h1'))
        )
        self.assertEqual(topic_title.text, 'Título de Teste')