import time
import sys
import os
sys.path.insert(0, 'modules/')
import sqlite3

def get_platform():
    platforms = {
        'linux1' : 'Linux',
        'linux2' : 'Linux',
        'darwin' : 'OS X',
        'win32' : 'Windows'
    }
    if sys.platform not in platforms:
        return sys.platform
    
    return platforms[sys.platform]

platform = get_platform()

if platform == 'Windows':    
    from win10toast import ToastNotifier

elif platform == 'Linux':
    import notify2

elif platform == 'OS X':
    pass

else:
    print('Ваша платформа не піддержує сповіщення.')
    sys.exit()


def db_open():
    global conn
    conn = sqlite3.connect(f"data/days.db")
    #conn.row_factory = sqlite3.Row
    global cursor
    cursor = conn.cursor()

db_open()

def db_close():
    cursor.close()
    conn.close()

def db_update():
    cursor.execute('SELECT * FROM task')
    task_list_unsorted = cursor.fetchall() #ДБ видає дані у виді (,). Цикл перетворює їх у список [,]
    task_list = []
    for task in task_list_unsorted:
        task_list.append(list(task))
    return task_list

def task_time():
    task_flag = []
    task_list = db_update()
    for task in task_list:
        task.append(True)
        task_flag.append(task)
    return task_list, task_flag

def change_platform_message(task):
    message = f'Невиконане завдання: {task}'
    if platform == 'Windows':
        show_message_windows(message)
    elif platform == 'Linux':
        show_message_linux(message)
    elif platform == 'OS X':
        show_message_osx(message)

def show_message_windows(message):
    toaster = ToastNotifier()
    toaster.show_toast("Planner", message, duration=10)

def show_message_linux(message):
    notify2.init('Planner')
    n = notify2.Notification(message, icon = 'images/icon/icon.png')

def show_message_osx(message,title=None,subtitle=None,soundname=None):
    titlePart = 'Planner'
    if(not title is None):
        titlePart = 'with title "{0}"'.format(title)
    subtitlePart = message
    if(not subtitle is None):
        subtitlePart = 'subtitle "{0}"'.format(subtitle)
    soundnamePart = ''
    if(not soundname is None):
        soundnamePart = 'sound name "{0}"'.format(soundname)

    appleScriptNotification = 'display notification "{0}" {1} {2} {3}'.format(message,titlePart,subtitlePart,soundnamePart)
    os.system("osascript -e '{0}'".format(appleScriptNotification))


while True: 
    task_list, task_flag = task_time()
    if len(task_list) > 0:
        time_task = f'PyQt5.QtCore.QTime({time.strftime("%H, %M")})'
        for i, task in enumerate(task_list):
            if time_task == task[2] and task[0] == 0: #task[0] - стан задачі (виконана/не виконана)
                if len(task_flag[i]) == 6:
                    if task_flag[i][5]:
                        change_platform_message(task[1])
                        task_flag[i][5] = False
                else:
                    change_platform_message(task[1])
                    task_flag[i].append(False)

    
    time.sleep(1)