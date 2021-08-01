#!/usr/bin/env python3
from doc.credentials import credentials
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

# setup the driver
driver = webdriver.Chrome("./bin/chromedriver.exe")
url = "https://www.adt.com/control-login"
driver.get(url)

# wait for and load all the login feilds
driver.implicitly_wait(30)
user_field = driver.find_element_by_xpath('//*[@id="username"]')
password_field = driver.find_element_by_xpath('//*[@id="password"]')
# button to remember the logging in computer
check_box = driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[4]/div[1]/div/div/div/div[1]/label')
login_button = driver.find_element_by_xpath('//*[@id="loginForm"]/div/button')
cookie_button = driver.find_element_by_xpath('//*[@id="cookie-banner-5553"]/a')

# click the accept cookies button to allow filling in useranme and password feilds
cookie_button.click()
# load the username and password from the credentials file
username = credentials['username'] 
password = credentials['password']
user_field.send_keys(username)
password_field.send_keys(password)
check_box.click()
login_button.click()

# now we must wait for the verification to kick in
driver.implicitly_wait(30)
continue_button = driver.find_element_by_xpath('//*[@id="ember465"]/div[1]/span')
continue_button.click()
# user gets 60 seconds to type in the code that was sent to their phone
# this is for 2FA
driver.implicitly_wait(60)
device_button = driver.find_element_by_xpath('//*[@id="ember478"]/div[1]/span');
device_button.click()

# now go to the video stream
driver.implicitly_wait(30)
video_link = driver.find_element_by_xpath("//*[contains(text(), 'Live Video')]")
video_link.click()

# display all videos on the screen
driver.implicitly_wait(30)
# make the videos full screen
full_screen = driver.find_element_by_css_selector('[aria-label="Full Screen"]')
full_screen.click()

# make the browser full screen
driver.fullscreen_window()
# continue to refresh the screen every 15 seconds
# this is required because ADT control wil time out very often
while True:
    time.sleep(15)
    # refresh the screen
    driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 'r')

# close the browser
# this may not run as infinite loop is set above
driver.close()
