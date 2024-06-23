import requests,json
import datetime,time
from loguru import logger


logger.add("loguru.log")
detail_id="85939"


if __name__=='__main__':
   for i in range(9999999):
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
 
        
        response = requests.get('https://show.bilibili.com/api/ticket/project/getV2?version=134&id='+detail_id+'&project_id='+detail_id+'&requestSource=pc-new', headers=headers)
        response=response.json()
        if(response['data']['is_sale']!=0 or response['data']['sale_begin']!=0 or  response['data']['sale_end']!=0 or response['data']['sale_flag']!='不可售'):
           is_sale=response['data']['is_sale']
           sale_begin=response['data']['sale_begin']
           sale_end=response['data']['sale_end']
           sale_flag=response['data']['sale_flag']
           msg=str(detail_id)+'有新变化：\nis_sale：'+str(is_sale)+'\nsale_begin：'+str(sale_begin)+'\nsale_end：'+str(sale_end)+'\nsale_flag：'+sale_flag
           ding_push_msg()
           
        time.sleep(30)   

