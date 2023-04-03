# _*_ coding : utf-8_*_
# @  Time：2022/11/27 17:53
# @Author ：肖宇宁
# @File ：
# @Project :pythonfile

from selenium.webdriver import Edge
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
import csv
from time import sleep


# 创建webdriver对象
opt = Options()
opt.add_argument('--headless')
opt.add_argument('--disable-gpu')
web = Edge(options=opt)

web.implicitly_wait(5) # 隐式等待5秒，模拟人工操作，骗过网站，反反爬技术
web.get("https://v.qq.com/channel/cartoon/list?filter_params=itype%3D5%26iarea%3D"
        "-1%26iyear%3D-1%26ipay%3D1%26anime_status%3D-1%"
        "26item%3D1%26sort%3D75&page_id=channel_list_second_page") # 获取腾讯视频分区内容
header = ['视频名字', '视频介绍', '视频链接'] #定义csv文件的表头

with open('腾讯视频基本信息.csv', mode='w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, header) # 以字典的方式写入
    # 写入表头的信息需要调用writeheader()
    writer.writeheader()
    a = 0 # a为后来用来计数一共爬了多少页的FLAG
    while 1:     # 循环
        js = 'var a = document.documentElement.scrollTop=1000000' # js代码滚动条下拉
        web.execute_script(js)  # 执行js代码
        sleep(1)  # 在两次滚动中间停止一秒，模拟人工滚动（算是简单的反反爬）
        web.execute_script(js)
        # 以上是实现在网页中通过脚本的方式刷新评论
        # video_first_list=web.find_elements(By.XPATH,"//div[@class='list-page-content']")#总页面
        video_name_list = web.find_elements(By.XPATH,"//a[@class='card vertical']/div[@class='info-wrap']/div[@class='title']")     #视频的名字
        video_talking_list = web.find_elements(By.XPATH,"//a[@class='card vertical']/div[@class='info-wrap']/div[@class='sub-title']") #视频的介绍
        req = web.find_elements(By.XPATH,"//div[@class='card-list-wrap']/a[@href]")     #视频链接
        video_ip_list = ([i.get_attribute("href") for i in req])

        for i in range(len(video_name_list)):
            item = i + 1 + a * 10  # 计算页数
            dic = {'视频名字': video_name_list[i].text,'视频介绍':video_talking_list[i].text,'视频链接':video_ip_list[i].__str__()}# 输出形式是一个字典
            writer.writerow(dic) #将结果dic写进去csv文件里面
        web.quit()  # 记得关闭浏览器
        break

'''
这里是关键，将本页面获取的视频链接写入txt文件中，方便下一步的爬取该地址的评论
'''
caigou = "\n".join(video_ip_list )#将视频链接格式改为str格式
Note = open("视频链接.txt",mode="w",encoding='utf-8')
Note.write(caigou)
Note.close()


