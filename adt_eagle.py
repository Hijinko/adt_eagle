#!/usr/bin/env python3
from doc.credentials import credentials
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
# setup the driver
# if the users has a windows device than set drive to the exe under bin
# else the driver should be the default path
if ('nt' == os.name):
    driver = webdriver.Chrome("./bin/chromedriver.exe", chrome_options=options)
else:
    driver = webdriver.Chrome(chrome_options=options)
url = "https://www.adt.com/control-login"
driver.get(url)

# wait for and load all the login feilds
driver.implicitly_wait(30)
user_field = driver.find_element_by_xpath('//*[@id="username"]')
password_field = driver.find_element_by_xpath('//*[@id="password"]')
# button to remember the logging in computer
check_box = driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[4]/div[1]/div/div/div/div[1]/label')
login_button = driver.find_element_by_xpath('//*[@id="loginForm"]/div/button')
cookie_button = driver.find_element_by_link_text("DISMISS")
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
continue_button = driver.find_element_by_xpath("//span[text()='Continue']")
continue_button.click()
# user gets 60 seconds to type in the code that was sent to their phone
# this is for 2FA
driver.implicitly_wait(60)
device_button = driver.find_element_by_xpath("//span[text()='Trust Device']");
device_button.click()

# now go to the video stream
driver.implicitly_wait(30)
video_link = driver.find_element_by_xpath("//*[contains(text(), 'Live Video')]")
video_link.click()

driver.fullscreen_window()
# display all videos on the screen
# make the videos full screen
full_screen = driver.find_element_by_xpath("//title[text()='Full Screen']")

full_screen.click()

# make the browser full screen
#driver.fullscreen_window()
#reset driver to default wait
driver.implicitly_wait(0)
while True:
    # continue to press the play buttons if they time out
    plays = driver.find_elements_by_xpath("//span[text()='Play']")
    if (0 != len(plays)):
        for play in plays:
            play.click()
    # sometime the streams time out and need to be restarted
    reconnects = driver.find_elements_by_xpath("//span[text()='Retry']")
    if (0 != len(reconnects)):
        for reconnect in reconnects:
            reconnect.click()
        # refresh the page to prevent timeouts
        body.refresh()

# close the browser
# this may not run as infinite loop is set above
driver.close()
