# coding=utf-8
import traceback
import json
import time
# 动作模板
def action_template():
    return {
        "method": "keyboard",
        "time": "default",
        "type": "default",
        "buttons": "default",
        "action": "default",
        "x": "default",
        "y": "default",
        "screenWidth": "default",
        "screenHeight": "default",
        "hScroll": "default",
        "vScroll": "default",
        "keycode": "default",
        "metaState": "default",
        "text": "default"
    }

class Recorder:
    def __init__(self,file_name='record.action'):
        self.recorded=False
        self.file_name = file_name
        self.file =  None

    def to_file(self,template):
        self.file.writelines(json.dumps(template) + "\n")
        self.file.flush()

    def start_record(self):
        self.file=open(self.file_name, 'w', encoding='utf-8')
        self.recorded = True

    def stop_record(self):
        self.file.close()
        self.recorded = False

    def toRecord(self,method, type, buttons=None, action=None, x=None, y=None, screenWidth=None, screenHeight=None, hScroll=None, vScroll=None, keycode=None, metaState=None, text=None):
        if not self.recorded:
            return
        template = action_template()
        template['method'] = method
        template['time'] = round(time.time(), 3)
        if method == "leftBtnClick":
                template['type'] = type
                template['buttons'] = buttons
                template['action'] = action
                template['x'] = x
                template['y'] = y
                template['screenWidth'] = screenWidth
                template['screenHeight'] = screenHeight
                self.to_file(template)
                return
        if method == "rightBtnClick":
            if type == 4:
                template['type'] = type
                template['action'] = action
                self.to_file(template)
                return
            template['type'] = type
            template['buttons'] = buttons
            template['action'] = action
            template['x'] = x
            template['y'] = y
            template['screenWidth'] = screenWidth
            template['screenHeight'] = screenHeight
            self.to_file(template)
            return
        if method == "middleBtnScroll":
            template['type'] = type
            template['x'] = x
            template['y'] = y
            template['hScroll'] = hScroll
            template['vScroll'] = vScroll
            template['screenWidth'] = screenWidth
            template['screenHeight'] = screenHeight
            self.to_file(template)
            return
        if method == "drag":
            template['type'] = type
            template['buttons'] = buttons
            template['action'] = action
            template['x'] = x
            template['y'] = y
            template['screenWidth'] = screenWidth
            template['screenHeight'] = screenHeight
            self.to_file(template)
            return
        if method == "keycodeClick":
            template['type'] = type
            template['metaState'] = metaState
            template['action'] = action
            template['keycode'] = keycode
            self.to_file(template)
            return
        if method == "textClick":
            template['type'] = type
            template['text'] = text
            self.to_file(template)
            return
        if method == "toggleScreenPower":
            template['type'] = type
            template['action'] = action
            self.to_file(template)
            return

    def bytes_content(self,method, type, buttons=None, action=None, x=None, y=None, screenWidth=None, screenHeight=None, hScroll=None, vScroll=None, keycode=None, metaState=None, text=None):
            try:
                self.toRecord(method=method, type=type, buttons=buttons, action=action, x=x, y=y, screenWidth=screenWidth,
                              screenHeight=screenHeight, hScroll=hScroll, vScroll=vScroll, keycode=keycode,
                              metaState=metaState, text=text)

                if method=="leftBtnClick":
                        x = x.to_bytes(4, byteorder='big')
                        y = y.to_bytes(4, byteorder='big')
                        type = type.to_bytes(1, byteorder='big')
                        buttons = buttons.to_bytes(4, byteorder='big')
                        action = action.to_bytes(1, byteorder='big')
                        screenWidth = screenWidth.to_bytes(2, byteorder='big')
                        screenHeight = screenHeight.to_bytes(2, byteorder='big')
                        content = type + action + buttons + x + y + screenWidth + screenHeight
                        return content
                if method=="rightBtnClick":
                    if type==4:
                        type = type.to_bytes(1, byteorder='big')
                        action = action.to_bytes(1, byteorder='big')
                        content = type + action
                        return content
                    x = x.to_bytes(4, byteorder='big')
                    y = y.to_bytes(4, byteorder='big')
                    type = type.to_bytes(1, byteorder='big')
                    action = action.to_bytes(1, byteorder='big')
                    buttons = buttons.to_bytes(4, byteorder='big')
                    screenWidth = screenWidth.to_bytes(2, byteorder='big')
                    screenHeight = screenHeight.to_bytes(2, byteorder='big')
                    content = type + action + buttons + x + y + screenWidth + screenHeight
                    return content
                if method=="middleBtnScroll":
                    type = type.to_bytes(1, byteorder='big')
                    x = x.to_bytes(4, byteorder='big')
                    y = y.to_bytes(4, byteorder='big')
                    hScroll = hScroll.to_bytes(4, byteorder='big', signed='true')
                    vScroll = vScroll.to_bytes(4, byteorder='big', signed='true')
                    screenWidth = screenWidth.to_bytes(2, byteorder='big')
                    screenHeight = screenHeight.to_bytes(2, byteorder='big')
                    content = type + x + y + screenWidth + screenHeight + hScroll + vScroll
                    return content
                if method=="drag":
                    type = type.to_bytes(1, byteorder='big')
                    buttons = buttons.to_bytes(4, byteorder='big')
                    action = action.to_bytes(1, byteorder='big')
                    x = x.to_bytes(4, byteorder='big')
                    y = y.to_bytes(4, byteorder='big')
                    screenWidth = screenWidth.to_bytes(2, byteorder='big')
                    screenHeight = screenHeight.to_bytes(2, byteorder='big')
                    content = type + action + buttons + x + y + screenWidth + screenHeight
                    return content
                if method=="keycodeClick":
                    type = type.to_bytes(1, byteorder='big')
                    metaState = metaState.to_bytes(4, byteorder='big')
                    action = action.to_bytes(1, byteorder='big')
                    keycode = keycode.to_bytes(4, byteorder='big')
                    content = type + action + keycode + metaState
                    return content
                if method=="textClick":
                    type = type.to_bytes(1, byteorder='big')
                    text = bytes(text, encoding="utf8")
                    length = len(text)
                    length = length.to_bytes(2, byteorder='big')
                    content = type + length + text
                    return content
                if method=="toggleScreenPower":
                    type = type.to_bytes(1, byteorder='big')
                    action = action.to_bytes(1, byteorder='big')
                    content = type + action
                    return content
            except Exception as e:
                print(e.args)
                print("==============")
                print(traceback.format_exc())
            return None
#注意 字符格式,字符串还是整型
    def file_to_content(self):
        with open(self.file_name, 'r', encoding='utf-8') as file:
            line = file.readline()
            contents=[]
            while line:
                template = json.loads(line)
                method=template['method']
                content=None
                if method == 'leftBtnClick':
                    type=int(template['type'])
                    buttons=int(template['buttons'])
                    action=int(template['action'])
                    x=int(template['x'])
                    y=int(template['y'])
                    screenWidth = int(template['screenWidth'])
                    screenHeight = int(template['screenHeight'])
                    content=self.bytes_content(method=method,type=type,action=action,buttons=buttons,x=x,y=y,screenWidth=screenWidth,screenHeight=screenHeight)
                elif method == 'rightBtnClick':
                    type = int(template['type'])
                    if type==4:
                        action = int(template['action'])
                        content=self.bytes_content(method=method,type=type,action=action)
                    else:
                        action = int(template['action'])
                        buttons = int(template['buttons'])
                        x = int(template['x'])
                        y = int(template['y'])
                        screenWidth = int(template['screenWidth'])
                        screenHeight = int(template['screenHeight'])
                        content=self.bytes_content(method=method,type=type,action=action,buttons=buttons,x=x,y=y,screenWidth=screenWidth,screenHeight=screenHeight)
                elif method=="middleBtnScroll":
                    type = int(template['type'])
                    hScroll = int(template['hScroll'])
                    vScroll = int(template['vScroll'])
                    screenWidth = int(template['screenWidth'])
                    screenHeight = int(template['screenHeight'])
                    x = int(template['x'])
                    y = int(template['y'])
                    content=self.bytes_content(method=method, type=type, hScroll=hScroll, vScroll=vScroll,screenWidth=screenWidth, screenHeight=screenHeight, x=x, y=y)
                elif method=="drag":
                    type = int(template['type'])
                    buttons = int(template['buttons'])
                    action = int(template['action'])
                    screenWidth = int(template['screenWidth'])
                    screenHeight = int(template['screenHeight'])
                    x = int(template['x'])
                    y = int(template['y'])
                    content=self.bytes_content(method=method, type=type, buttons=buttons, action=action,screenWidth=screenWidth, screenHeight=screenHeight, x=x, y=y)
                elif method == 'keycodeClick':
                    type = int(template['type'])
                    metaState = int(template['metaState'])
                    action = int(template['action'])
                    keycode = int(template['keycode'])
                    content=self.bytes_content(method=method, type=type, metaState=metaState, action=action, keycode=keycode)
                elif method == 'textClick':
                    type = int(template['type'])
                    text = int(template['text'])
                    content=self.bytes_content(method=method, type=type, text=text)
                elif method == 'toggleScreenPower':
                    type = int(template['type'])
                    action = int(template['action'])
                    content=self.bytes_content(method=method, type=type, action=action)
                if content:
                    _time=float(template['time'])
                    contents.append((_time,content))
                line = file.readline()
            return contents