import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

options = Options()
# Headless or windowed
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")

print("Launching Chrome...")
driver = webdriver.Chrome(options=options)

try:
    print("Navigating to https://www.pacificcouncil.org/get-involved/membership/apply ...")
    driver.get("https://www.pacificcouncil.org/get-involved/membership/apply")
    time.sleep(3)

    test_file = r"C:\Users\Mizan YT\Desktop\New folder\test.pdf"
    if not os.path.exists(test_file):
        # Create a dummy test pdf if missing
        with open(test_file, "wb") as f:
            f.write(b"%PDF-1.4 sample test file")

    print(f"Selecting test file: {test_file}")
    file_input = driver.find_element(By.ID, "edit-field-statement-of-interest-und-0-upload")
    file_input.send_keys(test_file)
    time.sleep(1)

    print("Locating Upload button...")
    upload_btn = driver.find_element(By.ID, "edit-field-statement-of-interest-und-0-upload-button")
    
    # Trigger upload
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", upload_btn)
    time.sleep(0.5)
    # Drupal AJAX attaches mousedown or click event
    driver.execute_script("""
        var btn = arguments[0];
        var evt = new MouseEvent('mousedown', { bubbles: true, cancelable: true, view: window });
        btn.dispatchEvent(evt);
        btn.click();
    """, upload_btn)
    print("Upload button triggered! Waiting for AJAX upload...")

    found_url = None
    for sec in range(30):
        time.sleep(1)
        # Check for link inside the wrapper or page
        try:
            links = driver.find_elements(By.XPATH, "//div[@id='edit-field-statement-of-interest-und-0-ajax-wrapper']//a[contains(@href, 'system/files')]")
            if not links:
                links = driver.find_elements(By.XPATH, "//a[contains(@href, 'system/files')]")
            if links:
                found_url = links[0].get_attribute("href")
                print(f"\n>>> SUCCESS! Found link in DOM after {sec+1}s: {found_url}")
                break
        except Exception as e:
            pass

    if not found_url:
        print("\nWrapper outer HTML:")
        wrapper = driver.find_elements(By.ID, "edit-field-statement-of-interest-und-0-ajax-wrapper")
        if wrapper:
            print(wrapper[0].get_attribute("outerHTML"))

finally:
    driver.quit()
    print("Driver closed.")
