from flask import Flask, render_template, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd

app = Flask(__name__)


def init_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/login', methods=['POST'])
def login_automation():
    data = request.form
    url = data.get('url')
    username = data.get('username')
    password = data.get('password')

    driver = init_driver()
    driver.get(url)
    time.sleep(2)

    try:
        driver.find_element(By.NAME, "username").send_keys(username)
        driver.find_element(By.NAME, "password").send_keys(password)
        driver.find_element(By.NAME, "password").send_keys(Keys.RETURN)
        time.sleep(3)
        driver.quit()
        return render_template('index.html', message="Login automation completed!")
    except Exception as e:
        driver.quit()
        return render_template('index.html', message=f"Error: {str(e)}")


@app.route('/scrape', methods=['POST'])
def scrape_data():
    data = request.form
    url = data.get('url')

    driver = init_driver()
    driver.get(url)
    time.sleep(2)

    titles = driver.find_elements(By.TAG_NAME, "h2")
    data_list = [title.text for title in titles]
    driver.quit()

    df = pd.DataFrame({'Titles': data_list})
    df.to_csv('static/scraped_data.csv', index=False)

    return render_template('index.html', message="Data scraped successfully!", file_link="/static/scraped_data.csv")


if __name__ == '__main__':
    app.run(debug=True)
