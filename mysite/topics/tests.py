from django.test import TestCase
from django.contrib.auth.models import User
from .models import Topic, Comment
from .forms import TopicForm, CommentForm, RegisterForm, LoginForm
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from django.contrib.auth.models import User
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Model testing
class TopicModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.topic = Topic.objects.create(title='Test Topic', description='Test Description', author=self.user)

    def test_topic_creation(self):
        self.assertEqual(self.topic.title, 'Test Topic')
        self.assertEqual(self.topic.description, 'Test Description')
        self.assertEqual(self.topic.author, self.user)

class CommentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.topic = Topic.objects.create(title='Test Topic', description='Test Description', author=self.user)
        self.comment = Comment.objects.create(topic=self.topic, text='Test Comment', author=self.user)

    def test_comment_creation(self):
        self.assertEqual(self.comment.text, 'Test Comment')
        self.assertEqual(self.comment.author, self.user)
        self.assertEqual(self.comment.topic, self.topic)

# Form testing
class TopicFormTest(TestCase):
    def test_valid_topic_form(self):
        form = TopicForm(data={'title': 'Test Topic', 'description': 'Test Description'})
        self.assertTrue(form.is_valid())

    def test_invalid_topic_form(self):
        form = TopicForm(data={'title': '', 'description': 'Test Description'})
        self.assertFalse(form.is_valid())

class CommentFormTest(TestCase):
    def test_valid_comment_form(self):
        form = CommentForm(data={'text': 'Test Comment'})
        self.assertTrue(form.is_valid())

    def test_invalid_comment_form(self):
        form = CommentForm(data={'text': ''})
        self.assertFalse(form.is_valid())

class RegisterFormTest(TestCase):
    def test_valid_register_form(self):
        form = RegisterForm(data={
            'username': 'testuser',
            'password': 'password123',
            'confirm_password': 'password123'
        })
        self.assertTrue(form.is_valid())

    def test_password_mismatch(self):
        form = RegisterForm(data={
            'username': 'testuser',
            'password': 'password123',
            'confirm_password': 'differentpassword'
        })
        self.assertFalse(form.is_valid())

class LoginFormTest(TestCase):
    def test_valid_login_form(self):
        form = LoginForm(data={'username': 'testuser', 'password': 'password123'})
        self.assertTrue(form.is_valid())

# View testing
from django.urls import reverse
from django.test import Client

class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')

    def test_topic_list_view(self):
        response = self.client.get(reverse('topic_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'topics/topic_list.html')

    def test_login_view(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'topics/login.html')

    def test_add_comment_view_authenticated(self):
        self.client.login(username='testuser', password='password')
        topic = Topic.objects.create(title='Test Topic', description='Test Description', author=self.user)
        follow_response = self.client.get(reverse('add_comment', args=[topic.id]), follow=True)
        self.assertEqual(follow_response.status_code, 200)


    def test_add_comment_view_unauthenticated(self):
        response = self.client.get(reverse('add_comment', args=[1]))
        self.assertEqual(response.status_code, 302)

    def test_delete_comment_view_authenticated(self):
        self.client.login(username='testuser', password='password')
        topic = Topic.objects.create(title='Test Topic', description='Test Description', author=self.user)
        comment = Comment.objects.create(topic=topic, text='Test Comment', author=self.user)
        response = self.client.get(reverse('delete_comment', args=[comment.id]))  # comment.id usado aqui
        self.assertEqual(response.status_code, 302)


    def test_delete_comment_view_unauthenticated(self):
        response = self.client.get(reverse('delete_comment', args=[1]))
        self.assertEqual(response.status_code, 302)

    def test_edit_topic_view_authenticated(self):
        self.client.login(username='testuser', password='password')
        topic = Topic.objects.create(title='Test Topic', description='Test Description', author=self.user)
        response = self.client.get(reverse('edit_topic', args=[topic.id]))  # topic.id usado aqui
        self.assertEqual(response.status_code, 200)

    def test_edit_topic_view_unauthenticated(self):
        response = self.client.get(reverse('edit_topic', args=[1]))
        self.assertEqual(response.status_code, 302)

    def test_delete_topic_view_authenticated(self):
        self.client.login(username='testuser', password='password')
        topic = Topic.objects.create(title='Test Topic', description='Test Description', author=self.user)
        follow_response = self.client.get(reverse('delete_topic', args=[topic.id]), follow=True)


    def test_delete_topic_view_unauthenticated(self):
        response = self.client.get(reverse('delete_topic', args=[1]))
        self.assertEqual(response.status_code, 302)

    def test_create_topic_view_authenticated(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('create_topic'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'topics/create_topic.html')

    def test_create_topic_view_unauthenticated(self):
        response = self.client.get(reverse('create_topic'))
        self.assertEqual(response.status_code, 302)

    def test_profile_view_authenticated(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'topics/profile.html')

    def test_profile_view_unauthenticated(self):
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 302)

    def test_register_view(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'topics/register.html')

    def test_login_view(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'topics/login.html')

    def test_logout_view_authenticated(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)

    def test_logout_view_unauthenticated(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)

# User auth testing
class UserAuthTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_register_user(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'password': 'password123',
            'confirm_password': 'password123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful registration
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_login_user(self):
        user = User.objects.create_user(username='testuser', password='password')
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'password'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful login
        self.assertTrue('_auth_user_id' in self.client.session)

    def test_logout_user(self):
        user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)  # Redirect after logout
        self.assertFalse('_auth_user_id' in self.client.session)

# Selenium tests
class SeleniumTests(LiveServerTestCase):
    def setUp(self):
        options = webdriver.FirefoxOptions()
        options.add_argument('--headless')
        self.driver = webdriver.Firefox(options=options)
        self.driver.implicitly_wait(10)
        User.objects.create_user(username='testuser', password='password')

    def tearDown(self):
        self.driver.quit()

    def auth_user(self):
        driver = self.driver
        driver.get('%s%s' % (self.live_server_url,'/topics/login'))
        username_input = driver.find_element(By.NAME, 'username')
        password_input = driver.find_element(By.NAME, 'password')
        login_button = driver.find_element(By.XPATH, '//input[@type="submit"]')

        username_input.send_keys('testuser')
        password_input.send_keys('password')

        login_button.click()

    def create_topic(self):
        driver = self.driver
        driver.get('%s%s' % (self.live_server_url,'/topics/topic/new/'))
        title_input = driver.find_element(By.NAME, 'title')
        content_input = driver.find_element(By.NAME, 'description')
        submit_button = driver.find_element(By.XPATH, '//input[@type="submit"]')

        title_input.send_keys('Test Topic')
        content_input.send_keys('Test Description')
        submit_button.click()

    def get_latest_topic_id(self):
        # Simplest solution but relies on the database. Doesn't get the id from the web page.
        # latest_topic = Topic.objects.latest('id')
        # return latest_topic.id
        driver = self.driver
        driver.get('%s%s' % (self.live_server_url, '/topics/'))
        latest_topic = driver.find_element(By.XPATH, "(//a[contains(@href, '/topics/topic/') and not(contains(@href, 'new'))])[1]")
        return latest_topic.get_attribute('href').split('/')[-2]

    def test_auth_user(self):
        driver = self.driver
        self.auth_user()

        driver.get('%s%s' % (self.live_server_url,'/topics/profile'))
        driver.find_element(By.XPATH, "//*[text()=concat('testuser', \"'s Profile\")]")

    def test_create_topic(self):
        driver = self.driver
        self.auth_user()
        self.create_topic()

        driver.get('%s%s' % (self.live_server_url,'/topics/'))
        driver.find_element(By.XPATH, "//*[contains(text(),'Test Topic')]")

    def test_comment_on_topic(self):
        driver = self.driver
        self.auth_user()
        self.create_topic()
        topic_id = self.get_latest_topic_id()

        driver.get('%s%s' % (self.live_server_url, f'/topics/topic/{topic_id}/'))

        comment_input = driver.find_element(By.NAME, 'text')
        comment_button = driver.find_element(By.XPATH, '//button[@type="submit"]')

        comment_input.send_keys('add comment')
        comment_button.click()

        driver.get('%s%s' % (self.live_server_url, f'/topics/topic/{topic_id}/'))
        driver.find_element(By.XPATH, "//*[contains(text(),'add comment')]")

    def test_delete_topic(self):
        driver = self.driver
        self.auth_user()
        self.create_topic()
        topic_id = self.get_latest_topic_id()

        driver.get('%s%s' % (self.live_server_url, f'/topics/topic/{topic_id}/'))

        delete_button = driver.find_element(By.XPATH, "//a[@class='btn btn-outline-danger']")
        delete_button.click()

        driver.get('%s%s' % (self.live_server_url, f'/topics/topic/{topic_id}/delete/'))
        delete_button = driver.find_element(By.XPATH, '//button[@type="submit"]')
        delete_button.click()

        driver.get('%s%s' % (self.live_server_url, '/topics/'))
        self.assertNotIn('Test Topic', driver.page_source)

    def test_create_topic_saves_to_db(self):
        driver = self.driver
        self.auth_user()
        self.create_topic()

        topic_exists = Topic.objects.filter(title="Test Topic", description="Test Description").exists()
        self.assertTrue(topic_exists)
