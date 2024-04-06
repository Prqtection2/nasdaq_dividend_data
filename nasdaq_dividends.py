import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import time

# Create a new instance of Chrome Options
options = Options()

# Add the arguments to ignore SSL errors
options.add_argument('--ignore-ssl-errors=yes')
options.add_argument('--ssl-protocol=any')
options.add_argument('--ignore-certificate-errors=yes')

# Initialize the Chrome driver with the options
driver = webdriver.Chrome(options=options)

# Navigate to the webpage
driver.get('https://www.nasdaq.com/market-activity/dividends')

# Base XPath of the columns
base_xpath = '/html/body/div[2]/div/main/div[2]/div[2]/div[2]/div/div[2]/div/div[3]/div[5]/div[1]/div/table/tbody/tr[{}]/{}[{}]'

# Prepare the CSV file
with open('nasdaq.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    
    # Write the header
    writer.writerow(['Ticker', 'Name', 'Ex-Dividend Date', 'Payment Date', 'Record Date', 'Dividend', 'Indicated Annual Dividend', 'Announcement Date'])

    while True:
        # Number of rows in the tbody
        num_rows = len(driver.find_elements(By.XPATH, '/html/body/div[2]/div/main/div[2]/div[2]/div[2]/div/div[2]/div/div[3]/div[5]/div[1]/div/table/tbody/tr'))

        # Loop through each row
        for i in range(1, num_rows + 1):
            row_data = []
            
            # Get the ticker from the th element
            ticker_xpath = base_xpath.format(i, 'th', 1)
            ticker_element = driver.find_element(By.XPATH, ticker_xpath)
            ticker = ticker_element.text
            row_data.append(ticker)

            # Loop through each column
            for j in range(1, 8):
                # Generate the XPath for this cell
                xpath = base_xpath.format(i, 'td', j)

                # Find the cell element
                cell_element = driver.find_element(By.XPATH, xpath)

                # Extract the cell text
                cell_text = cell_element.text
                row_data.append(cell_text)

            # Write the row data to the CSV file
            print (row_data)
            writer.writerow(row_data)

        from selenium.common.exceptions import ElementNotInteractableException, ElementClickInterceptedException

        try:
            # Find the 'next' button
            next_button = driver.find_element(By.XPATH, '/html/body/div[2]/div/main/div[2]/div[2]/div[2]/div/div[2]/div/div[3]/div[6]/button[2]')
            
            # Try to find the element that's blocking the 'next' button and click it
            blocking_element = driver.find_element(By.ID, 'onetrust-accept-btn-handler')
            blocking_element.click()

            # Now click the 'next' button
            next_button.click()
        except NoSuchElementException:
            # No more pages
            print("No more pages.")
            break
        except ElementNotInteractableException:
            # Element not interactable, try again after a short delay
            print("Element not interactable, waiting...")
            time.sleep(2)
            next_button.click()
        except ElementClickInterceptedException:
            # Element click intercepted, try again after a short delay
            print("Element click intercepted, waiting...")
            time.sleep(2)
            next_button.click()

# Close the browser
driver.quit()
