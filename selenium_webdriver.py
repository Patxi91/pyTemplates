from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def main(url):
    """
    Scrapes the MVP profiles from the MVP search page and opens their LinkedIn profiles in new tabs.

    Args:
        url (str): The URL of the MVP search page to scrape.

    Returns:
        None.
    """

    # Create the driver instance
    driver = webdriver.Chrome()
    driver.get(url)

    try:
        # Find and click the "I Accept" button if it exists
        accept_button = driver.find_element(By.XPATH, "//button[text()='I Accept']")
        accept_button.click()
    except:
        # If the button is not found, continue without clicking it
        pass

    # Find all links on the page and iterate over them
    links = driver.find_elements(By.TAG_NAME, 'a')
    for link in links:
        href = link.get_attribute('href')
        if href is not None and 'mvp.microsoft.com/en-us/PublicProfile/' in href:
            # If the link contains 'mvp.microsoft.com/en-us/PublicProfile/', visit the link
            driver.execute_script("window.open('"+href+"', '_blank');")
            driver.switch_to.window(driver.window_handles[-1])
            try:
                # Wait for the LinkedIn profile link to be present and click it
                linkedin_link = WebDriverWait(driver, 3).until(
                    EC.presence_of_element_located((By.XPATH, "//a[contains(@href, 'linkedin.com/in/')]"))
                )
                linkedin_url = linkedin_link.get_attribute('href')
                print(linkedin_url)
                #driver.execute_script("window.open('"+linkedin_url+"', '_blank');")
            except:
                # If the LinkedIn link is not found, continue to the next link
                pass

            # Close the current tab
            driver.close()

            # Switch back to the first tab
            driver.switch_to.window(driver.window_handles[0])

    # Close the driver
    driver.quit()


main("https://mvp.microsoft.com/en-us/MvpSearch?&lo=United%20States&sc=e&ps=48&pn=1")
