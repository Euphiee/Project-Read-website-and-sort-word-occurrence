# import library
import requests
from bs4 import BeautifulSoup
import re
import time
import os
import psutil


# get url from user and separate website by languages (English, Chinese, Japanese)
def get_info():
    '''
    Get user's information of website and language.
    Args: NA
    Returns: 
        (str) url - user's input of url
        (str) lang - user's input of language
    '''   
    
    while True:
            try:
                url = input('\nPlease enter the website:\n')
                # request for a webpage 
                res = requests.get(url)
                #check requests ststus 
                if res.status_code == 200:
                    break
                else:
                    print('Please try another website.')
            except:
                print('Please enter a valid website.')
                continue
    
    while True:
        try:
            lang = input('\nPlease select the language of result (English, Chinese or Japanese):\n').lower()
            if lang in ['english', 'chinese', 'japanese']:
                break
            else:
                print('Please enter a valid language.')
        except:
            continue
    return url, lang

def get_html_text(url):
    '''
    Get html from website and get rid of html tag, and then convert to beautifulsoup object.
    Args: 
        (str) url - website url
    Returns: 
        (str) text - text without html tags   
    '''
    
    res = requests.get(url)
    # get html from url
    html_text = res.text
    # change to beautifulsoup object
    soup = BeautifulSoup(html_text, 'html.parser')
    # get rid of extra spaces and line breaks and change to string separete by space
    text = ' '.join(soup.stripped_strings) 
    return text
                
def text_process_en(text):
    '''
    Function for process if the selected language is English.
    Args: 
        (str) text - text without html tags  
    Returns: 
        (list) list - a list containing each word
    '''
    
    # get rid of punctuations and special characters
    clean_text = re.sub(r"[^a-zA-Z0-9]+", ' ', text)
    # get rid of numbers
    clean_text = re.sub(r'\d+', '', clean_text)
    
    # change text to a list of words
    list =  clean_text.split()
    return list
    
def text_process_jp(text):
    '''
    Function for process if the selected language is Japanese.
    Args: 
        (str) text - text without html tags    
    Returns: 
        (list) list - a list containing each hanzi
    '''
    
    # get rid of punctuations and special characters
    punctuation_jp = '[!"#$%&()*+,-./:;<=>?@[\\]：^_`{|}~「」〔〕“”〈〉『』【】＆＊・（）＄＃＠。、？！｀＋￥％]'
    clean_text = re.sub(punctuation_jp, "", text)
    # get rid of English characters and numbers
    clean_text = re.sub("[A-Za-z0-9]", '',clean_text)
    # get rid of spaces
    clean_text = clean_text.replace(' ', '') 
    
    # change text to a list of hanzi
    list = []
    for i in clean_text:
        list.append(i) 
    return list 

def text_process_ch(text):
    '''
    Function for process if the selected language is Chinese.
    Args: 
        (str) text - text without html tags  
    Returns: 
        (list) list - a list containing each hanzi
    '''
    
    # get rid of punctuations and special characters
    punctuation_ch = '[！？。＂＃＄％＆＇/（）＊＋，－／|():：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､、·〃》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘’‛“”„‟…‧﹏.]'
    clean_text = re.sub(punctuation_ch, '',text)
    # get rid of English characters and numbers
    clean_text = re.sub("[A-Za-z0-9]", '',clean_text)
    # get rid of spaces
    clean_text = clean_text.replace(' ', '') 
    
    # change text to a list of hanzi
    list = []
    for i in clean_text:
        list.append(i) 
    return list 

def sorted_result(list):  
    '''
    Function to sort the words by frequency.
    Args: 
        (list) list - a list containing each word (English) or hanzi (Chinese, Japanese)
    Returns: 
        (dic) result - a dictionary containing each word (English) or hanzi (Chinese, Japanese) and it's frequency
    ''' 
    
    # create a dictionary to store words and it's frenquency
    dic = {}
    for word in list:
        if word in dic:
            dic[word] += 1
        else:
            dic[word] = 1

    # list containing sorted the words by frenquency
    list_sort = sorted(dic, key = dic.get, reverse = True)
    # create a dictionary to show sorted results
    result = {}
    for i in list_sort:
        result[i] = dic[i]
    return result
       
def export_csv(result_dic):
    '''
    Function to export the result to a csv file.
    Args: 
        (dic) result_dic - a dictionary containing each word (English) or hanzi (Chinese, Japanese) and it's frequency
    Returns: 
        NA   
    '''
    
    with open('data.csv', 'w', encoding = 'utf-8') as f:
        for key in result_dic:
            f.write('%s, %i\n' % (key, result_dic[key]))

# def of memory and time?

def main():
    while True:
        url, lang = get_info()
        # check start time
        start = time.time()
        # check start memory
        pid = os.getpid()
        p = psutil.Process(pid)
        info_start = p.memory_full_info().uss/1024
        
        soup = get_html_text(url)
        if lang == 'english':            
            list_en = text_process_en(soup)
            result = sorted_result(list_en)
            export_csv(result)
        elif lang == 'japanese':
            list_jp = text_process_jp(soup)
            result = sorted_result(list_jp)
            export_csv(result)
        else:
            list_ch = text_process_ch(soup)
            result = sorted_result(list_ch)
            export_csv(result)
        
        print('The result file was generated.')
        # check end time and calculate running time
        end = time.time()
        print('running time: %s seconds' % str(end - start))
        # check end memory
        info_end = p.memory_full_info().uss/1024
        print('running memory: %s KB' % str(info_end - info_start))
                    
        while True:
            try:
                restart = input('\nWould you like to restart? Enter yes or no (Please change the saved file name if you want to restart).\n').lower()
                if restart in ['yes', 'no']:
                    break
                else:
                    print('Please enter a valid input.')
            except:
                continue

        if restart != 'yes':
            break
       
if __name__ == "__main__":
    main()  
    
    
    
    
    

