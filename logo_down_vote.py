import pyautogui
import os, time, threading
from datetime import datetime
import numpy as np

'returning position (x,y) of mouse'
def get_pos():
    return tuple(pyautogui.position())

'Movements of Mouse Absolute & Relative'
def move(x,y,abs=True,duration=0):
    if abs:
        pyautogui.moveTo(  x,y,duration=duration )
    else:
        pyautogui.moveRel( x,y,duration=duration )

'Dragging with Mouse Absolute & Relative'
def drag(x,y,abs=True,duration=0.1):
    if abs:
        pyautogui.dragTo(  x,y,duration=duration )
    else:
        pyautogui.dragRel( x,y,duration=duration )

'Various types of clicks to be done'
def click(x,y,typ='left'):
    # ['left','down','up','middle','right','double']
    if typ=='left':
        pyautogui.click(x,y)
    elif typ=='down':
        pyautogui.mouseDown(x,y)
    elif typ=='up':
        pyautogui.mouseUp(x,y)
    elif typ=='middle':
        pyautogui.middleClick(x,y)
    elif typ=='right':
        pyautogui.rightClick(x,y)
    elif typ=='double':
        pyautogui.doubleClick(x,y)

'Scrolling with Mouse, +ve gives up-scroll'
def scroll(x):
    pyautogui.scroll(x)

'keyboard function'
def write(st,delay=0.1):
    'st can be atring or list of special keys'
    pyautogui.typewrite(st,delay=delay)
def key(st,state='press'):
    if state=='down':
        pyautogui.keyDown(st)
    elif state=='up':
        pyautogui.keyUp(st)
    elif state=='press':
        pyautogui.press(st)
def hotkey(*ls):
    pyautogui.hotkey(*ls)
def get_all_keys():
    return pyautogui.KEYBOARD_KEYS

'Screenshot & Image processing function'
def ss():
    return pyautogui.screenshot()
def pixel_value(im,x,y):
    return im.getpixel((x,y))
def match_color(im,x,y,val):
    return pyautogui.pixelMatchesColor(x,y,val)
def locate(img): # None if that cannot be found
    'return bounding box in form of (LX,LY,dX,dY)'
    pyautogui.locateOnScreen(img)
def locateAll(img):
    return list( pyautogui.locateAllOnScreen(img) )
def center(tpl):
    return pyautogui.center(tpl)


class AutomateSurvey(threading.Thread):
    def __init__(self,action_images_dir='.',PAUSE=1,FAILSAFE=True,sleep_duration=15,drag_limit=1,out_center=0.3):
        super(AutomateSurvey, self).__init__()
        self.main_running, self.auto_thread_running = True, False
        self.action_images_dir = action_images_dir
        self.WIDTH, self.HEIGHT  = pyautogui.size()
        # Seconds of Pause after each function of pyautogui call
        pyautogui.PAUSE = PAUSE
        # Enabling FAILSAFE, moving to (0,0) raises 'pyautogui.FailSafeException'
        pyautogui.FAILSAFE = True 
       
        self.sleep_duration = sleep_duration
        self.drag_limit = drag_limit
        self.out_center = out_center
    
    def mcenter(self,tpl):
        tmp = pyautogui.center(tpl)
        return ( tmp[0]+tpl[2]*np.random.random()*self.out_center , tmp[1]+tpl[3]*np.random.random()*self.out_center )

    def mclick(self,*arg):
        delay = self.drag_limit*np.random.random()
        move(*arg,duration=delay) ; click(*arg)

    def wait_find_click(self,image,auto_scroll=0):
        while True:
            tmp = locateAll(self.action[image])
            if tmp:
                click_pos = self.mcenter(tmp[0])
                self.mclick(*click_pos)
                break
            time.sleep(self.sleep_duration)
            pyautogui.scroll(auto_scroll)
        

    def autorun(self):
        self.action = action = {x:os.path.join(self.action_images_dir,x) for x in os.listdir(self.action_images_dir)}
        pyautogui.hotkey('altleft','\t')
        count = 0
        while True:
            self.wait_find_click('1.PNG')
            self.wait_find_click('2.PNG',-1000)
            pyautogui.press('pagedown')
            self.wait_find_click('3.PNG',-1000)
            count+=1
            with open('click_count.txt','w') as f:
                f.write(str(count))


if __name__=='__main__':
    '                      directory, PAUSE, FAIL_SAFE, SLEEP_DURATION, DRAG_DELAY_LIMIT, OUT_CENTER'
    survey = AutomateSurvey( 'self',    0.2,      True,         0,               0,            0.25 )
    assert (survey.WIDTH,survey.HEIGHT)==(1366,768)
    survey.autorun()
    