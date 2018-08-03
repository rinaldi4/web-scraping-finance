from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time
from selenium.webdriver.common.keys import Keys
import csv


def get_balance_sheet(tckr, file_path):
    pass
     #start browser to page and click on financials
     url = "https://www.morningstar.com/stocks/xnys/" + tckr + "/quote.html"
     browser = webdriver.Firefox()
     browser.get(url)
     browser.find_element_by_link_text('Financials').click()
     WebDriverWait(browser, 15).until(lambda browser: browser.find_element_by_link_text('All Financials Data'))
      
     #click on 'all financials data'    
     browser.find_element_by_link_text('All Financials Data').send_keys(Keys.CONTROL + Keys.RETURN)
     time.sleep(1)
     #switch to second window and wait for text to appear
     windows = browser.window_handles
     browser.switch_to_window(windows[1])
     WebDriverWait(browser, 15).until(lambda browser: browser.find_element_by_link_text('Balance Sheet'))
     time.sleep(2)
      
     browser.find_element_by_link_text('Balance Sheet').send_keys(Keys.CONTROL + Keys.RETURN)
     time.sleep(2)
     windows = browser.window_handles
     browser.switch_to.windows(windows[0])
     browser.close()
     browser.switch_to.window(windows[1])
     browser.close()
     browser.switch_to_window(windows[-1])
     WebDriverWait(browser, 15).until(lambda browser: browser.find_element_by_link_text('Balance Sheet'))
      
      
     #find left column with row titles
     page_two_soup = BeautifulSoup(browser.page_source, 'html.parser')
     parent_left = page_two_soup.find('div', {'class':'r_xcmenu rf_table_left'})
     column_1 = parent_left.findChildren(recursive = False)
    
    master_list=[]
 #================================================================================================

    for row in column_1:
        data_list = []
        
        if row.attrs['class'][0] == 'r_content':
            row_2 = row.findChildren(recursive = False)
            
            for part in row_2:
                data_list = []
                if part.attrs['class'][0] == 'r_content':
                    part_children = part.findChildren(recursive = False)
                    
                    for child in part_children:
                        
                
                part_lbl = part.findChildren(recursive = False)
                for i in part_lbl:
                    if i.attrs['class'][0] == 'lbl':
                        title_name = i.get_text()
                        data_list.append(title_name)
                        break
                
                
                
           
        title = row.findChildren(recursive = False)
        for part in title:
            if part.attrs['class'] == 'lbl':
                data_list.append(part.get_text())
                break
                
                
        if data_list != []:
            master_list.append(data_list)

#==================================================================================            
        
     
     
    dataset = page_two_soup.find('div', {'class':'r_xcmenu rf_table'})
    column_2 = dataset.findChildren(recursive = False)
    data_list = []
    for data in column_2[0].findChildren(recursive = False):
        data_list.append(data.get_text())
             
    for i in data_list:
        master_list[0].append(i)
     
    data = []
    column_2 = dataset.findChildren(recursive = False)
    for row in column_2:
        if row.attrs['class'][0] == 'r_content':
            data.append(row)
    index = 0
    for group in data:
        rows = group.findChildren(recursive = False)
        for element in rows:
            data_list = []
            try:
                if element.attrs['style'] == 'overflow:hidden;white-space: nowrap;' and element.get_text() == '\xa0':
                    for i in range(len(master_list[0])):
                        data_list.append('')
                    break
            except:
                pass
             
             
            try:
                if element.get_text() =='\xa0' or element.get_text() == '':
                    break
            except:
                pass
             
             
            try:
                if element.attrs['style'] =='display:none':
                    break 
            except:
                pass
             
        data_list.append(element.get_text())
        if data_list == []:
            continue
    index +=1
    for i in data_list:
        master_list[index].append(i)
 
          
              
     #write data to csv
     with open(file_path, 'w', newline='') as file:
         writer = csv.writer(file)
         writer.writerows(master_list)
      
     browser.quit()

    
    
    
    

def get_income_statement(tckr, file_path):
    #start browser to page and click on financials
    url = "https://www.morningstar.com/stocks/xnys/" + tckr + "/quote.html"
    browser = webdriver.Firefox()
    browser.get(url)
    browser.find_element_by_link_text('Financials').click()
    WebDriverWait(browser, 15).until(lambda browser: browser.find_element_by_link_text('All Financials Data'))
    
    #click on 'all financials data'    
    browser.find_element_by_link_text('All Financials Data').send_keys(Keys.CONTROL + Keys.RETURN)
    time.sleep(1)
    #switch to second window and wait for text to appear
    windows = browser.window_handles
    browser.switch_to_window(windows[1])
    WebDriverWait(browser, 15).until(lambda browser: browser.find_element_by_link_text('Income Statement'))
    time.sleep(2)
    
    #find left column with row titles
    page_two_soup = BeautifulSoup(browser.page_source, 'html.parser')
    parent_left = page_two_soup.find('div', {'class':'r_xcmenu rf_table_left'})
    column_1 = parent_left.findChildren(recursive = False)
    
    master_list =[]
    #iterate through left column to give a title to each row
    for row in column_1:
        title_list = []
        try:
            if str(row.findChildren()[0].get_text())== '\xa0':
                continue
        except:
            pass
        try:
            if row.attrs['style'] == 'display:none; _float:none;':
                continue
            elif row.findChildren()[0].attrs['style'] =='display:none; _float:none;':
                continue
        except:
            pass
        
        title = row.findChildren()[0].get_text()
        title_list.append(title)
        master_list.append(title_list)
    
    #grab dataset on the right side of the page
    dataset = page_two_soup.find('div', {'class':'r_xcmenu rf_table'})
    
    #navigate through each row of the dataset
    rows = dataset.findChildren(recursive = False)
    index = -1
    for row in rows:
        elements = row.findChildren(recursive = False)
        data_list = []
        
        try:
            if row.attrs['style'] == 'display:none':
                continue
        except:
            pass
        
        #navigate through each element of the row
        for element in elements:
            try:
                if element.attrs['style'] == 'overflow:hidden;white-space: nowrap;' and element.get_text() == '\xa0':
                    for i in range(len(master_list[0])):
                        data_list.append('')
                    break
            except:
                pass
            
            
            try:
                if element.get_text() =='\xa0':
                    break
            except:
                pass
            
            
            try:
                if element.attrs['style'] =='display:none':
                    break 
            except:
                pass
            
            try:
                if element.findChildren()[0].attrs['style'] =='display:none':
                    break
            except:
                pass
    
            indv_data = element.get_text()
            data_list.append(indv_data)
        
        if data_list == []:
                continue
                
        index += 1
        
        #append each element of a row to the row in the masterlist 
        for i in data_list:
            master_list[index].append(i)
        
            
    #write data to csv
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(master_list)
    
    browser.quit()

def get_cash_flow(tckr, file_path):
    pass
