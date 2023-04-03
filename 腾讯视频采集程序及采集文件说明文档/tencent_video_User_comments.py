# _*_ coding : utf-8_*_
# @  Time：2022/12/3 12:31
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

web.implicitly_wait(5)  # 隐式等待5秒，模拟人工操作，骗过网站，反反爬技术

comments_ip = open("视频链接.txt")  # 读取视频链接的文件
lianjie = comments_ip.read().split("\n")
header = ['\n名字', '时间', '内容\n']  # 定义csv文件的表头

with open('腾讯视频有关评论.csv', mode='w', encoding='utf-8', newline="\n") as f:

    for j in range(0, len(lianjie)):
        web.get(lianjie[j])# 获取腾讯视频分区内容
        sleep(5)

        writer = csv.DictWriter(f, header)  # 以字典的方式写入
        # 写入表头的信息需要调用writeheader()
        writer.writeheader()
        a = 0  # a为后来用来计数一共爬了多少页的FLAG
        js = 'var a = document.documentElement.scrollTop=1000'  # js代码滚动条下拉
        web.execute_script(js)  # 执行js代码
        sleep(3)  # 在两次滚动中间停止一秒，模拟人工滚动（算是简单的反反爬）
        web.execute_script(js)
        # 以上是实现在网页中通过脚本的方式刷新评论

        # 用户的名字
        user_reviews_name = web.find_elements(By.XPATH,
                                                  '//*[@id="commentWrapper"]/section/div[2]/div[3]/div[1]/div/div[1]/div/div[1]/div/div/span')
        # 评论时间
        user_reviews_time = web.find_elements(By.XPATH,
                                                  '//*[@id="commentWrapper"]/section/div[2]/div[3]/div[1]/div/div/div/div[1]/div/div[4]')
        # 评论内容
        user_reviews_content = web.find_elements(By.XPATH,
                                                  '//*[@id="commentWrapper"]/section/div[2]/div[3]/div[1]/div/div[1]/div/div[2]/div/div/div[1]')

        for i in range(10):
            # 以字典形式输出内容
            dic = { '\n名字': user_reviews_name[i].text,
                    '时间': user_reviews_time[i].text,
                    '内容\n': user_reviews_content[i].text
                  }
            # 将结果dic写进去csv文件里面
            writer.writerow(dic)
    # 关闭浏览器
    web.quit()
