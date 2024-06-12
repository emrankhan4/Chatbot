from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
chrome_options = Options()
chrome_options.add_experimental_option('detach', True)
# chrome_options.add_argument("--headless")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=chrome_options)
driver.maximize_window()


def scrap_about():
    
    url = 'https://www.nikles.com/about/'
    driver.get(url)
   

    Name = driver.find_element('xpath','/html/body/div[1]/div/article/div/section[1]/div[3]/div/div/div[1]/div/h1')
    niklesInShort = driver.find_element('xpath','/html/body/div[1]/div/article/div/section[3]/div[2]/div[1]/div/div[1]/div/h2')
    niklesInShortDesc = driver.find_element('xpath','/html/body/div[1]/div/article/div/section[3]/div[2]/div[1]/div/div[1]/div/h2')
    NiklesHistory={}
    # print(Name.text,niklesInShort.text,niklesInShortDesc.text)
    # print(Name.text)
    for i in range(2,16):
    
        
        
        Hxpath=f"/html/body/div[5]/div/article/div/section[5]/div/div/div/div[3]/div/div/div/div/div/div[1]/div[3]/div/div[1]/h5"
        #  /html/body/div[5]/div/article/div/section[5]/div[2]/div/div/div[3]/div/div/div/div/div/div[1]/div[6]/div/div[1]/h5
    #           #  /html/body/div[5]/div/article/div/section[5]/div/div/div/div[3]/div/div/div/div/div/div[1]/div[1]/div/div[1]/h5
    #     # path = f'html/body/div[5]/div/article/div/section[5]/div/div/div/div[3]/div/div/div/div/div/div[1]/div[{i}]/div/div[1]/div'
     
    #     # Pxpath=f'/html/body/div[1]/div/article/div/section[5]/div[2]/div/div/div[3]/div/div/div/div/div/div[1]/div[{i}]/div/div[1]/div'
        head = driver.find_element(By.XPATH,Hxpath)
    #     # para = driver.find_element('xpath',path)
    # #     # NiklesHistory['']
        print(head.text)
        # print('Head: ',head.text, 'Para: ',para.text)

scrap_about()

# driver.get('https://www.nikles.com/about/')
# name = driver.find_element('xpath','html/body/div[1]/div/article/div/section[5]/div[2]/div/div/div[3]/div/div/div/div/div/div[1]/div[1]/div/div[1]/h5')
#                                    #html/body/div[1]/div/article/div/section[5]/div[2]/div/div/div[3]/div/div/div/div/div/div[1]/div[1]/div/div[1]/h5
# print(name.text)

#driver.quit()

# html/body/div[1]/div/article/div/section[5]/div[2]/div/div/div[3]/div/div/div/div/div/div[1]/div[4]/div/div[1]/h5
# html/body/div[5]/div/article/div/section[5]/div/div/div/div[3]/div/div/div/div/div/div[1]/div[4]/div/div[1]/h5
# /html/body/div[5]/div/article/div/section[5]/div[2]/div/div/div[3]/div/div/div/div/div/div[1]/div[1]/div/div[1]/h5