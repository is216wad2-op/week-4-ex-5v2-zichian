import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager

options = Options()
options.add_argument('--headless')
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# Update to the correct file path
url = 'file://' + os.path.abspath('ex5.html')
driver.get(url)
time.sleep(1)

actions = ActionChains(driver)

def get_elem_details(elem_id):
    elem = driver.find_element(By.ID, elem_id)
    bradius = elem.value_of_css_property("border-radius")
    padding_top = elem.value_of_css_property("padding-top")
    return bradius, padding_top

# Initial: should be circle, border-radius 50%
bradius, padding_top = get_elem_details("circle")
assert bradius in ["50%", "75px"], f"Expected border-radius 50% or 75px, got {bradius}"
assert padding_top in ["60px", "60.0px"], f"Initial padding-top should be 60px, got {padding_top}"

# Mouse over: becomes square, border-radius 0 and padding-top 20px
circle_elem = driver.find_element(By.ID, "circle")
actions.move_to_element(circle_elem).perform()
time.sleep(0.5)

square_elem = driver.find_element(By.ID, "square")
bradius, padding_top = get_elem_details("square")
assert bradius in ["0px", "0.0px"], f"Expected border-radius 0 when square, got {bradius}"
assert padding_top in ["20px", "20.0px"], f"Padding-top should be 20px when square, got {padding_top}"

# Mouse out: should revert to circle, border-radius 50% and padding-top 60px
actions.move_by_offset(200, 0).perform()
time.sleep(0.5)

circle_elem = driver.find_element(By.ID, "circle")
bradius, padding_top = get_elem_details("circle")
assert bradius in ["50%", "75px"], f"Expected border-radius 50% or 75px, got {bradius}"
assert padding_top in ["60px", "60.0px"], f"Padding-top should be back to 60px, got {padding_top}"

print("All tests passed!")

driver.quit()
