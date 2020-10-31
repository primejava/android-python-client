# coding=utf-8
import threading
import datetime
from android_keycodes import AndroidKeyCodes
from pynput import keyboard, mouse
from pynput.mouse import Button
from ctypes import *
GetForegroundWindow = windll.user32.GetForegroundWindow
GetWindowText = windll.user32.GetWindowTextA

title_win="控制台"

# 鼠标动作监听
class MouseActionListener(threading.Thread):
    def __init__(self, _videoBox):
        super().__init__()
        self.videoBox = _videoBox

    def leftBtnClick(self,_client,screen,pressed, x, y):
        type = 2
        buttons = 17
        action = 1
        if(pressed):
            screen.setFocus(True)
            action = 0
        content=_client.record.bytes_content(method="leftBtnClick", type=type, buttons=buttons, action=action, x=x, y=y, screenWidth=_client.decoder.frame_width, screenHeight=_client.decoder.frame_height)
        _client.decoder.send_data(content)

    def rightBtnClick(self,_client,pressed, x, y):
        if(pressed):
            type = 4
            action = 0
            content = _client.record.bytes_content(method="rightBtnClick", type=type, action=action)
            _client.decoder.send_data(content)
        else:
            type = 2
            action = 1
            buttons = 26
            content = _client.record.bytes_content(method="rightBtnClick", type=type, action=action, buttons=buttons, x=x, y=y, screenWidth=_client.decoder.frame_width, screenHeight=_client.decoder.frame_height)
            _client.decoder.send_data(content)

    def middleBtnScroll(self,_client,x, y, hScroll, vScroll):
        type = 3
        content = _client.record.bytes_content(method="middleBtnScroll", type=type, x=x, y=y,  screenWidth=_client.decoder.frame_width, screenHeight=_client.decoder.frame_height,hScroll=hScroll, vScroll=vScroll)
        _client.decoder.send_data(content)

    def drag(self,_client,x,y):
        type = 2
        buttons = 17
        action = 2
        content = _client.record.bytes_content(method="drag", type=type, action=action, buttons=buttons, x=x, y=y,  screenWidth=_client.decoder.frame_width, screenHeight=_client.decoder.frame_height)
        _client.decoder.send_data(content)

    def run(self):
        self.starttime = datetime.datetime.now()
        self.ispressd=False
        # 鼠标移动事件
        def on_move(x, y):
            if(not self.ispressd):
                return
            nowtime= datetime.datetime.now()
            if((nowtime - self.starttime).microseconds>10*1000):
                self.starttime = nowtime
                win_hd = GetForegroundWindow()
                if (getWinTitle(win_hd) == title_win):
                    client, pos,_ = getPosInPhoneScreen(self.videoBox, x, y)
                    if client and client.is_runing():
                        (x, y) = pos
                        self.drag(client,x, y)
        # 鼠标点击事件
        def on_click(x, y, button, pressed):
            win_hd = GetForegroundWindow()
            if(getWinTitle(win_hd)==title_win):
                client, pos,screen= getPosInPhoneScreen(self.videoBox, x, y)
                if client and client.is_runing():
                    (x,y)=pos
                    if(button==Button.left):
                        self.ispressd=pressed
                        self.leftBtnClick(client,screen,pressed, x, y)
                    elif(button==Button.right):
                        self.rightBtnClick(client,pressed, x, y)
        # 鼠标滚动事件
        def on_scroll(x, y, x_axis, y_axis):
            win_hd = GetForegroundWindow()
            if (getWinTitle(win_hd) == title_win):
                client,pos,_ = getPosInPhoneScreen(self.videoBox, x, y)
                if client and client.is_runing():
                    (x, y)=pos
                    self.middleBtnScroll(client,x, y, x_axis, y_axis)

        with mouse.Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll) as mouseListener:
            mouseListener.join()


# 键盘动作监听
class KeyboardActionListener(threading.Thread):
    def __init__(self,_videoBox):
        super().__init__()
        self.videoBox=_videoBox

    def get_key_name(self,key):
        if (isinstance(key, keyboard.KeyCode)):
            if key.char:
                return key.char
            else:
                return str(key)
        else:
            return str(key)
    #常规按键
    def keycodeClick(self,_client,keycode,isPress=True):
        if _client is None:
            return
        if not _client.is_runing():
            return
        type = 0
        metaState = 2097152
        action = 1
        if(isPress):
            action = 0
        content = _client.record.bytes_content(method="keycodeClick", type=type, action=action, keycode=keycode, metaState=metaState)
        _client.decoder.send_data(content)
    #标点符号等按键
    def textClick(self,_client,text):
        if _client is None:
            return
        if not _client.is_runing():
            return
        type = 1
        content = _client.record.bytes_content(method="textClick", type=type,text=text)
        _client.decoder.send_data(content)
    #关闭手机屏幕
    def toggleScreenPower(self,_client):
        if _client is None:
            return
        if not _client.is_runing():
            return
        type = 5
        # 0是关闭1是打开
        action=0
        content = _client.record.bytes_content(method="toggleScreenPower", type=type, action=action)
        _client.decoder.send_data(content)

    def run(self):
            # 键盘按下监听
            def on_press(key):
                if key == keyboard.Key.tab:
                    idx=-1
                    length=len(self.videoBox.pictureLabels)
                    if length==0:
                        return True
                    for i,screen in enumerate(self.videoBox.pictureLabels):
                        if screen.hasFocus():
                            idx=i
                            break
                    self.videoBox.pictureLabels[(idx+1)%length].setFocus(True)
                    return True
                _,client=self.videoBox.current_screen(True)
                if client:
                    name = self.get_key_name(key)
                    type,keycode = AndroidKeyCodes.getKeycode(name)
                    if type==0:
                        self.keycodeClick(client,keycode)
                    if type == 1:
                        self.textClick(client,keycode)
            # 键盘抬起监听
            def on_release(key):
                 pass
            # 键盘监听
            with keyboard.Listener(on_press=on_press, on_release=on_release) as keyboardListener:
                keyboardListener.join()


#获取窗体的标题---目的检查是否是在控制台上操作
def getWinTitle(win_hd):
    if win_hd is None:
        return None
    if win_hd==0:
        return None
    buffer = create_string_buffer(255,'\0')
    GetWindowText(win_hd,buffer,255)
    value=buffer.value.decode('gbk')
    return value

# 获取窗体矩形
# def getWindowRect(hWnd):
#     try:
#         f = ctypes.windll.dwmapi.DwmGetWindowAttribute
#     except WindowsError:
#         f = None
#     if f:
#         rect = ctypes.wintypes.RECT()
#         DWMWA_EXTENDED_FRAME_BOUNDS = 9
#         f(ctypes.wintypes.HWND(hWnd),
#           ctypes.wintypes.DWORD(DWMWA_EXTENDED_FRAME_BOUNDS),
#           ctypes.byref(rect),
#           ctypes.sizeof(rect)
#           )
#         return rect
#根据全体坐标获取窗体内相对坐标,(目前在x方向不精确)在分辨率缩放设置不是100%的情况下会出现bug
#最好更换方式,使用pyqt自带的,只需要获取label控件相对于整个window窗口的坐标就好
# def getWindowPosintion(hWnd,x,y):
#     rect_outer = getWindowRect(hWnd)
#     rect_inner = win32gui.GetClientRect(hWnd)
#     height_outer=rect_outer.bottom-rect_outer.top
#     height_inner=rect_inner[3]-rect_inner[1]
#     height_title_bar=height_outer-height_inner
#     x_relative=x-rect_outer.left
#     y_relative = y - rect_outer.top-height_title_bar
#     return x_relative,y_relative
#
# def getWindowPosintion(videoBox,x,y):
#     x_relative=x-videoBox.geometry().x()-videoBox.pictureLabel.x()
#     y_relative = y -videoBox.geometry().y()-videoBox.pictureLabel.y()
#     return x_relative,y_relative

#获取坐标点,相对于某一个某个客户端的坐标点,并连带客户端一起返回
def getPosInPhoneScreen(videoBox,x,y):
    #这个应该就是在leftLayout里面的坐标了
    x =x-videoBox.geometry().x()-videoBox.mainLayout.geometry().x()
    y = y -videoBox.geometry().y()-videoBox.mainLayout.geometry().y()
    width=videoBox.leftLayout.geometry().width()
    height=videoBox.leftLayout.geometry().height()
    if (x<0 or y<0 or x>width or y >height):
        return None,None,None
    for client,screen in zip(videoBox.clients,videoBox.pictureLabels):
        rect = screen.geometry()
        if (x>rect.x() and y>rect.y()):
            if x-rect.x()<rect.width():
                if y-rect.y()<rect.height():
                    return client,(x-rect.x(),y-rect.y()),screen
    return None,None,None

