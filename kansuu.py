import requests
from bs4 import BeautifulSoup
import tkinter as tk
import tkinter.ttk as ttk
import urllib
import webbrowser
import matplotlib.pyplot as plt
from mplsoccer.pitch import Pitch
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import scrolledtext as st
import japanize_matplotlib

def attend_graph(div,frame2,startyear):
    #global canvas2
    #global canvas_widget2
    for widget in frame2.winfo_children():
        widget.destroy()

    news_url = f'https://data.j-league.or.jp/SFTD12/search?competitionFrameName=Ｊ２リーグ&teamFlag=1&page=&startCompetitionYear={startyear}&endCompetitionYear=2024&competitionFrame={div}'
    news_html = requests.get(news_url)
    soup = BeautifulSoup(news_html.text, 'html.parser')

    table_over_boxes = soup.find_all(class_="table-over-box")

    team_name_list = []
    attendance_list = []

    for table_over_box in table_over_boxes:
        rows = table_over_box.find_all('tr')
        for row in rows:
            for name in row.find_all('th',class_='name'):
                team_name_list.append(name.text)
            th_list = row.find_all('th')     
            if len(th_list) == 5:
                attendance_tag = th_list[4]
                attendance = attendance_tag.text.replace(',','')
                attendance_list.append(attendance)

    attendance_list_int = [int(attendance)for attendance in attendance_list]
    team_attendance_dict = dict(zip(team_name_list, attendance_list_int))
    last_key, last_value = team_attendance_dict.popitem()
    team_attendance_dict = dict(sorted(team_attendance_dict.items(), key=lambda x: x[1],reverse=True))
    
    fig = Figure(figsize = (10,6))
    ax = fig.add_subplot(111)
    ax.bar(team_attendance_dict.keys() ,team_attendance_dict.values())
    ax.set_ylim(0,60000)
    ax.tick_params(axis = 'x',rotation=90,labelsize=7)
    ax.tick_params(axis = 'y',labelsize=7)
    canvas2 = FigureCanvasTkAgg(fig, master=frame2)
    canvas_widget2 = canvas2.get_tk_widget()
    #canvas_widget2.draw()
    canvas_widget2.pack()


def time_score(div,frame2,startyear):

    for widget in frame2.winfo_children():
        widget.destroy()

    time_score_url = f'https://data.j-league.or.jp/SFTD06/search?selectFlag=3&competitionFrameId={div}&startYear={startyear}&endYear=2024&point=1'
    time_score_html = requests.get(time_score_url)
    soup = BeautifulSoup(time_score_html.text, 'html.parser')

    table = soup.find('table', class_='table-base00 search-table')
    rows = table.find_all('tr')

    total_values = [0] * 6

    for row in rows:
        cells = row.find_all('td')

        for i, cell in enumerate(cells[3:9]):  # 2番目の列から処理を開始します（最初の2列はチー失点ム名とリンクなので除外します）
            text = cell.get_text(strip=True).split('(')[0]  # (数字)を除外してテキストを取得
            if text:  # テキストが空でない場合のみ処理を行う
                value = int(text)
            else:
                value = 0  # テキストが空の場合はゼロとして扱う

            total_values[i] += value

    times_list=['1-15分', '16-30分', '31-45分', '46-60分', '61-75分', '76-90分']
    times_goal_dict = dict(zip(times_list,total_values))
    fig = Figure(figsize = (6,6))
    ax = fig.add_subplot(111)
    ax.pie(times_goal_dict.values() ,labels=times_goal_dict.keys(), autopct='%.2f%%',startangle=90,counterclock=False)
    canvas2 = FigureCanvasTkAgg(fig, master=frame2)
    canvas_widget2 = canvas2.get_tk_widget()
    canvas_widget2.pack()
    
