import scrapy
import requests
from scrapy.http import Request
from bs4 import BeautifulSoup
import random
from datetime import date, datetime, timedelta
import time
from AISpider.items.casey_items import CaseyItem
from common._date import get_all_month_

"""
网站分析：
1. search页面选择日期 进行ASP.NET_SessionId的注册,只有这个id注册后才能去请求搜索结果的页面
    payloads 在当前页面中可以取
    cookies 
        ASP.NET_SessionId 只要这一个就行
2. 更换月时 post请求search页面 302跳转跳转到结果页面不需要管结果用这个id请求一次
3. 从结果页面找链接 处理分页结果
4. 链接中取数据
5. 最早数据时间1993年10月28日至今
"""


class CaseySpider(scrapy.Spider):
    name = "casey"
    allowed_domains = ["casey-web.t1cloud.com"]
    start_urls = [
        "https://casey-web.t1cloud.com/T1PRDefault/WebApps/eProperty/P1/eTrack/eTrackApplicationSearch.aspx?r=P1.WEBGUEST&f=%24P1.ETR.SEARCH.ENQ"]
    custom_settings = {
        'LOG_STDOUT': True,
        # 'LOG_FILE': 'scrapy_casey.log',
        # 'DOWNLOAD_TIMEOUT': 1200
    }

    def __init__(self,category=None,days=None,*args, **kwargs):
        super(CaseySpider, self).__init__(*args, **kwargs)
        self.category = category

        if days == None:
            # 如果没有传days默认为这个月的数据
            self.days = get_this_month()
        else:
            now = datetime.now()
            days = int(days)
            date_from = (now - timedelta(days)).date().strftime('%d/%m/%Y')
            self.days = date_from
            # 这里计算出开始时间 设置到self.days
        self.headers = {
        }

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, dont_filter=True, callback=self.set_search_time)

    

    def set_search_time(self, response):
        # 设置开始时间 get_all_month获取时间
        if self.category == 'current':
            all_month = get_all_month_(self.days, datetime.now().date().strftime('%d/%m/%Y'))
            for index, y_date in enumerate(all_month):
                if y_date == all_month[-1]:
                    break
                start_time = y_date
                end_time = all_month[index + 1]
                print(start_time+"-----"+end_time)
                for item in self.parse(self, start_time, end_time):
                    yield item
        if self.category == 'past':
            all_month = get_all_month_(self.days, datetime.now().date().strftime('%d/%m/%Y'))
            for index, y_date in enumerate(all_month):
                if y_date == all_month[-1]:
                    break
                start_time = y_date
                end_time = all_month[index + 1]
                print(start_time+"-----"+end_time)
                for item in self.parse(self, start_time, end_time):
                    yield item
        if self.category != 'current' and self.category != 'past':
            print('set category error')
            return

    def parse(self, response, start_time, end_time):
        sessionID = self.get_sessionID(start_time, end_time)
        for item in self.get_search_results_urllist(sessionID, start_time, end_time):
            yield item

    """
    改变时间获取不同时间的sessionid 并进行post请求注册cookie
    result sessionid
    """

    def get_sessionID(self, start_time, end_time):
        search_url = 'https://casey-web.t1cloud.com/T1PRDefault/WebApps/eProperty/P1/eTrack/eTrackApplicationSearch.aspx?r=P1.WEBGUEST&f=%24P1.ETR.SEARCH.ENQ'
        resp = requests.get(search_url, headers=self.headers)
        main_page = BeautifulSoup(resp.text, "html.parser")
        viewstate = main_page.select_one("#__VIEWSTATE")
        viewstate = viewstate.get('value')
        viewstategenerator = main_page.select_one("#__VIEWSTATEGENERATOR")
        viewstategenerator = viewstategenerator.get('value')
        eventvalidation = main_page.select_one("#__EVENTVALIDATION")
        eventvalidation = eventvalidation.get('value')
        scrollpositiony = random.randint(1800, 2100)
        cookiejar = resp.cookies
        cookiedict = requests.utils.dict_from_cookiejar(cookiejar)
        start_time = str(start_time)
        end_time = str(end_time)
        if self.category == 'current':
            from_data = {
                "ctl00_Content_ajaxToolkitManager_HiddenField": "",
                '__EVENTTARGET': 'ctl00$Content$btnSearch',
                '__EVENTARGUMENT': '',
                '__VIEWSTATE': viewstate,
                '__VIEWSTATEGENERATOR': viewstategenerator,
                '__SCROLLPOSITIONX': 0,
                '__SCROLLPOSITIONY': scrollpositiony,
                '__EVENTVALIDATION': eventvalidation,
                'ctl00$Content$txtApplicationID$txtText': '',
                'ctl00$Content$txtDateFrom$txtText': start_time,
                'ctl00$Content$txtDateTo$txtText': end_time,
                'ctl00$Content$txtDescription$txtText': '',
                'ctl00$Content$ddlApplicationType$elbList': 'all',
                'ctl00$Content$ddlStatus$elbList': 'C',
                'ctl00$Content$ddlDecision$elbList': 'all',
                'ctl00$Content$txtStreetNoFrom$txtText': '',
                'ctl00$Content$txtStreetNoTo$txtText': '',
                'ctl00$Content$txtStreet$txtText': '',
                'ctl00$Content$txtStreetType$txtText': '',
                'ctl00$Content$txtSuburb$txtText': '',
                'ctl00$Content$cusFieldsAppInformation$PropertyElectorate$elbList': 'NotSelected'
            }
        else:
            from_data = {
                "ctl00_Content_ajaxToolkitManager_HiddenField": "",
                '__EVENTTARGET': 'ctl00$Content$btnSearch',
                '__EVENTARGUMENT': '',
                '__VIEWSTATE': viewstate,
                '__VIEWSTATEGENERATOR': viewstategenerator,
                '__SCROLLPOSITIONX': 0,
                '__SCROLLPOSITIONY': scrollpositiony,
                '__EVENTVALIDATION': eventvalidation,
                'ctl00$Content$txtApplicationID$txtText': '',
                'ctl00$Content$txtDateFrom$txtText': start_time,
                'ctl00$Content$txtDateTo$txtText': end_time,
                'ctl00$Content$txtDescription$txtText': '',
                'ctl00$Content$ddlApplicationType$elbList': 'all',
                'ctl00$Content$ddlStatus$elbList': 'P',
                'ctl00$Content$ddlDecision$elbList': 'all',
                'ctl00$Content$txtStreetNoFrom$txtText': '',
                'ctl00$Content$txtStreetNoTo$txtText': '',
                'ctl00$Content$txtStreet$txtText': '',
                'ctl00$Content$txtStreetType$txtText': '',
                'ctl00$Content$txtSuburb$txtText': '',
                'ctl00$Content$cusFieldsAppInformation$PropertyElectorate$elbList': 'NotSelected'
            }
        requests.post(search_url, headers=self.headers, data=from_data, cookies=cookiedict)
        print(cookiedict['ASP.NET_SessionId'])
        return cookiedict['ASP.NET_SessionId']

    """
    判断是否有搜索结果
    """

    def judge_serch_result(self, resp, start_time, end_time):
        main_page = BeautifulSoup(resp.text, "html.parser")
        validatorSummary = main_page.select_one("#ctl00_Header_h1PageTitle")
        if 'Error' in validatorSummary.get_text():
            print("None search results：" + start_time + "-----" + end_time)
            return False
        else:
            print("Exist search results：" + start_time + "-----" + end_time)
            return True

    """
    使用不同时间去请求搜索结果页面
    """

    def get_search_results_urllist(self, sessionID, start_time, end_time):
        cookie_dict = {'ASP.NET_SessionId': sessionID, }
        search_url = 'https://casey-web.t1cloud.com/T1PRDefault/WebApps/eProperty/P1/eTrack/eTrackApplicationSearchResults.aspx?r=P1.WEBGUEST&f=%24P1.ETR.RESULTS.VIW'
        resp = requests.get(search_url, headers=self.headers, cookies=cookie_dict)
        # print(resp.text)
        main_page = BeautifulSoup(resp.text, "html.parser")
        viewstate = main_page.select_one("#__VIEWSTATE")
        viewstate = viewstate.get('value')
        # print(viewstate)
        eventvalidation = main_page.select_one("#__EVENTVALIDATION")
        eventvalidation = eventvalidation.get('value')
        viewstategenerator = main_page.select_one("#__VIEWSTATEGENERATOR")
        viewstategenerator = viewstategenerator.get('value')
        # print(eventvalidation)
        search_result = self.judge_serch_result(resp, start_time, end_time)
        if search_result == True:
            app_number_list = self.find_app_number(resp.text)
            page_number = self.find_app_number_page(resp.text)
            for i in range(page_number + 1):
                if i == 0:
                    pass
                else:
                    if i == 1:
                        print(f"page 1:  ")
                        print(app_number_list)
                        result = self.get_details(app_number_list, cookie_dict)
                        for item in result:
                            yield item
                    else:
                        SCROLLPOSITIONY = int(random.randint(2500, 2800))
                        from_data = {
                            '__EVENTTARGET': 'ctl00$Content$cusResultsGrid$repWebGrid$ctl00$grdWebGridTabularView',
                            '__EVENTARGUMENT': f'Page${i}',
                            '__VIEWSTATE': viewstate,
                            '__VIEWSTATEGENERATOR': viewstategenerator,
                            '__SCROLLPOSITIONX': 0,
                            '__SCROLLPOSITIONY': SCROLLPOSITIONY,
                            '__EVENTVALIDATION': eventvalidation
                        }
                        resp = requests.post(search_url, headers=self.headers, data=from_data, cookies=cookie_dict)
                        app_number_list = self.find_app_number(resp.text)
                        print(f"page {i}:  ")
                        print(app_number_list)
                        result = self.get_details(app_number_list, cookie_dict)
                        for item in result:
                            yield item
        else:
            return None

    """
    获取搜索结果中的app_number
    return app_number_list
    """

    def find_app_number(self, resp):
        main_page = BeautifulSoup(resp, "html.parser")
        app_number_list = []
        try:
            app_numbers = main_page.select(".grid .normalRow a")
            for i in app_numbers:
                app_number_list.append(i.get_text())
            app_numbers = main_page.select(".grid .alternateRow a")
            for i in app_numbers:
                app_number_list.append(i.get_text())
            # print(app_number_list)
        except:
            print("error: function find_app_number")
        return app_number_list

    """
    获取搜索结果页码数
    return page number
    """

    def find_app_number_page(self, resp):
        # print(resp)
        main_page = BeautifulSoup(resp, "html.parser")
        page_number = 1
        try:
            app_numbers = main_page.select(".grid .pagerRow a")
            for i in app_numbers:
                page_number += 1
            print(f'page_number: {page_number}')
            return page_number
        except:
            return 1

    """ 
    请求详情页
    """

    def get_details(self, all_app_number, cookie_dict):
        for i in all_app_number:
            print(f'get_details: {i}')
            url = f'https://casey-web.t1cloud.com/T1PRDefault/WebApps/eProperty/P1/eTrack/eTrackApplicationDetails.aspx?r=P1.WEBGUEST&f=%24P1.ETR.APPDET.VIW&ApplicationId={i}'
            yield Request(url=url, method="GET", cookies=cookie_dict, callback=self.parse_detail)

    """ 
    根据请求的日期获取一个新的cookie sessionID
    """

    def get_new_sessionID(self, response):
        print(self.cookies)
        print("post请求cookie已注册")
        search_result_url = 'https://casey-web.t1cloud.com/T1PRDefault/WebApps/eProperty/P1/eTrack/eTrackApplicationSearchResults.aspx?r=P1.WEBGUEST&f=%24P1.ETR.RESULTS.VIW'
        yield Request(url=search_result_url, method="GET", headers=self.headers, callback=self.deal_search_result)

    """
    处理搜索结果页面
    """

    def deal_search_result(self, response):
        print(response.text)

    """
    详情页取内容
    """

    def parse_detail(self, response):
        # print(response.text)
        item = CaseyItem()
        main_page = BeautifulSoup(response.text, "html.parser")
        tbleft = main_page.select(".grid td")
        temp = ''
        PropertyAddress = ''
        LandDescription = ''
        print('=====================')
        for i in tbleft:
            if temp == '':
                if i.get_text() == "Application Number":
                    temp = i.get_text()
                elif i.get_text() == "Estate Name":
                    temp = i.get_text()
                elif i.get_text() == "Proposal Description":
                    temp = i.get_text()
                elif i.get_text() == "Lodgement Date":
                    temp = i.get_text()
                elif i.get_text() == "Estimated Value":
                    temp = i.get_text()
                elif i.get_text() == "Status":
                    temp = i.get_text()
                elif i.get_text() == "Further Info Requested Date":
                    temp = i.get_text()
                elif i.get_text() == "Further Info Received Date":
                    temp = i.get_text()
                elif i.get_text() == "Advertising Commencement":
                    temp = i.get_text()
                elif i.get_text() == "Advertising Completion":
                    temp = i.get_text()
                elif i.get_text() == "No of Objections":
                    temp = i.get_text()
                elif i.get_text() == "Responsible Authority Outcome":
                    temp = i.get_text()
                elif i.get_text() == "Final Outcome":
                    temp = i.get_text()
                elif i.get_text() == "Final Outcome Date":
                    temp = i.get_text()
                elif i.get_text() == "VCAT Lodged Date":
                    temp = i.get_text()
                elif i.get_text() == "System Status":
                    temp = i.get_text()
                elif i.get_text() == "Version Lodged Date":
                    temp = i.get_text()
                elif i.get_text() == "Permit Ext Start Date":
                    temp = i.get_text()
                elif i.get_text() == "Permit Ext End Date":
                    temp = i.get_text()
                elif i.get_text() == "Property Address":
                    temp = i.get_text()
                elif i.get_text() == "Land Description":
                    temp = i.get_text()
                elif i.get_text() == "Ward":
                    item["property_address"] = PropertyAddress
                    item["land_description"] = LandDescription
                    break
            else:
                if temp == "Application Number":
                    # print(temp)
                    print(i.get_text())
                    item["app_number"] = i.get_text().strip()
                    temp = ''
                elif temp == "Estate Name":
                    # print(temp)
                    # print(i.get_text().strip())
                    item["estate_name"] = i.get_text().strip()
                    temp = ''
                elif temp == "Proposal Description":
                    # print(temp)
                    # print(i.get_text().strip())
                    item["description"] = i.get_text().strip()
                    temp = ''
                elif temp == "Lodgement Date":
                    try:
                        lodged_date = i.get_text().strip()
                        time_array = time.strptime(lodged_date, '%d/%m/%Y')
                        temp_data = int(time.mktime(time_array))
                        item["lodged"] = temp_data if lodged_date else 0
                    except:
                        item["lodged"]=0
                    temp = ''
                elif temp == "Estimated Value":
                    # print(temp)
                    # print(i.get_text())
                    item["estimated_value"] = i.get_text().strip()
                    temp = ''
                elif temp == "Status":
                    # print(temp)
                    # print(i.get_text())
                    item["status"] = i.get_text().strip()
                    temp = ''
                elif temp == "Further Info Requested Date":
                    try:
                        lodged_date = i.get_text().strip()
                        time_array = time.strptime(lodged_date, '%d/%m/%Y')
                        temp_data = int(time.mktime(time_array))
                        item["further_info_requested_date"] = temp_data if lodged_date else 0
                    except:
                        item["further_info_requested_date"]=0
                    temp = ''
                elif temp == "Further Info Received Date":
                    try:
                        lodged_date = i.get_text().strip()
                        time_array = time.strptime(lodged_date, '%d/%m/%Y')
                        temp_data = int(time.mktime(time_array))
                        item["further_info_received_date"] = temp_data if lodged_date else 0
                    except:
                        item["further_info_received_date"]=0
                    temp = ''
                elif temp == "Advertising Commencement":
                    # print(temp)
                    # print(i.get_text())
                    item["advertising_commencement"] = i.get_text().strip()
                    temp = ''
                elif temp == "Advertising Completion":
              
                    item["advertising_completion"] = i.get_text().strip()
                    temp = ''
                elif temp == "No of Objections":
                    # print(temp)
                    # print(i.get_text())
                    item["no_of_objections"] = i.get_text().strip()
                    temp = ''
                elif temp == "Responsible Authority Outcome":
                    # print(temp)
                    # print(i.get_text())
                    item["responsible_authority_outcome"] = i.get_text().strip()
                    temp = ''
                elif i.get_text() == "Final Outcome":
                    # print(temp)
                    # print(i.get_text())
                    item["final_outcome"] = i.get_text().strip()
                    temp = ''
                elif temp == "Final Outcome Date":
                    try:
                        lodged_date = i.get_text().strip()
                        time_array = time.strptime(lodged_date, '%d/%m/%Y')
                        temp_data = int(time.mktime(time_array))
                        item["final_outcome_date"] = temp_data if lodged_date else 0
                    except:
                        item["final_outcome_date"] =0
                    temp = ''
                elif temp == "VCAT Lodged Date":
                    try:
                        lodged_date = i.get_text().strip()
                        time_array = time.strptime(lodged_date, '%d/%m/%Y')
                        temp_data = int(time.mktime(time_array))
                        item["vcat_lodged_date"] = temp_data if lodged_date else 0
                    except:
                        item["vcat_lodged_date"] = 0
                    temp = ''

                elif i.get_text() == "System Status":
                    # print(temp)
                    # print(i.get_text())
                    item["system_status"] = i.get_text().strip()
                    temp = ''
                elif temp == "Version Lodged Date":
                    try:
                        lodged_date = i.get_text().strip()
                        time_array = time.strptime(lodged_date, '%d/%m/%Y')
                        temp_data = int(time.mktime(time_array))
                        item["versio_lodged_date"] = temp_data if lodged_date else 0
                    except:
                        item["versio_lodged_date"] = 0
                    temp = ''

                elif temp == "Permit Ext Start Date":
                    try:
                        lodged_date = i.get_text().strip()
                        time_array = time.strptime(lodged_date, '%d/%m/%Y')
                        temp_data = int(time.mktime(time_array))
                        item["permit_ext_start_date"] = temp_data if lodged_date else 0
                    except:
                        item["permit_ext_start_date"] = 0
                    temp = ''
                elif temp == "Permit Ext End Date":
                    try:
                        lodged_date = i.get_text().strip()
                        time_array = time.strptime(lodged_date, '%d/%m/%Y')
                        temp_data = int(time.mktime(time_array))
                        item["permit_ext_end_date"] = temp_data if lodged_date else 0
                    except:
                        item["permit_ext_end_date"] = 0
                    temp = ''
                elif temp == "Property Address":
                    # print(temp)
                    # print(i.get_text())
                    PropertyAddress += i.get_text().strip() + ';'
                    temp = ''
                elif temp == "Land Description":
                    # print(temp)
                    # print(i.get_text())
                    temp = ''
                    LandDescription += i.get_text().strip() + ';'
                elif temp == 'Ward':
                    break

        item['metadata']={}
        del item['metadata']
        yield item
