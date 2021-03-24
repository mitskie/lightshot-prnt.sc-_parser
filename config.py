import os

MAIN_URL = 'https://prnt.sc/'

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) ' \
             'Chrome/91.0.4446.0 Safari/537.36 '

RESULT_PATH = os.path.dirname(os.path.abspath(__file__)) + '/result/'

# если скриншота не существует или просто не верная ссылка, то выдается картинка заглушка
NO_SCREENSHOT = 'st.prntscr.com/2021/02/09/0221/img/0_173a7b_211be8ff.png'
