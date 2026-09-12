import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument('--start-maximized')
options.add_argument('--disable-blink-features=AutomationControlled')

driver = webdriver.Chrome(options=options)
try:
    print('Navigating to https://www.pacificcouncil.org/junior-fellowship-application ...')
    driver.get('https://www.pacificcouncil.org/junior-fellowship-application')
    time.sleep(3)
    
    file_input = driver.find_element(By.ID, 'edit-submitted-supporting-documents-resume-cv-upload')
    test_file = r'C:\Users\Mizan YT\Desktop\New folder\test.pdf'
    file_input.send_keys(test_file)
    print('Selected file!')
    time.sleep(1)
    
    upload_btn = driver.find_element(By.ID, 'edit-submitted-supporting-documents-resume-cv-upload-button')
    print('Clicking upload button...')
    driver.execute_script("""
        var btn = arguments[0];
        var evt = new MouseEvent('mousedown', { bubbles: true, cancelable: true, view: window });
        btn.dispatchEvent(evt);
        btn.click();
    """, upload_btn)
    
    found_url = None
    for i in range(25):
        time.sleep(1)
        links = driver.find_elements(By.XPATH, "//div[@id='edit-submitted-supporting-documents-resume-cv-ajax-wrapper']//a[contains(@href, 'system/files')]")
        if not links:
            links = driver.find_elements(By.XPATH, "//a[contains(@href, 'system/files')]")
        if links:
            found_url = links[0].get_attribute('href')
            print(f'>>> SUCCESS! Found link: {found_url}')
            break
            
    if not found_url:
        print('Wrapper content:', driver.find_element(By.ID, 'edit-submitted-supporting-documents-resume-cv-ajax-wrapper').get_attribute('outerHTML'))
finally:
    driver.quit()
