from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time
from selenium.webdriver.common.keys import Keys
import csv
from functions import get_balance_sheet
from functions import get_income_statement
from functions import get_cash_flow

class Stock_object():
    def __init__(self, tckr):
        self.tckr = tckr
        self.last_close = 0
        self.market_cap = 0
        self.income_csv = 'C:\\Users\\antho\\Desktop\\web-scraping finance\\CSV Data\\' + tckr.lower() + '-income.csv'
        self.balance_csv = 'C:\\Users\\antho\\Desktop\\web-scraping finance\\CSV Data\\' + tckr.lower() + '-balance.csv'
        self.cash_csv = 'C:\\Users\\antho\\Desktop\\web-scraping finance\\CSV Data\\' + tckr.lower() + '-cash.csv'
        
        self.get_stock_data()
        self.get_csv_file('income')
        #=======================================================================
        # self.get_csv_file('balance')
        # self.get_csv_file('cash')
        #=======================================================================


    def get_stock_data(self):
        #setup browser
        url = "https://www.morningstar.com/stocks/xnys/" + self.tckr + "/quote.html"
        browser = webdriver.Firefox()
        browser.get(url)
        time.sleep(5)
        page_source = browser.page_source
        page_soup = BeautifulSoup(page_source, 'html.parser')
        
    #     no_of_pg_down = 20
        
        #while no_of_pg_down > 0:
            #elem.send_keys(Keys.PAGE_DOWN)
            #element = WebDriverWait(browser).until(EC.presence_of_all_elements_located(()))
            #time.sleep(.5)
            #no_of_pg_down -=1
        
        
        #get last close price and store
        last_price = float(page_soup.find('text', {'class':'previous-close-value'}).get_text())
        self.last_close = last_price
        
        #get market cap and store
        caps = page_soup.find_all('div', {'class':'dp-name ng-binding'})
        for cap in caps:
            if cap.get_text() =='Market Cap':
                cap = cap
                break
            else:
                pass
        #find parent and list of children to find market cap
        parent = cap.parent
        children = parent.findChildren()
        market_cap= children[1].get_text()
        
        #break market cap into value and str (i.e. 'Bil')
        market_value = market_cap[:-4]
        market_str   = market_cap[-3:]
        
        #multiply market value by correct value to get market cap total
        if market_str.lower() == 'bil':
            self.market_cap = float(market_value) * 1000000000
            
        elif market_str.lower() == 'mil':
            self.market_cap = float(market_value) * 1000000
            
        else:
            self.market_cap = market_cap
        
        browser.quit()
        #===============================================================================
        # #look for 'financials' tag at head of page
        # list = page_soup.find_all('a', {'class':'ng-binding'})
        # 
        # for item in list:
        #     if item.get_text() =='Financials':
        #         print('Found "financials"')
        #         break
        #           #browser.find_elements_by_xpath(''//*[@id="sal-components-nav"]/div/div/nav[2]/ul/li[5]/a').click()
        #         #time.sleep(5)
        #     else:
        #         pass
        #===============================================================================
        
    def get_csv_file(self, statement):
        #starts up browser
#         url = "https://www.morningstar.com/stocks/xnys/" + self.tckr + "/quote.html"
#         browser = webdriver.Chrome()
#         browser.get(url)
#         time.sleep(5)
#         #click on 'financials' at top of page    
#         browser.find_element_by_link_text('Financials').click()
#         time.sleep(3)
        
        
        #===============================================================================
        # #look for tag 'all financials data' underneath financial data
        # list_1 = page_soup.find_all('a', {'class':'ng-binding'})
        #  
        # for item in list_1:
        #     if item.get_text() =='Financials':
        #         print('Found "financials"')
        #         break
        #         #browser.find_elements_by_xpath(''//*[@id="sal-components-nav"]/div/div/nav[2]/ul/li[5]/a').click()
        #         #time.sleep(5)
        #     else:
        #         pass
        #===============================================================================
        
        #click on 'all financials data' underneath financials section
        #browser.find_element_by_link_text('All Financials Data').click()        
        
        #get data and header_row from website
        #all data may not contain same # of columns, iterate over sister columns
        #and rows instead of grabbing directly for each one
        #i.e. start at first element and iterate through
        
        #create master lsit
        #create sublist with row info
        #masterlist.append(sublist)
        
        if statement == 'income':
            get_income_statement(self.tckr, self.income_csv)
        elif statement =='balance':
            get_balance_sheet(self.tckr, self.balance_csv)
        elif statement =='cash':
            get_cash_flow(self.tckr, self.cash_csv)
        else:
            raise ValueError('No such type of statement.')
        
        
#         page_two_soup = BeautifulSoup(browser.page_source, 'html.parser')
#         parent_left = page_two_soup.find_all('div', {'class':'r_xcmenu rf_table_left'})
#         column_1 = parent_left.findChildren()
#         
#         master_list =[]
# 
#         for row in len(column_1):
#             title_list = []
#             try:
#                 title = column_1[row].findChildren()[0].get_text()
#                 if title == '&nbsp;':
#                     break
#                 elif column_1[row].attrs['style'] == 'display:none; _float:none;':
#                     break
#                 else:
#                     title_list.append(title)
#                     master_list.append(title_list)
#             except:
#                 pass
#         
#         dataset = page_two_soup.find_all('div', {'class':'r_xcmenu rf_table'})
#         for row in dataset.findChildren():
#             index = 0
#             elements = row.findChildren()
#             data_list = []
#             for element in elements:
#                 try:
#                     indv_data = element.get_text()
#                     if indv_data =='&nbsp;':
#                         break
#                     elif element.attrs['style'] =='display:none':
#                         break
#                     else:
#                         data_list.append(indv_data)
#                 except:
#                     pass
#             for i in data_list:
#                 master_list[index].append(i)
#             index += 1
#         
#         #write data to csv
#         with open(self.csv, 'w', newline='') as file:
#             writer = csv.writer(file)
#             writer.writerows(master_list)
#         
#         browser.quit()
        
        
        
        
        
        
        
        
        
        
        
        
        
if __name__ == '__main__':
    infy = Stock_object('infy')
    infy.last_close
    infy.market_cap        
        
        
        