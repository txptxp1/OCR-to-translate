import tkintertools as tkt
import requests
import json
import os
from threading import Thread
import tkinter
from tkinter import *
from tkinter import messagebox
import pygetwindow
from pynput import mouse
import pyautogui
from PIL import Image
import base64
import time
import shutil
import json
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException 
from tencentcloud.tmt.v20180321 import tmt_client, models
from paddleocr import PaddleOCR

class Local_OCR():
    def __init__(self,sourcetext) -> None:
        self.sourcetext=sourcetext

    def localocr(self):
        ocr = PaddleOCR(use_angle_cls=True, lang=f"{self.sourcetext}")
        #要识别图片的路径：
        img_path = r"trans.png"
        #识别结果：
        result = ocr.ocr(img_path, cls=True)
        #结果输出展示：
        lst=[]
        try:
            for i in range(len(result[0])):
                print(result[0][i][1][0])   # 输出识别结果
                lst.append(result[0][i][1][0])
            connected_text = ' '.join(lst)
            return connected_text
        except TypeError:
            print (TypeError)

class Trans():
    def __init__(self,sourceText,source,target,transID,transKEY):
        self.sourceText=sourceText
        self.source=source
        self.target=target
        self.transID=transID
        self.transKEY=transKEY

    def trans(self):
            
        try: 
            cred = credential.Credential(f"{self.transID}", f"{self.transKEY}") 
            httpProfile = HttpProfile()
            httpProfile.endpoint = "tmt.tencentcloudapi.com"

            clientProfile = ClientProfile()
            clientProfile.httpProfile = httpProfile
            client = tmt_client.TmtClient(cred, "ap-beijing", clientProfile) 

            req = models.TextTranslateRequest()
            req.SourceText = f"{self.sourceText}"
            req.Source = f"{self.source}"
            req.Target = f"{self.target}"
            req.ProjectId = 0

            resp = client.TextTranslate(req) 
            print(resp.to_json_string()) 
            return resp.to_json_string()
        except TencentCloudSDKException as err: 
            print(err)
if os.path.exists('save'):
    pass
else:
    os.mkdir('save')

if os.path.exists('temp'):
    pass
else:
    os.mkdir('temp')

try:
    with open('_config.json','r',encoding='utf-8')as f:
        load_dict=json.load(f)
        OCRtime=load_dict['OCRtime']
except:
    OCRtime=0

try:
    with open('_ocr.json','r',encoding='utf-8')as f:
        load_dict=json.load(f)
        local_ocr=load_dict['local_ocr']
except:
    local_ocr=None

try:
    with open('_token.json','r',encoding='utf-8')as f:
        load_dict = json.load(f)
        access_token=load_dict['access_token']
        #print (access_token)
except:
    access_token=None

try:
    with open('_trans_token.json','r',encoding='utf-8')as f:
        load_dict = json.load(f)
        transid=load_dict['transid']
        transkey=load_dict['transkey']
        #print (access_token)
except:
    transid=None
    transkey=None
#
try:
    with open('_ocrlangs.json','r',encoding='utf-8')as f:
        load_dict = json.load(f)
        OCRlangset=load_dict['OCRlangs']
except:
    OCRlangset='en'


try:
    with open('_source_and_target.json','r',encoding='utf-8')as f:
        load_dict = json.load(f)
        sourcetext=load_dict['sourcetext']
        targettext=load_dict['targettext']
        #print (access_token)
except:
    sourcetext='en'
    targettext='zh'

def trans(source_trans_Text):
    if source_trans_Text!='':
        post=Trans(sourceText=f'{source_trans_Text}',source=f'{sourcetext}',target=f'{targettext}',transID=f'{transid}',transKEY=f'{transkey}')
        transtext=post.trans()
        trans_text=eval(transtext)
        result=trans_text['TargetText']
        show_text_label.configure(text=f'{result}')

ocr_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic"
def ocr(path):
    # 二进制方式打开图片文件
    with open(path, 'rb')as f:
        img = base64.b64encode(f.read())
    params = {"image":img}
    #print (access_token)
    request_url = ocr_url + "?access_token=" +access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    if response:
        #print (response.json())
        word=response.json()
        # 使用列表推导式提取所有words的值 
        print (word) 
        all_words = [result['words'] for result in word['words_result']]  

        # 将all_words列表转换为一个由逗号加空格分隔的字符串  
        words_str = ', '.join(all_words)  
        #print(words_str)  # 输出: OCR实时图片识别1, OCR实时图片识别2, OCR实时图片识别3
        trans(words_str)

def local_ocr_identify():
    local=Local_OCR(sourcetext=OCRlangset)
    a=local.localocr()
    trans(a)

def launch():
    launchtoplevel=tkt.Toplevel(root,width=1000,height=600,title='Launch')
    launch=tkt.Canvas(launchtoplevel,1000,600,x=0,y=0)
    tkt.Label(launch,55,20,width=60,height=20,font=(tkt.FONT,20),text='选择游戏进程',borderwidth=0,color_fill=tkt.COLOR_NONE)
    tkt.Label(launch,100,50,width=60,height=20,font=(tkt.FONT,12),text='点击该按钮后再点击你想锁定的进程',borderwidth=0,color_fill=tkt.COLOR_NONE)
    threadshow=tkt.Label(launch,60,120,justify='left',width=900,height=15,font=(tkt.FONT,10),text='未锁定进程',borderwidth=0,color_fill=tkt.COLOR_NONE)
    def cannel():
        imgshow.destroy()
        threadshow.configure(text='未锁定进程')
        started.set_live(value=True)
        nexted.set_live(value=False)
        canneled.set_live(value=False)

    def cut(windows):
        window = pygetwindow.getWindowsWithTitle(windows)[0]
        left, top, width, height = window.left, window.top, window.width, window.height
        # 截图
        #print (left, top, width, height)
        screenshot = pyautogui.screenshot(region=(left, top, width, height))
        # 保存截图
        screenshot.save(rf'temp/{windows}.png')
        #载入截图
        image = Image.open(rf'temp/{windows}.png')
        # 计算缩放因子
        width, height = image.size
        max_size = (600,450)  # 假设最大尺寸为200x150
        # 计算缩放因子
        width_factor = max_size[0] / width
        height_factor = max_size[1] / height
        factor = min(width_factor, height_factor)
        # 使用缩放因子计算新的图像尺寸
        new_size = (int(width * factor), int(height * factor))

        # 调整图像大小
        resized_image_with_ratio = image.resize(new_size)

        # 保存调整大小后的图像
        resized_image_with_ratio.save(rf'temp/{windows}_show.png')
        resized_image_with_ratio.save(rf'save/{windows}_show.png')
        global imgshow
        imgshow=tkt.Label(launch,320,160,width=600,justify='left',height=400,borderwidth=0,color_fill=tkt.COLOR_NONE,image=tkt.PhotoImage(file=rf'temp/{windows}_show.png'))
        started.set_live(value=False)
        nexted.set_live(value=True)
        canneled.set_live(value=True)



    def on_click():
        with mouse.Events() as events:
            for event in events:
                if hasattr(event, 'button'):
                    if event.button == mouse.Button.left:
                        global windows
                        windows = pygetwindow.getActiveWindowTitle()
                        #print (windows)
                        if windows!='Launch':
                            threadshow.configure(text='已锁定进程，进程为:'+windows)
                            cut(windows=windows)
                            return False
    

    def next():
        messagebox.showinfo('tips','请绘制需要翻译的区域',parent=launchtoplevel)
        launchtoplevel.destroy()
        image = Image.open(rf'temp/{windows}.png')
        # 计算缩放因子
        width, height = image.size
        draw=tkt.Toplevel(root,width=width,height=height,title='Draw')
        drawcavens=tkt.Canvas(draw,x=0,y=0,width=width,height=height)
        tkt.Label(drawcavens,0,0,height=height,width=width,borderwidth=0,color_fill=tkt.COLOR_NONE,image=tkt.PhotoImage(file=rf'temp/{windows}.png'))

        def on_press(event):
            global x_start,y_start,rect
            x_start=event.x
            y_start=event.y
            #print (x_start,y_start)
            rect=drawcavens.create_rectangle(x_start,y_start,1,1,outline='red')
            return x_start,y_start

        def on_move_press(event):
            curX, curY = (event.x, event.y)
            # expand rectangle as you drag the mouse
            drawcavens.coords(rect,x_start,y_start,curX, curY)

        def on_release(event):
            global x_end,y_end
            x_end=event.x
            y_end=event.y
            #print (x_end,y_end)
            msg = messagebox.askokcancel('tips', '确定或者取消？',parent=draw)
            if msg==True:
                draw.destroy()
                show()
                return x_end,y_end
            elif msg==False:
                drawcavens.delete(rect)
        
        def show():
            global show_text_label,showtext
            showtext=tkt.Tk(title='翻译结果',width=1150,height=240,topmost=True,alpha=0.4)
            showtext.resizable(0,0)
            canvesshow_text=tkt.Canvas(showtext,1150,240,x=0,y=0,background='#ead4db')
            show_text_label=tkinter.Message(canvesshow_text,width=1100,font=(tkt.FONT,10),text='')
            show_text_label.place(x=50,y=20,width=1100,height=200)
            t1=Thread(target=ready)
            t1.start()
            showtext.mainloop()
            

        def ready():
            while True:
                window = pygetwindow.getWindowsWithTitle(windows)[0]
                left, top, width, height =window.left+x_start,window.top+y_start,x_end-x_start,y_end-y_start
                recognition=pyautogui.screenshot(region=(left,top,width,height))
                recognition.save(rf'trans.png')
                path=rf'trans.png'
                if local_ocr==True:
                    local_ocr_identify()
                else:
                    if access_token!=None:
                        ocr(path)
                        time.sleep(OCRtime)
                    else: 
                        messagebox.showerror('error','未配置ocr')
                        break

        drawcavens.bind('<ButtonPress-1>',on_press)
        drawcavens.bind('<ButtonRelease-1>',on_release)
        drawcavens.bind("<B1-Motion>",on_move_press)





    started=tkt.Button(launch,60,80,font=(tkt.FONT,8),text='start',width=60,height=20,command=on_click)
    canneled=tkt.Button(launch,30,170,text='取消选择',font=(tkt.FONT,8),width=60,height=20,command=cannel)
    nexted=tkt.Button(launch,100,170,text='下一步',font=(tkt.FONT,8),width=60,height=20,command=next)
    nexted.set_live(value=False)
    canneled.set_live(value=False)


            
def posttrans():
    transid=transID.get()
    transkey=transKEY.get()
    post=Trans(sourceText='hello',source='en',target='zh',transID=f'{transid}',transKEY=f'{transkey}')
    targettext=eval(post.trans())
    if targettext['TargetText']=='你好':
        trans_token={}
        new={"transid":transid,
             "transkey":transkey}
        trans_token.update(new)
        trans_token_info.configure(text='测试成功')
        with open('_trans_token.json','w',encoding='utf-8')as f:
            json.dump(trans_token,f, ensure_ascii=False, indent=4)
    else:
        trans_token_info.configure(text='失败，请检查你的id和key')


def source_and_target():
    global sourcetext,targettext
    sourcetext=source.get()
    targettext=target.get()
    with open('_source_and_target.json','w',encoding='utf-8') as f:
        sourceandtarget={"sourcetext":sourcetext,"targettext":targettext}
        json.dump(sourceandtarget,f, ensure_ascii=False, indent=4)



def local_ocr_True():
    global local_ocr
    local_ocr=True
    with open('_ocr.json','w',encoding='utf-8')as f:
        new={"local_ocr":local_ocr}
        json.dump(new,f,ensure_ascii=False,indent=4)
    local_ocr_T.set_live(value=False)
    local_ocr_F.set_live(value=True)


def local_ocr_False():
    global local_ocr
    local_ocr=False
    with open('_ocr.json','w',encoding='utf-8')as f:
        new={"local_ocr":local_ocr}
        json.dump(new,f,ensure_ascii=False,indent=4)
    local_ocr_F.set_live(value=False)
    local_ocr_T.set_live(value=True)

def post():
    APIkey=APIKey.get()
    Secretkey=SecretKey.get()
    url = f"https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={APIkey}&client_secret={Secretkey}"
    
    payload = ""
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)
    token={}
    #print(response.json())
    dic=response.json()
    try:
        global access_token
        access_token=dic['access_token']
        token_info.configure(text='绑定成功!'+access_token)
        if os.path.exists('_token.json'):
            new={"access_token":access_token}
            token.update(new)
            with open('_token.json','w',encoding='utf-8') as f:
                json.dump(token, f, ensure_ascii=False, indent=4)

        else:
            new={"access_token":access_token}
            token.update(new)
            with open('_token.json','w',encoding='utf-8')as f:
                json.dump(token, f, ensure_ascii=False, indent=4)

    except KeyError:
        Error = dic.get('error_description', '未知错误')
        # 在这里创建并显示错误标签
        token_info.configure(text=f'{Error}')
        #tkt.Label(OCR,200,150,width=100,height=20,borderwidth=0,text=Error,font=(tkt.FONT,8),color_fill=tkt.COLOR_NONE)

def saveOCRlangs():
    a=OCRlangs.get()
    with open('_ocrlangs.json','w',encoding='utf-8')as f:
        new={"OCRlangs":a}
        json.dump(new,f, ensure_ascii=False, indent=4)
    global OCRlangset
    OCRlangset=a




def config():
    config=tkt.Toplevel(root,title='Config',width=570,height=630)
    OCR=tkt.Canvas(config,570,630,x=0,y=0)
    Trans=tkt.Canvas(config,570,630,x=570,y=0)
    Other=tkt.Canvas(config,570,630,x=570,y=0)

    def setOCR():
        global OCR
        OCR=tkt.Canvas(config,570,630,x=0,y=0)
        Trans=tkt.Canvas(config,570,630,x=570,y=0)
        Other=tkt.Canvas(config,570,630,x=570,y=0)
        #OCR侧边按钮
        tkt.Label(OCR,80,0,width=50,height=30,text='设置',borderwidth=0,font=(tkt.FONT,15),color_fill=tkt.COLOR_NONE)
        tkt.Button(OCR,8,40,width=70,height=30,font=(tkt.FONT,8),text='OCR配置',command=setOCR)
        tkt.Button(OCR,8,70,width=70,height=30,font=(tkt.FONT,8),text='Translate配置',command=setTrans)
        tkt.Button(OCR,8,100,width=70,height=30,font=(tkt.FONT,8),text='其他配置',command=setOther)
        #界面布局
        global APIKey,SecretKey,token_info,OCRlangs,local_ocr_F,local_ocr_T
        tkt.Label(OCR,120,50,width=100,height=20,text='百度OCR access_token配置',borderwidth=0,font=(tkt.FONT,10),color_fill=tkt.COLOR_NONE)
        APIKey=tkt.Entry(OCR,120,80,text='请在此键入access_token的APIKey',width=190,height=20,font=(tkt.FONT,8))
        SecretKey=tkt.Entry(OCR,120,110,text='请在此键入access_token的SecretKey',width=190,height=20,font=(tkt.FONT,8))
        tkt.Button(OCR,430,90,text='上传',font=(tkt.FONT,8),width=50,height=30,command=post)
        token_info=tkt.Label(OCR,200,150,width=200,height=20,borderwidth=0,text='',font=(tkt.FONT,8),color_fill=tkt.COLOR_NONE)
        tkt.Label(OCR,120,180,width=100,height=20,borderwidth=0,text='启用本地OCR(较消耗性能且速度慢)',font=(tkt.FONT,8),color_fill=tkt.COLOR_NONE)
        local_ocr_T=tkt.Button(OCR,100,210,text='启用',font=(tkt.FONT,8),width=30,height=20,command=local_ocr_True)
        local_ocr_F=tkt.Button(OCR,150,210,text='禁用',font=(tkt.FONT,8),width=30,height=20,command=local_ocr_False)
        OCRlangs=tkt.Entry(OCR,150,240,text='输入OCR识别的文本',font=(tkt.FONT,8),width=150,height=20)
        tkt.Button(OCR,320,240,text='保存',font=(tkt.FONT,8),width=50,height=30,command=saveOCRlangs)
        if local_ocr==True:
            local_ocr_T.set_live(value=False)
            local_ocr_F.set_live(value=True)
        elif local_ocr==False:
            local_ocr_F.set_live(value=False)
            local_ocr_T.set_live(value=True)
        elif local_ocr==None:
            local_ocr_F.set_live(value=False)
            local_ocr_T.set_live(value=True)
        if access_token!=None:
            token_info.configure(text='已绑定')
        else:
            pass

    def setTrans():
        OCR=tkt.Canvas(config,570,630,x=570,y=0)
        Trans=tkt.Canvas(config,570,630,x=0,y=0)
        Other=tkt.Canvas(config,570,630,x=570,y=0)
        #Trans侧边按钮
        tkt.Label(Trans,80,0,width=50,height=30,text='设置',borderwidth=0,font=(tkt.FONT,15),color_fill=tkt.COLOR_NONE)
        tkt.Button(Trans,8,40,width=70,height=30,font=(tkt.FONT,8),text='OCR配置',command=setOCR)
        tkt.Button(Trans,8,70,width=70,height=30,font=(tkt.FONT,8),text='Translate配置',command=setTrans)
        tkt.Button(Trans,8,100,width=70,height=30,font=(tkt.FONT,8),text='其他配置',command=setOther)
        #界面布局
        tkt.Label(Trans,120,50,width=100,height=20,text='腾讯私人翻译 access_token配置',borderwidth=0,font=(tkt.FONT,10),color_fill=tkt.COLOR_NONE)
        global transID,transKEY,trans_token_info,source,target
        transID=tkt.Entry(Trans,120,80,text='请在此键入access_token的SerectID',width=190,height=20,font=(tkt.FONT,8))
        transKEY=tkt.Entry(Trans,120,110,text='请在此键入access_token的SecretKey',width=190,height=20,font=(tkt.FONT,8))
        tkt.Button(Trans,430,90,text='上传',font=(tkt.FONT,8),width=50,height=30,command=posttrans)
        trans_token_info=tkt.Label(Trans,200,150,width=200,height=20,borderwidth=0,text='',font=(tkt.FONT,8),color_fill=tkt.COLOR_NONE)
        source=tkt.Entry(Trans,120,140,text='输入源文本语言',width=90,height=20,font=(tkt.FONT,8))
        target=tkt.Entry(Trans,120,170,text='输入翻译文本语言',width=90,height=20,font=(tkt.FONT,8))
        tkt.Button(Trans,430,170,text='save',font=(tkt.FONT,8),width=50,height=30,command=source_and_target)

    def setOther():
        OCR=tkt.Canvas(config,570,630,x=570,y=0)
        Trans=tkt.Canvas(config,570,630,x=570,y=0)
        Other=tkt.Canvas(config,570,630,x=0,y=0)
        #Other侧边按钮
        tkt.Label(Other,80,0,width=50,height=30,text='设置',borderwidth=0,font=(tkt.FONT,15),color_fill=tkt.COLOR_NONE)
        tkt.Button(Other,8,40,width=70,height=30,font=(tkt.FONT,8),text='OCR配置',command=setOCR)
        tkt.Button(Other,8,70,width=70,height=30,font=(tkt.FONT,8),text='Translate配置',command=setTrans)
        tkt.Button(Other,8,100,width=70,height=30,font=(tkt.FONT,8),text='其他配置',command=setOther)
        #界面布局
        tkt.Label(Other,140,50,width=100,height=20,text='设定OCR扫描秒数',borderwidth=0,font=(tkt.FONT,10),color_fill=tkt.COLOR_NONE)
        tkt.Label(Other,200,80,width=100,height=20,text='默认为0\n调低此项可以适当减少OCR调用次数,但是会减慢OCR刷新',justify='left',borderwidth=0,font=(tkt.FONT,8),color_fill=tkt.COLOR_NONE)
        def savetime():
            try:
                setOCRtime1=float(setOCRtime.get())
                global OCRtime
                OCRtime=setOCRtime1
                show_OCRtime.configure(text=f'现在设定的刷新时间为{OCRtime}')
            except:
                messagebox.showerror('Warning','请输入数字',parent=config)
        global setOCRtime
        setOCRtime=tkt.Entry(Other,140,120,width=190,height=20,text='输入你想设定的OCR识别刷新秒数',font=(tkt.FONT,8))
        tkt.Button(Other,140,150,width=170,height=15,text='保存',font=(tkt.FONT,8),command=savetime)
        show_OCRtime=tkt.Label(Other,140,160,text=f'现在设定的刷新时间为{OCRtime}',width=150,height=15,font=(tkt.FONT,6),borderwidth=0,color_fill=tkt.COLOR_NONE)
        tkt.Label(Other,105,180,width=100,height=20,text='清除已绑定的token',borderwidth=0,font=(tkt.FONT,10),color_fill=tkt.COLOR_NONE)

        

        def delet():
            if access_token !=None:
                with open('_token.json','w',encoding='utf-8')as f:
                    f.write('\t')
                messagebox.showinfo('提示','token已解绑')
                return access_token,None
            else:
                messagebox.showinfo('提示','未配置token或文件不存在')
        tkt.Button(Other,105,210,width=40,height=20,text='清除',font=(tkt.FONT,8),command=delet)
        

    setOCR()


def quick_start():
    messagebox.showinfo('tips','未开发')
    '''quickwindow=pygetwindow.getAllWindows()
    detect=[]
    detect.append(quickwindow)
    for i in detect:
        file=os.walk(r'/save')
        for dirpath,dirname,filename in file:
            if filename==quickwindow:
                signwindow=quickwindow
                break
    if signwindow:
        windows=signwindow
        #ready()'''
    
    '''def refresh():
            show_text_label.configure(text=f'{words_str}')

        def ready():
            while True:
                window = pygetwindow.getWindowsWithTitle(windows)[0]
                left, top, width, height =window.left+x_start,window.top+y_start,x_end-x_start,y_end-y_start
                print (left, top, width, height)
                recognition=pyautogui.screenshot(region=(left,top,width,height))
                recognition.save(rf'trans.png')
                print ('success')
                path=rf'trans.png'
                if access_token!=None:
                    pass
                    ocr(path)
                    refresh()
                    #showtext.after(10, refresh)
                    #showtext.after(1500, ready)  # 1500毫秒后再次执行这个函数
                    time.sleep(OCRtime)
                    #ready()
            
            else:
                messagebox.showerror('error','未配置ocr')
            
            '''

def rootclose():
    try:
        showtext.destroy()
    except:
        pass
    shutil.rmtree('temp')
    root.destroy()





def rooted():
    global root
    root=tkt.Tk(title='OCR翻译',width=420,height=200,shutdown=rootclose)
    root.resizable(0,0)
    cavens=tkt.Canvas(root,420,200,x=0,y=0)
    cavens.create_text(35,10,text='OCR翻译器',font=(tkt.FONT,13))
    #cavens.create_image(420,200,image=tkt.PhotoImage('background.png'))
    tkt.Button(cavens,text='Launch',font=(tkt.FONT,8),x=10,y=160,width=60,height=30,command=launch)
    tkt.Button(cavens,text='Config',font=(tkt.FONT,8),x=80,y=160,width=60,height=30,command=config)
    #tkt.Button(cavens,text='Quick_start',font=(tkt.FONT,8),x=150,y=160,width=60,height=30,command=quick_start)
    root.mainloop()
rooted()