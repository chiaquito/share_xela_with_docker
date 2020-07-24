import platform
import os


OS = ""
OS_TYPE = ["OSX", "LINUX"]




def getTypeOS():
    """
    'python manage.py runserver' コマンド実行時のOSを判定する。

    returns:
        str: OSXまたはLINUXの文字列
    """

    pf = platform.system()

    if pf == 'Darwin':
        print("OSXの環境 -> 開発環境")
        OS = OS_TYPE[0]
        return OS

    if pf == 'Linux':
        print("LINUXの環境 -> 製品環境")
        OS = OS_TYPE[1]
        return OS
    


def setDjangoSettingsModule(OS):
    """
    OS(開発環境、製品環境)によって、 'DJANGO_SETTINGS_MODULE' を定める。
    これにより、 python manage.py runserver --settings DJANG0_SETTINGS_MODULE=config.settings.dev_settings
    と入力する必要がなくなる。
    単に python manage.py runserver コマンドを実行すれば良い
    """

    if OS == OS_TYPE[0]:
        return os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev_settings')

    if OS == OS_TYPE[1]:
        return os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.prod_settings')



def setDSM():
    OS = getTypeOS()
    return setDjangoSettingsModule(OS)



    