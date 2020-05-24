import sys
import os
import subprocess

sys.path.insert(0, 'modules/')
import sqlite3

from PyQt5.QtCore import (QTime, pyqtSignal, QSize, QRect)
from PyQt5.QtWidgets import (QWidget, QPushButton, QFrame, QLabel, QLineEdit, QTimeEdit, QApplication, QAbstractSpinBox, QVBoxLayout, QSizePolicy, QFontDialog, QPlainTextEdit)
from PyQt5.QtGui import (QIcon, QImage, QPalette, QBrush)

def db_open():
    conn = sqlite3.connect(f"data/days.db")
    #conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    return conn, cursor

def db_close(conn, cursor):
    conn.commit()
    cursor.close()
    conn.close()
 

class main(QWidget):
    #Problem Widgets
    widgets = []
    info = []
    lines_tasks = []

    windowClosed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.initUI()
 
    def initUI(self):
        #Buttons
        self.btn_add = QPushButton('', self)
        self.btn_add.setGeometry(5, 5, 50, 50)
        self.btn_add.setIcon(QIcon('images/background/BtnAdd1.png'))
        self.btn_add.setIconSize(QSize(50, 50))
        self.btn_add.setStyleSheet("border-style: solid;")
        self.btn_add.clicked.connect(self.add_tasks)
 
        self.btn_all_del = QPushButton('', self)
        self.btn_all_del.setGeometry(900, 5, 100, 50)
        self.btn_all_del.setIcon(QIcon('images/background/BtnADel.png'))
        self.btn_all_del.setIconSize(QSize(100, 50))
        self.btn_all_del.clicked.connect(self.del_all_tasks)
        self.btn_all_del.setStyleSheet("border-style: solid;")

        #Line
        self.line_h = QFrame(self)
        self.line_h.setGeometry(QRect(0, 60, 1000, 4))
        self.line_h.setFrameShape(QFrame.HLine)
        self.line_h.setFrameShadow(QFrame.Sunken)
        self.line_h.setObjectName("Hline1")

        self.create_lines()

        #more info widget
        self.info_widget = QWidget()
        self.info_widget.setGeometry(625, 300, 750, 500)
        self.info_widget.setFixedSize(750, 500)
        self.info_widget.setWindowTitle('Додаткова інформація')
        self.info_widget.setWindowIcon(QIcon('images/icon/icon.png'))
        oImage = QImage("images/background/back1.png")
        info_widget_palette = QPalette()
        info_widget_palette.setBrush(QPalette.Window, QBrush(oImage)) 
        self.info_widget.setPalette(info_widget_palette)

        self.btn_edit_ok = QPushButton('Ок', self.info_widget)
        self.btn_edit_ok.setGeometry(675, 465, 70, 30)
        self.btn_edit_ok.clicked.connect(self.btn_edit_ok_clicked)

        self.btn_edit_cancel = QPushButton('Відмінити', self.info_widget)
        self.btn_edit_cancel.setGeometry(600, 465, 70, 30)
        self.btn_edit_cancel.clicked.connect(self.btn_edit_cancel_clicked)

        self.note_edit = QLineEdit(self.info_widget)
        self.note_edit.setGeometry(0, 0, 750, 35)
        self.note_edit.setStyleSheet('border-style: solid; font-size: 15px;')
        self.note_edit.setPlaceholderText('Введіть текст на замітку...')

        self.text_edit = QPlainTextEdit(self.info_widget)
        self.text_edit.setGeometry(0, 35, 750, 427)
        self.text_edit.setStyleSheet('border-style: solid; font-size: 15px;')
        self.text_edit.setPlaceholderText('Введіть додаткову інофрмацію...')

        self.text_edit_line1 = QFrame(self.info_widget)
        self.text_edit_line1.setGeometry(QRect(0, 34, 750, 3))
        self.text_edit_line1.setFrameShape(QFrame.HLine)
        self.text_edit_line1.setFrameShadow(QFrame.Sunken)
        self.text_edit_line1.setObjectName(f"text_edit_line1")

        self.text_edit_line2 = QFrame(self.info_widget)
        self.text_edit_line2.setGeometry(QRect(0, 462, 750, 3))
        self.text_edit_line2.setFrameShape(QFrame.HLine)
        self.text_edit_line2.setFrameShadow(QFrame.Sunken)
        self.text_edit_line2.setObjectName(f"text_edit_line2")

        #Window
        self.setGeometry(500, 150, 1000, 763)
        self.setFixedSize(1000, 763)
        self.setWindowTitle('Planner')
        self.setWindowIcon(QIcon('images/icon/icon.png'))
        #self.setStyleSheet("background-color: white;")
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(oImage))                        
        self.setPalette(palette)
 
        self.show()

        #load tasks with database
        self.load_tasks()

    
    ######################################## Problem defs #############################################
    def show_tasks(self):
        main.widgets[0][1].setGeometry(0, 61, 70, 72)
        main.widgets[0][2].setGeometry(0, 61, 70, 72)
        main.widgets[0][3].setGeometry(69, 61, 650, 72)
        main.widgets[0][4].setGeometry(730, 61, 50, 71)
        main.widgets[0][5].setGeometry(800, 62, 80, 70)
        main.widgets[0][6].setGeometry(900, 61, 50, 71)
        main.widgets[0][7].setGeometry(950, 61, 50, 71)
        for num, widgets in enumerate(main.widgets[1:]):
            widgets[1].setGeometry(0, 62+70*(num+1), 70, 71)
            widgets[2].setGeometry(0, 62+70*(num+1), 70, 71)
            widgets[3].setGeometry(69, 62+70*(num+1), 650, 71)
            widgets[4].setGeometry(730, 62+70*(num+1), 50, 71)
            widgets[5].setGeometry(800, 63+70*(num+1), 80, 69)
            widgets[6].setGeometry(900, 62+70*(num+1), 50, 71)
            widgets[7].setGeometry(950, 62+70*(num+1), 50, 71)

        for i, widgets in enumerate(main.widgets):
            for widget in widgets[1:]:
                widget.setVisible(True)
            if widgets[0]:
                widgets[2].setVisible(False)
            if main.info[i][0] != '' or main.info[i][1] != '':
                main.widgets[i][4].setIcon(QIcon('images/background/infoActive.png'))

        for line in main.lines_tasks[:len(main.widgets)]:
            line.setVisible(True)

    def hide_tasks(self):
        for widgets in main.widgets:
            for widget in widgets[1:]: #widgets[0] = flag (bool)
                widget.hide()

        for line in main.lines_tasks:
            line.setVisible(False)

    def del_all_tasks(self):
        self.hide_tasks()
        for widgets in main.widgets:
            for widget in widgets[1:]:
                widget.setParent(None)
        main.widgets.clear()
        main.info.clear()
        self.save_tasks()

    def del_task(self):
        self.hide_tasks()
        target = self.sender()
        for i, widgets in enumerate(main.widgets):
            if target in widgets:
                for elem in widgets[1:]:
                    elem.setParent(None)
                main.widgets.remove(widgets)
                del main.info[i]
        if len(main.widgets) > 0:
            self.show_tasks()
        self.save_tasks()
        
    def add_tasks(self):
        if len(main.widgets) < 10:

            self.checkBtnActive = QPushButton('', self)
            self.checkBtnActive.setVisible(False)
            self.checkBtnActive.setIcon(QIcon('images/background/BtnActive.png'))
            self.checkBtnActive.setIconSize(QSize(60, 50))
            self.checkBtnActive.setStyleSheet("border-style: solid;")
            self.checkBtnActive.clicked.connect(self.set_passive)

            self.checkBtnPassive = QPushButton('', self)
            self.checkBtnPassive.setIcon(QIcon('images/background/BtnPassive.png'))
            self.checkBtnPassive.setIconSize(QSize(60, 50))
            self.checkBtnPassive.setStyleSheet("border-style: bashed;")
            self.checkBtnPassive.clicked.connect(self.set_active)

            self.lineEditP = QLineEdit(self)
            self.lineEditP.setEnabled(False)
            self.lineEditP.setPlaceholderText("Нажміть кнопку для редагування...")
            self.lineEditP.setStyleSheet("font-size: 20px; background-color: rgba(0, 0, 0, 0); border-style: solid;")

            self.TimeEdit = QTimeEdit(self)
            self.TimeEdit.setEnabled(False)
            self.TimeEdit.setButtonSymbols(QAbstractSpinBox.NoButtons)
            self.TimeEdit.setStyleSheet("border-style: solid; font-size: 20px;")
            
            self.btnPEdit = QPushButton('', self)
            self.btnPEdit.setIcon(QIcon('images/background/BtnEdit.png'))
            self.btnPEdit.setIconSize(QSize(50, 50))
            self.btnPEdit.clicked.connect(self.edit)
            self.btnPEdit.setStyleSheet("border-style: solid;")

            self.btnDelTask = QPushButton('', self)
            self.btnDelTask.setIcon(QIcon('images/background/BtnDel.png'))
            self.btnDelTask.setIconSize(QSize(50, 50))
            self.btnDelTask.setStyleSheet("border-style: solid;")
            self.btnDelTask.clicked.connect(self.del_task)

            self.btn_info = QPushButton('', self)
            self.btn_info.setIcon(QIcon('images/background/info.png'))
            self.btn_info.setIconSize(QSize(50, 50))
            self.btn_info.setStyleSheet("border-style: solid;")
            self.btn_info.clicked.connect(self.show_info_widget)

            self.note_text = ''
            self.info_text = ''

            flag = 0

            main.widgets.append([flag, self.checkBtnActive, self.checkBtnPassive, self.lineEditP, self.btn_info, self.TimeEdit, self.btnPEdit, self.btnDelTask])
            main.info.append([self.note_text, self.info_text])

            self.hide_tasks()
            self.show_tasks()

    def add_tasks_database(self):
        for task_info in self.task_info_list:
            self.checkBtnActive = QPushButton('', self)
            self.checkBtnActive.setVisible(False)
            self.checkBtnActive.setIcon(QIcon('images/background/BtnActive.png'))
            self.checkBtnActive.setIconSize(QSize(60, 50))
            self.checkBtnActive.setStyleSheet("border-style: solid;")
            self.checkBtnActive.clicked.connect(self.set_passive)

            self.checkBtnPassive = QPushButton('', self)
            self.checkBtnPassive.setIcon(QIcon('images/background/BtnPassive.png'))
            self.checkBtnPassive.setIconSize(QSize(60, 50))
            self.checkBtnPassive.setStyleSheet("border-style: bashed;")
            self.checkBtnPassive.clicked.connect(self.set_active)

            self.lineEditP = QLineEdit(self)
            self.lineEditP.setText(task_info[1])
            self.lineEditP.setEnabled(False)
            self.lineEditP.setPlaceholderText("Нажміть кнопку для редагування...")
            self.lineEditP.setStyleSheet("font-size: 20px; background-color: rgba(0, 0, 0, 0); border-style: solid;")

            self.TimeEdit = QTimeEdit(self)
            self.TimeEdit.setTime(QTime(int(task_info[2][19:-1].split(',')[0]), int(task_info[2][19:-1].split(',')[1])))
            self.TimeEdit.setEnabled(False)
            self.TimeEdit.setButtonSymbols(QAbstractSpinBox.NoButtons)
            self.TimeEdit.setStyleSheet("border-style: solid; font-size: 20px;")
                
            self.btnPEdit = QPushButton('', self)
            self.btnPEdit.setIcon(QIcon('images/background/BtnEdit.png'))
            self.btnPEdit.setIconSize(QSize(50, 50))
            self.btnPEdit.clicked.connect(self.edit)
            self.btnPEdit.setStyleSheet("border-style: solid;")

            self.btnDelTask = QPushButton('', self)
            self.btnDelTask.setIcon(QIcon('images/background/BtnDel.png'))
            self.btnDelTask.setIconSize(QSize(50, 50))
            self.btnDelTask.setStyleSheet("border-style: solid;")
            self.btnDelTask.clicked.connect(self.del_task)

            self.btn_info = QPushButton('', self)
            self.btn_info.setIcon(QIcon('images/background/info.png'))
            self.btn_info.setIconSize(QSize(50, 50))
            self.btn_info.setStyleSheet("border-style: solid;")
            self.btn_info.clicked.connect(self.show_info_widget)

            flag = 0

            main.widgets.append([flag, self.checkBtnActive, self.checkBtnPassive, self.lineEditP, self.btn_info, self.TimeEdit, self.btnPEdit, self.btnDelTask, self.btn_info])

            self.hide_tasks()
            self.show_tasks()

    def save_tasks(self):     
        conn, cursor = db_open()
        cursor.execute("""DELETE FROM task""")
        
        task_save_list = []

        for i, tasks in enumerate(main.widgets):
            if tasks[3].text() != '': 
                task_save_list.append([tasks[0], tasks[3].text(), str(tasks[5].time()), main.info[i][0], main.info[i][1]])

        cursor.executemany("""INSERT INTO task VALUES (?, ?, ?, ?, ?)""", task_save_list)
        db_close(conn, cursor)

    def update_one_task(self, task, target, element):
        conn, cursor = db_open()
        cursor.execute("""UPDATE task SET {0} = {1} WHERE text_task = '{2}'""".format(target, element, task[3].text()))
        db_close(conn, cursor)

    def load_tasks(self):
        conn, cursor = db_open()
        cursor.execute('SELECT * FROM task')
        tasks = cursor.fetchall()
        self.task_info_list = []
        self.info_text_db = []
        for task in tasks:
            self.task_info_list.append(task[:-2])
            main.info.append([task[-2], task[-1]])


        db_close(conn, cursor)
        self.add_tasks_database()


    ########################################## edit task ############################################
    def edit(self):
        target = self.sender()
        self.set_btn_enabled(flag=False)
        for widgets in main.widgets:
            if target in widgets:
                self.target_widgets = widgets

                self.edit_line = widgets[3]
                self.edit_line.setPlaceholderText('Введіть задачу та виставіть час...')
                self.old_text = self.edit_line.text()
                self.edit_time = widgets[5]
                self.old_time = self.edit_time.time()
                
                self.btn_ok = QPushButton('', self)
                self.btn_ok.setGeometry(450, 5, 50, 50)
                self.btn_ok.setIcon(QIcon('images/background/ok.png'))
                self.btn_ok.setIconSize(QSize(50, 50))
                self.btn_ok.setStyleSheet('border-style: solid;')
                
                self.btn_can = QPushButton('', self)
                self.btn_can.setGeometry(500, 5, 50, 50)
                self.btn_can.setIcon(QIcon('images/background/cancel.png'))
                self.btn_can.setIconSize(QSize(50, 50))
                self.btn_can.setStyleSheet('border-style: solid;')
                
                self.btn_ok.clicked.connect(self.edit_ok)
                self.btn_can.clicked.connect(self.edit_cancel)
                
                self.btn_ok.show()
                self.btn_can.show()
                
                self.edit_line.setEnabled(True)
                self.edit_time.setEnabled(True)

    def edit_ok(self):
        self.edit_line.setEnabled(False)
        self.edit_line.setPlaceholderText('Нажміть кнопку для редагування...')
        self.edit_time.setEnabled(False)
        self.delete_edit_buttons()
        self.set_btn_enabled(flag=True)
        self.save_tasks()

    def edit_cancel(self):
        self.edit_line.setText(self.old_text)
        self.edit_line.setPlaceholderText('Нажміть кнопку для редагування...')
        self.edit_line.setEnabled(False)
        self.edit_time.setTime(self.old_time)
        self.edit_time.setEnabled(False)
        self.delete_edit_buttons()
        self.set_btn_enabled(flag=True)
        
        
    def delete_edit_buttons(self):
        self.btn_ok.deleteLater()
        self.btn_can.deleteLater()
        self.btn_ok.setParent(None)
        self.btn_can.setParent(None)

    def set_btn_enabled(self, flag):
        self.btn_add.setEnabled(flag)
        self.btn_all_del.setEnabled(flag)
        for widgets in main.widgets:
            widgets[1].setEnabled(flag)
            widgets[2].setEnabled(flag)
            widgets[6].setEnabled(flag)
            widgets[7].setEnabled(flag)

    ############################################## set active/passive check button ########################################################

    def set_active(self):
        button = self.sender()
        for widgets in main.widgets:
            if button in widgets:
                button.setVisible(False)
                widgets[1].setVisible(True)
                widgets[0] = 1
                self.update_one_task(task=widgets, target='check_task', element='1')

    def set_passive(self):
        button = self.sender()
        for widgets in main.widgets:
            if button in widgets:
                button.setVisible(False)
                widgets[2].setVisible(True)
                widgets[0] = 0
                self.update_one_task(task=widgets, target='check_task', element='0')   

    ############################################## info widget ###########################################################################
    def show_info_widget(self):
        target = self.sender()
        for i, widgets in enumerate(main.widgets):
            if target in widgets:
                self.note_text = main.info[i][0]
                self.info_text = main.info[i][1]
                self.i = i

        self.note_edit.setText(self.note_text)

        self.text_edit.setPlainText(self.info_text)

        self.info_widget.show()

    def btn_edit_ok_clicked(self):
        self.info_widget.hide()
        self.btn_info.setToolTip(f'<b>{self.note_edit.text()}</b>')

        main.info[self.i][0] = self.note_edit.text()
        main.info[self.i][1] = self.text_edit.toPlainText()

        self.info_change_icon()
        self.save_tasks()

    def btn_edit_cancel_clicked(self):
        self.info_widget.hide()

        self.info_change_icon()
        self.save_tasks()


    def info_change_icon(self):
        if main.info[self.i][0] != '' or main.info[self.i][1] != '':
            main.widgets[self.i][4].hide()
            main.widgets[self.i][4].setIcon(QIcon('images/background/infoActive.png'))
            main.widgets[self.i][4].show()
        else:
            main.widgets[self.i][4].hide()
            main.widgets[self.i][4].setIcon(QIcon('images/background/info.png'))
            main.widgets[self.i][4].show()
        

    ###############################################################################################
    def create_lines(self):
        for num in range(15):
            self.task_line = QFrame(self)
            self.task_line.setGeometry(QRect(0, 130+70*(num), 1000, 6))
            self.task_line.setFrameShape(QFrame.HLine)
            self.task_line.setFrameShadow(QFrame.Sunken)
            self.task_line.setObjectName(f"task_line{num+1}")
            self.task_line.setVisible(False)
            main.lines_tasks.append(self.task_line)

    def closeEvent(self, *args, **kwargs):
        super().closeEvent(*args, **kwargs)

        self.windowClosed.emit()

def kill_cron():
    cron.kill()
    

cron = subprocess.Popen(['python.exe', 'cron.py'])
app = QApplication(sys.argv)
main = main()
main.windowClosed.connect(kill_cron)
n = sys.exit(app.exec_())
