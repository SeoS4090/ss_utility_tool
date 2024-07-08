from win10toast import *
import Constant

def Show_Toast(title = 'test', msg = 'test message', icon_path = f'{Constant.RESOURCE_PATH}ico_icon.ico', duration = 3, threaded = False):
    toaster = ToastNotifier()
    #toaster.show_toast(title,msg,f'{Constant.RESOURCE_PATH}ico_icon.ico')
    toaster.show_toast(title,msg,icon_path,duration,threaded)

Show_Toast()