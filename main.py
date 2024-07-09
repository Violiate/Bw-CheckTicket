
import requests,json,urllib3
import datetime,time
from loguru import logger



detail_id="85939"
web_url = "https://oapi.dingtalk.com/robot/send?access_token="  #填写钉钉推送token
bl = "https://api.day.app/"   #填写bark推送token
token = '' #在pushpush网站中可以找到，填写pushpush推送token


logger.add("loguru.log")
def ding_push_message():
    # 构建请求头部
    header = {
        "Content-Type": "application/json",
        "Charset": "UTF-8"
    }
 
    # 构建请求数据
    message = {
        "msgtype": "text",
        "text": {
            "content": msg
        },
        "at": {
            "isAtAll": True 
        }
    }
 
    # 对请求的数据进行json封装
    message_json = json.dumps(message)
    # 发送请求
    info = requests.post(url=web_url, data=message_json, headers=header)
    # 打印返回的结果
    logger.info(info.text)

def pushplus_notify(title,content):
    today=datetime.date.today()
    date_text=today.strftime("%Y-%m-%d")
    
    title= title+date_text
    url = 'http://www.pushplus.plus/send'
    data = {
        "token":token,
        "title":title,
        "content":content
    }
    body=json.dumps(data).encode(encoding='utf-8')
    headers = {'Content-Type':'application/json'}
    requests.post(url,data=body,headers=headers)

def send2bark(self,title, content):
        
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        try:

            for i in range(4):
             msg = "{0}/{1}/{2}/?sound=update".format(bl, title, content)
             link = msg  
             res = requests.get(link, verify=False)
             time.sleep(6)
        except Exception as e:
            logger.error('Reason:', e)
            return
        return

if __name__=='__main__':
   while True:
       try:
        with open("settings.json",'r',encoding='utf-8')as settings_f:
         settings=json.load(settings_f)
       except:
           
                
            settings={}
            
            settings['sale_begin']=0
            settings['sale_end']=0
            settings['is_sale']=0
            settings['sale_flag']='0'
            settings['length']=0
            with open("settings.json",'w',encoding='utf-8')as settings_f:
                 json.dump(settings, settings_f,ensure_ascii=False)
       headers = {
          'authority': 'show.bilibili.com',
          'accept': '*/*',
          'accept-language': 'zh-CN,zh;q=0.9',
          'cookie': '',
          'referer': 'https://show.bilibili.com/platform/detail.html?id='+detail_id,
          'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
          'sec-ch-ua-mobile': '?0',
          'sec-ch-ua-platform': '"Windows"',
          'sec-fetch-dest': 'empty',
          'sec-fetch-mode': 'cors',
          'sec-fetch-site': 'same-origin',
          'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
               }
 
       url='https://show.bilibili.com/api/ticket/project/getV2?version=134&id='+detail_id+'&project_id='+detail_id+'&requestSource=pc-new'
       try:
         response = requests.get(url=url, headers=headers)
         response=response.json()

         if(response['data']['is_sale']!= settings['is_sale'] or response['data']['sale_begin']!= settings['sale_begin'] or  response['data']['sale_end']!= settings['sale_end'] or response['data']['sale_flag']!=settings['sale_flag'] or  len(response["data"]["screen_list" ])!=settings['length']):
           title=response['data']['name']
           logger.debug(response)
           is_sale=response['data']['is_sale']
           sale_begin=response['data']['sale_begin']
           settings['sale_begin']=response['data']['sale_begin']
           settings['sale_end']=response['data']['sale_end']
           settings['is_sale']=response['data']['is_sale']
           settings['sale_flag']= response['data']['sale_flag']
           settings['length']=len(response["data"]["screen_list" ])
           with open("settings.json",'w',encoding='utf-8')as settings_f:
                 json.dump(settings, settings_f,ensure_ascii=False)
           if(int(sale_begin)!=0):
              #转换成localtime
              time_local = time.localtime(sale_begin)
              #转换成新的时间格式(2016-05-05 20:28:54)
              start_readtime = time.strftime("%Y-%m-%d %H:%M:%S",time_local)
           else:
              start_readtime='0'
           sale_end=response['data']['sale_end']
           if(int(sale_end)!=0):
              #转换成localtime
              time_local = time.localtime(sale_end)
              #转换成新的时间格式(2016-05-05 20:28:54)
              end_readtime = time.strftime("%Y-%m-%d %H:%M:%S",time_local)
           else:
              end_readtime='0'
           sale_flag=response['data']['sale_flag']
           msg=title+' '+str(detail_id)+'有新变化：\n是否可售：'+str(is_sale)+'\n售票开始时间：'+str(start_readtime)+'\n售票结束时间：'+str(end_readtime)+'\n状态：'+sale_flag+'\n'
           logger.info(msg)
           try:
            ding_push_message()
           except Exception as e:
              logger.error('\n钉钉推送出错!\n')
           try:
            pushplus_notify('监控'+title+'有新变化！',msg)
           except Exception as e:
              logger.error('\nPushPlus推送出错!\n')
           try:
            send2bark(1,'监控'+title+'有新变化！',msg)
           except Exception as e:
              logger.error('\nbark推送出错!\n')
              
         time.sleep(8)   
       except Exception as e:
          logger.debug(response.text)
          logger.error('\n本轮请求出错!\n')
