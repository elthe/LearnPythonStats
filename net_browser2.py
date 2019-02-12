import time
from selenium import webdriver

# 浏览器
browser = webdriver.Chrome('/opt/chrome/chromedriver')
# 入口网址
browser.get("http://gs.amac.org.cn/amac-infodisc/res/pof/fund/index.html")

# 等待5秒
time.sleep(5)
# 输出网页内容
print(browser.page_source)

# 关闭按钮
btnClose = browser.find_element_by_css_selector(".ui-dialog-buttonset").find_element_by_css_selector(".ui-button-text")
btnClose.click()
# 等待2秒
time.sleep(2)

# 输入关键词
inputKeyword = browser.find_element_by_id("keyword")
inputKeyword.send_keys("关键词")

# 点击查询按钮
btnSearch = browser.find_element_by_css_selector(".control-group.text-right").find_element_by_css_selector(".btn.btn-primary")
btnSearch.click()

# 等待3秒
time.sleep(3)

hrefList= []

# 取得总页数
pageStr = browser.find_element_by_id("fundlist_info").text
posStart = pageStr.find("，共")
posEnd = pageStr.find("页")
pageNum = int(pageStr[posStart+2:posEnd])
print(pageNum)

# 对每页进行循环
for i in range(pageNum - 1):
    # 读取当前页面的基金名和链接
    trList = browser.find_element_by_id("fundlist").find_element_by_tag_name("tbody").find_elements_by_tag_name("tr")
    for trData in trList:
        tdList = trData.find_elements_by_tag_name("td")
        tdFundName = tdList[1]
        hrefTxt = tdFundName.find_element_by_tag_name("a").get_attribute("href")
        fundName = tdFundName.find_element_by_tag_name("a").text
        hrefList.append({
            "name": fundName,
            "link": hrefTxt
        })

    # 点击下一页按钮
    btnNext = browser.find_element_by_id("fundlist_paginate").find_element_by_css_selector(".paginate_button.next")
    btnNext.click()

    # 等待3秒
    time.sleep(3)

# 输出全部链接
print(hrefList, "hrefList")

