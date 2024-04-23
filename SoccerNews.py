import requests
from bs4 import BeautifulSoup
import tkinter as tk
import tkinter.ttk as ttk
import urllib
import webbrowser
import matplotlib.pyplot as plt
from mplsoccer.pitch import Pitch
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import kansuu
import japanize_matplotlib

#ウィンドウを閉じる関数
def close_window():
    root.destroy()

#ウィンドウを最前面に固定する関数
def top_window():
    root.attributes('-topmost',True)

#ウィンドウを最前面を解除する関数
def back_window():
    root.attributes('-topmost',False)

#仮関数チーム情報にする予定
def show_rank():
    for tab in note.tabs():
        note.forget(tab)

#試合結果を表示
def show_result():
    for tab in note.tabs():
        note.forget(tab)
    add_match_tab(J1_soup,'J1')
    add_match_tab(J2_soup,'J2')
    add_match_tab(J3_soup,'J3')
    

def add_match_tab(soup,league_name):

    tab_result = tk.Frame(note,cursor='hand2')
    change_background(tab_result,'white')
    note.add(tab_result, text=league_name)

    for match_div in soup.find_all('div', class_='main-box-base'):
        div_data = [a.get_text(strip=True) for a in match_div.find_all('a', href=True)]
        date_elements = match_div.find(class_='main-box-child')
        date_td = date_elements.find('td')
        date= date_td.text
        match_elements = match_div.find(class_='score')
        if match_elements is None:
            continue

        match_elements_link = match_elements.find('a')

        if match_elements_link is None:
            continue

        match_elements_url = match_elements_link.get('href')
        match_url = urllib.parse.urljoin(J1_url, match_elements_url)
        home_team = div_data[1]
        away_team = div_data[4]
        score = div_data[2]
            
        if len(div_data) < 5:
            continue
        else:
            label = tk.Label(tab_result, text=f"{date}  {home_team} {score} {away_team}\n",bg='white')
            label.bind("<Button-1>", lambda e, url=match_url: webbrowser.open(url,autoraise=True))
            label.pack(anchor='w')

        note.pack(fill='both')
    

#順位タブを表示
def show_rank():
    for tab in note.tabs():
        note.forget(tab)
    add_rank_tab(J1_soup,'J1')
    add_rank_tab(J2_soup,'J2')
    add_rank_tab(J3_soup,'J3')

def add_rank_tab(soup,league_name):
    tab_rank = tk.Frame(note,cursor='hand2')
    change_background(tab_rank,'white')
    note.add(tab_rank, text=league_name)

    for match_div in soup.find_all(id="ranking_content"):
        rank_dl = match_div.find_all('dl')
        ranks = [rank.text.strip().replace('\n','位  ') for rank in rank_dl]
        for dl, rank in zip(rank_dl, ranks):
            rank_elements_url = dl.find('a').get('href')
            rank_url = urllib.parse.urljoin(url, rank_elements_url)
            label = tk.Label(tab_rank, text=f'{rank}', bg='white')
            label.bind("<Button-1>", lambda e, url=rank_url: webbrowser.open(url, autoraise=True))
            label.pack(anchor='w')
    note.pack(fill='both')   

#ニュースタブを表示
def show_news():
    for tab in note.tabs():
        note.forget(tab)
    add_news_tab(J1_news_soup,'J1')
    add_news_tab(J2_news_soup,'J2')
    add_news_tab(J3_news_soup,'J3')

def add_news_tab(soup,league_name):
    tab_news = tk.Frame(note,cursor='hand2')
    change_background(tab_news,'white')
    note.add(tab_news, text=league_name)
    news = soup.find(class_='newsList')
    
    for news_element in news.find_all('h3')[:15]:
        news_title = news_element.text
        news_element_url = news_element.find('a').get('href')
        link_url = urllib.parse.urljoin(news_url, news_element_url)
        label = tk.Label(tab_news, text=f'・{news_title}', bg='white',cursor='hand2', justify='left', wraplength=500)
        label.bind("<Button-1>", lambda e, url=link_url: webbrowser.open(url, autoraise=True))
        label.pack(anchor='w')
    note.pack()

       
#チーム名表示関数
def show_team_name(soup):
    name_class = soup.find(id="ranking_content")
    team_names= [team_name.text for team_name in name_class.findAll('div')]
    return team_names


#コンボボックスで選択した関数を実行する関数
def combo_select(event):
    global canvas_widget2
    selected_item = combobox.get()
    if selected_item =='試合結果':
        combobox2.pack_forget()
        combobox3.pack_forget()
        #label2.pack_forget()
        frame2.pack_forget()
        show_result()
    elif selected_item =='データ':
        note.pack_forget()
        combobox2.pack()
        frame2.pack()
        selected_item = combobox2.get()
        if selected_item =='J1':
            combobox3.pack()
            selected_item = combobox3.get()
            if selected_item =='平均入場者数(今季)':  
                kansuu.attend_graph(1,frame2,2024)
            elif selected_item =='平均入場者数(通算)':  
                kansuu.attend_graph(1,frame2,1993)
            elif selected_item =='時間帯別得点率(今季)':
                kansuu.time_score(1,frame2,2024) 
            elif selected_item =='時間帯別得点率(通算)':
                kansuu.time_score(1,frame2,1999)
        if selected_item =='J2':
            combobox3.pack()
            selected_item = combobox3.get()
            if selected_item =='平均入場者数(今季)':  
                kansuu.attend_graph(2,frame2,2024)
            elif selected_item =='平均入場者数(通算)':  
                kansuu.attend_graph(2,frame2,1993)
            elif selected_item =='時間帯別得点率(今季)':
                kansuu.time_score(2,frame2,2024) 
            elif selected_item =='時間帯別得点率(通算)':
                kansuu.time_score(2,frame2,1999) 
        if selected_item =='J3':
            combobox3.pack()
            selected_item = combobox3.get()
            if selected_item =='平均入場者数(今季)':  
                kansuu.attend_graph(3,frame2,2024)
            elif selected_item =='平均入場者数(通算)':  
                kansuu.attend_graph(3,frame2,1993)
            elif selected_item =='時間帯別得点率(今季)':
                kansuu.time_score(3,frame2,2024) 
            elif selected_item =='時間帯別得点率(通算)':
                kansuu.time_score(3,frame2,1999)    
    elif selected_item =='ニュース':
        note.pack_forget()
        #label2.pack_forget()
        combobox2.pack_forget()
        combobox3.pack_forget()
        frame2.pack_forget()
        show_news()
    elif selected_item =='順位':
        note.pack_forget()
        #label2.pack_forget()
        combobox2.pack_forget()
        combobox3.pack_forget()
        frame2.pack_forget()
        show_rank()


#背景色変更用関数
def change_background(tab_id, color):
    tab = note.nametowidget(tab_id)
    tab.config(bg=color)

#画面を左上に移動する関数
def move_leftup():
    root.geometry('400x650+0+0')

#ウィンドウを閉じたときに終了する関数
def close_window():
    root.destroy()
    root.quit()
    

#データサイト
all_division_url = []
for division in range(1,4):
    url = f'https://data.j-league.or.jp/SFTP01/?startPage=0&endPage=5&competitionFrameId={division}&prev_next=&nextBtnVal=0&prevBtnVal=0'
    all_division_url.append(url)
J1_url = all_division_url[0]
J1_html = requests.get(J1_url)
J1_html.encoding = 'utf-8'
J1_soup = BeautifulSoup(J1_html.text, 'html.parser')
J2_url = all_division_url[1]
J2_html = requests.get(J2_url)
J2_html.encoding = 'utf-8'
J2_soup = BeautifulSoup(J2_html.text, 'html.parser')
J3_url = all_division_url[2]
J3_html = requests.get(J3_url)
J3_html.encoding = 'utf-8'
J3_soup = BeautifulSoup(J3_html.text, 'html.parser')

#ニュースURL
all_division_news = []
for div in range(1,7):
    news_url =f'https://www.jleague.jp/news/search/?category={div}&team=&year=&month='
    all_division_news.append(news_url)
J1_news_url = all_division_news[1]
J1_news_html = requests.get(J1_news_url)
J1_news_html.encoding = 'utf-8'
J1_news_soup = BeautifulSoup(J1_news_html.text, 'html.parser')
J2_news_url = all_division_news[3]
J2_news_html = requests.get(J2_news_url)
J2_news_html.encoding = 'utf-8'
J2_news_soup = BeautifulSoup(J2_news_html.text, 'html.parser')
J3_news_url = all_division_news[5]
J3_news_html = requests.get(J3_news_url)
J3_news_html.encoding = 'utf-8'
J3_news_soup = BeautifulSoup(J3_news_html.text, 'html.parser')

#スコアURL
score_url = 'https://data.j-league.or.jp/SFRT09/search?yearFlag=false&competition_id=1&sub_competition_id=&section_id=0&number=10&competition_year_id=2024&competition_year=2024%E5%B9%B4&competitionName=%E6%98%8E%E6%B2%BB%E5%AE%89%E7%94%B0%EF%BC%AA%EF%BC%91%E3%83%AA%E3%83%BC%E3%82%B0&sub_competition=&sectionName=%E6%9C%80%E6%96%B0%E7%AF%80&section_id=0&sub_error_flag=&sub_competition_flag=1'
score_html = requests.get(score_url)
score_html.encoding = 'utf-8'
soup3 = BeautifulSoup(score_html.text, 'html.parser')


#画面を表示
root = tk.Tk()
root.geometry('650x650+600+100')
root.title('SoccerNews')


frame0 = tk.Frame(root, highlightthickness=0,bg='white')
frame0.pack(side="top", expand=False)

frame = tk.Frame(root, highlightthickness=0)
frame.pack(side="top", expand=False)

frame2 = tk.Frame(root, highlightthickness=0)
frame2.tk_setPalette(background='white')
frame2.pack(side="bottom", padx=5,pady=5)

menu_frame = tk.Frame(root)
note = ttk.Notebook(frame)
news_txt = tk.Text(padx=0, pady=0,width=55,height=40)
label3 = tk.Label(frame, text=' ', justify='left', wraplength=350)

#ピッチ
fig, ax = plt.subplots(figsize=(2,1))
plt.xkcd()
pitch = Pitch(pitch_color='grass', line_color='white', stripe=True,linewidth=1)
pitch.draw(ax)
pitch_title= ax.annotate('SoccerNews',(50, 10), fontsize=20, ha='center')
canvas = FigureCanvasTkAgg(fig, master=frame0)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack()
plt.rcdefaults()
plt.rcParams['font.family'] = ['Hiragino Maru Gothic Pro', 'Yu Gothic']

#グラフ用
canvas2 = FigureCanvasTkAgg(fig, master=frame2)
canvas_widget2 = canvas2.get_tk_widget()


#コンボボックス1(メイン)
option=['試合結果','順位','ニュース','データ']
combobox=ttk.Combobox(frame,values=option,width=9,state='readonly',)
combobox.bind("<<ComboboxSelected>>", combo_select)

#コンボボックス2(ディビジョン選択)
option2=['J1','J2','J3',]
combobox2=ttk.Combobox(frame,values=option2,width=9,state='readonly',)
combobox2.bind("<<ComboboxSelected>>", combo_select)

option3=['平均入場者数(今季)','平均入場者数(通算)','時間帯別得点率(今季)','時間帯別得点率(通算)']
combobox3=ttk.Combobox(frame,values=option3,width=20,state='readonly',)
combobox3.bind("<<ComboboxSelected>>", combo_select)

#チーム情報を選択したときのラベル
label=tk.Label(frame,text='表示したい項目を選択してください')
#label2 = tk.Label(frame)

#コンボボックスとラベルを表示
label.pack()
combobox.pack()


#メニューバーを表示
menubar = tk.Menu(menu_frame)
root.config(menu = menubar)
filemenu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label='メニュー', menu=filemenu)
filemenu.add_command(label='最前面に固定', command=top_window)
filemenu.add_command(label='固定を解除', command=back_window)
filemenu.add_command(label='左上に移動', command=move_leftup)
filemenu.add_command(label='終了', command=close_window)

root.protocol("WM_DELETE_WINDOW", close_window)

root.mainloop()

