import sys
import os
import urllib.request
import json
import webbrowser

import threading
import pickle
from datetime import date, datetime
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QStandardItem
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtGui
from PyQt5 import uic
import time


form_class = uic.loadUiType("naver_browser.ui")[0]

class NvApp(QMainWindow, form_class):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()

        self.client_id = "oKNRMLOlufvmy01grzMe"
        self.client_secret = "DEF5k96DfV"

        self.thread_renew_seconds()
        self.stackedWidget.setCurrentIndex(0)
        self.btn_search.clicked.connect(lambda: self.Nv_search(1, self.client_id, self.client_secret))
        self.search_bar.returnPressed.connect(lambda: self.Nv_search(1, self.client_id, self.client_secret))
        self.btn_search_2.clicked.connect(lambda: self.Nv_search(2, self.client_id, self.client_secret))
        self.search_bar_2.returnPressed.connect(lambda: self.Nv_search(2, self.client_id, self.client_secret))
        self.btn_naver.clicked.connect(lambda: webbrowser.open('http://www.naver.com'))
        self.btn_user_opinion.clicked.connect(lambda: webbrowser.open('https://forum.whale.naver.com/'))
        self.btn_news.clicked.connect(lambda: self.show_sw(0))
        self.btn_blog.clicked.connect(lambda: self.show_sw(1))
        self.btn_shop.clicked.connect(lambda: self.show_sw(2))
        self.btn_cafe.clicked.connect(lambda: self.show_sw(3))
        self.btn_image.clicked.connect(lambda: self.show_sw(4))
        self.btn_webdoc.clicked.connect(lambda: self.show_sw(5))
        self.btn_kin.clicked.connect(lambda: self.show_sw(6))
        self.btn_next_search.clicked.connect(lambda: self.search_more(10))

    def thread_renew_seconds(self):
        week = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"]
        now = datetime.now()
        self.label_5.setText("{}".format(str(now.second).zfill(2)))
        self.label_3.setText("{}:{}".format(str(now.hour).zfill(2), str(now.minute).zfill(2)))
        self.label_2.setText("{}      {}".format(date.today().isoformat(), week[now.weekday()]))
        threading.Timer(1, self.thread_renew_seconds).start()

    def show_sw(self, index):
        self.stackedWidget_2.setCurrentIndex(index)

    def search_more(self, display):
        search_word = self.search_word_final
        self.last_start = self.last_start + display
        self.Nv_search_2(search_word, self.client_id, self.client_secret, self.last_start, display)

    def Nv_search(self, search_bar, client_id, client_secret):
        layouts = [self.news_layout, self.blog_layout, self.shop_layout,
                   self.cafe_layout, self.image_layout, self.webdoc_layout,
                   self.kin_layout]
        for layout in layouts:
            for i in reversed(range(layout.count())):
                layout.itemAt(i).widget().deleteLater()
        if search_bar == 1:
            search_word = self.search_bar.text()
            self.search_bar_2.setText(search_word)
        elif search_bar == 2:
            search_word = self.search_bar_2.text()
        self.search_word_final = search_word

        start = 1
        self.last_start = start
        display = 10
        self.Nv_search_2(search_word, client_id, client_secret, start, display)

    def Nv_search_2(self, search_word, client_id, client_secret, start, display):
        encText = urllib.parse.quote(search_word)
        nodes = ["news", "blog", "shop", "cafearticle", "image", "webkr", "kin"]
        totals = []
        for node in nodes:
            parameters = "&start=%s&display=%s" % (start, display)
            url = "https://openapi.naver.com/v1/search/%s.json?query=" % node + encText + parameters

            request = urllib.request.Request(url)
            request.add_header("X-Naver-Client-Id", client_id)
            request.add_header("X-Naver-Client-Secret", client_secret)
            response = urllib.request.urlopen(request)
            rescode = response.getcode()

            if rescode == 200:
                response_body = response.read()
                results = json.loads(response_body.decode('utf-8'))
                # print(results["items"])

                totals.append(results['total'])
                # print("total", totals)

                post_cnt = 1
                for post in results["items"]:
                    # print(post.keys())
                    # print(post.values())
                    values = list(post.values())

                    if node == 'news':
                        texts = [values[0], values[3], values[4]]
                        links = post['link']
                        new_post = self.create_search_frame(post_cnt, 600, 100, links, texts)
                        post_cnt += 1
                        self.stackedWidget.setCurrentIndex(1)
                        self.news_layout.addWidget(new_post)
                    elif node == 'blog':
                        texts = [values[0], values[2], values[5]]
                        links = post['link']
                        new_post = self.create_search_frame(post_cnt, 600, 100, links, texts)
                        post_cnt += 1
                        self.stackedWidget.setCurrentIndex(1)
                        self.blog_layout.addWidget(new_post)
                    elif node == 'shop':
                        texts = [values[0], values[5], values[8]]
                        links = post['link']
                        new_post = self.create_search_frame(post_cnt, 600, 100, links, texts)
                        post_cnt += 1
                        self.stackedWidget.setCurrentIndex(1)
                        self.shop_layout.addWidget(new_post)
                    elif node == 'cafearticle':
                        texts = [values[0], values[3], values[2]]
                        links = post['link']
                        new_post = self.create_search_frame(post_cnt, 600, 100, links, texts)
                        post_cnt += 1
                        self.stackedWidget.setCurrentIndex(1)
                        self.cafe_layout.addWidget(new_post)
                    elif node == 'image':
                        links = post['link']
                        new_post = self.create_image_frame(post_cnt, 200, 220, links, post['thumbnail'], post['title'])
                        post_cnt += 1
                        self.stackedWidget.setCurrentIndex(1)
                        self.image_layout.addWidget(new_post)
                    elif node == 'webkr':
                        texts = [values[0], values[2], values[1]]
                        links = post['link']
                        new_post = self.create_search_frame(post_cnt, 600, 100, links, texts)
                        post_cnt += 1
                        self.stackedWidget.setCurrentIndex(1)
                        self.webdoc_layout.addWidget(new_post)
                    elif node == 'kin':
                        texts = [values[0], values[2], values[1]]
                        links = post['link']
                        new_post = self.create_search_frame(post_cnt, 600, 100, links, texts)
                        post_cnt += 1
                        self.stackedWidget.setCurrentIndex(1)
                        self.kin_layout.addWidget(new_post)

        print(totals)
        self.search_result_indicator.setText('"{}"로 검색한 결과입니다.'
                                             '\n총 검색결과 : \n[뉴스] {}건, [블로그] {}건, '
                                             '[쇼핑] {}건, [카페] {}건, [이미지] {}건,'
                                             '[웹문서] {}건, [지식인] {}건'.format(self.search_word_final,
                                                                              totals[0], totals[1], totals[2],
                                                                              totals[3], totals[4], totals[5], totals[6]))
    def initUI(self):
        self.setWindowTitle('NAVER SEARCH')
        self.resize(1000, 850)
        self.center()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def create_label(self, links, texts, label_no, minW, minH, maxW, maxH):
        align = Qt.AlignLeft
        labels = []
        count = 0
        for i in range(label_no):
            globals()['label_search_{}'.format(i)] = QLabel('<a href="{}">{}</a>'.format(links, texts[count]))
            globals()['label_search_{}'.format(i)].setOpenExternalLinks(True)
            labels.append(globals()['label_search_{}'.format(i)])
            count += 1
        for i in range(len(labels)):
            labels[i].setMinimumSize(minW, minH)
            labels[i].setMaximumSize(maxW, maxH)
            if i == 0:
                labels[i].setAlignment(Qt.AlignLeft)
            else:
                labels[i].setAlignment(align)
        return labels

    def create_image_label(self, links, title):
        image_labels = []
        for i in range(1):
            globals()['label_image_{}'.format(i)] = QLabel('<a href="{}">{}</a>'.format(links, title))
            globals()['label_image_{}'.format(i)].setOpenExternalLinks(True)
            globals()['label_image_{}'.format(i)].setMinimumSize(180, 25)
            globals()['label_image_{}'.format(i)].setMaximumSize(600, 25)
            globals()['label_image_{}'.format(i)].setFont(QtGui.QFont("나눔스퀘어_ac", 13))
            globals()['label_image_{}'.format(i)].setStyleSheet("QLabel{color: rgb(0,0,0); border: none;}")
            image_labels.append(globals()['label_image_{}'.format(i)])
        return image_labels

    def create_image_label_2(self, thumbnail):
        images = []
        for i in range(1):
            image = urllib.request.urlopen(thumbnail).read()
            pixmap = QPixmap()
            pixmap.scaledToHeight(180)
            pixmap.loadFromData(image)
            globals()['image_search_{}'.format(i)] = QLabel()
            globals()['image_search_{}'.format(i)].setPixmap(pixmap)
            images.append(globals()['image_search_{}'.format(i)])
        return images

    def create_image_frame(self, frame_no, width, height, links, thumbnail, title):
        layout = QGridLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        image_labels = self.create_image_label(links, title)
        image_labels_2 = self.create_image_label_2(thumbnail)

        layout.addWidget(image_labels[0], 0, 1)
        layout.addWidget(image_labels_2[0], 0, 0)

        frames = []
        globals()['frame_{}'.format(frame_no)] = QFrame(self)
        frames.append(globals()['frame_{}'.format(frame_no)])
        frames[0].resize(width, height)
        frames[0].setMinimumSize(180, 205)
        frames[0].setMaximumSize(1920, height)
        frames[0].setContentsMargins(0, 0, 0, 0)
        frames[0].setLayout(layout)
        frames[0].setStyleSheet("QFrame{background-color: rgb(255,255,255); border: none;}")
        return frames[0]

    def create_search_frame(self, frame_no, width, height, links, texts):
        labels = self.create_label(links, texts, 3, 500, 30, 1920, 1600)
        labels[0].setFont(QtGui.QFont("나눔스퀘어_ac Light", 13, QtGui.QFont.Bold))
        labels[1].setFont(QtGui.QFont("나눔스퀘어_ac", 11))
        labels[2].setFont(QtGui.QFont("나눔스퀘어_ac", 9))

        layout = QVBoxLayout()
        layout.setSpacing(2)
        layout.setContentsMargins(5,5,0,5)

        layout.addWidget(labels[0])
        layout.addWidget(labels[1])
        layout.addWidget(labels[2])

        frames = []
        globals()['frame_{}'.format(frame_no)] = QFrame(self)
        frames.append(globals()['frame_{}'.format(frame_no)])
        frames[0].resize(width, height)
        frames[0].setMinimumSize(width, height)
        frames[0].setMaximumSize(1920, height)
        frames[0].setLayout(layout)
        frames[0].setContentsMargins(0, 0, 0, 0)
        frames[0].setStyleSheet("QFrame{background-color: rgb(255,255,255); border: none;}")
        return frames[0]

if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = NvApp()
    form.show()
    exit(app.exec_())