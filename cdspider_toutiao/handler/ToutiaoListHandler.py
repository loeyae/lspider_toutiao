#-*- coding: utf-8 -*-
# Licensed under the Apache License, Version 2.0 (the "License"),
# see LICENSE for more details: http://www.apache.org/licenses/LICENSE-2.0.

"""
:author:  Zhang Yi <loeyae@gmail.com>
:date:    2018-11-21 20:45:56
"""
import copy
import time
from cdspider_wemedia.handler import WemediaListHandler
from cdspider.database.base import *
from cdspider.libs.constants import *
from cdspider.parser import ListParser, CustomParser
from cdspider.libs import utils
from cdspider.parser.lib import TimeParser

class ToutiaoListHandler(WemediaListHandler):
    """
    general list handler
    :property task 爬虫任务信息 {"mode": "list", "uuid": SpiderTask.list uuid}
                   当测试该handler，数据应为 {"mode": "list", "url": url, "listRule": 列表规则，参考列表规则}
    """

    TAB_ARTICLE = 'article'
    TAB_VIDEO = 'video'
    TAB_TOUTIAO = 'toutiao'
    MAX_RETRY = 10
    EXPIRE = 7200

    LIST_URL = 'https://www.toutiao.com/pgc/ma/?page_type=1&max_behot_time={max_behot_time}&uid={uid}&media_id={mediaId}&output=json&is_json=1&count=20&from=user_profile_app&version=2&as={as}&cp={cp}&callback=jsonp4'
    VIDEO_URL = 'https://www.toutiao.com/pgc/ma/?page_type=0&max_behot_time={max_behot_time}&uid={uid}&media_id={mediaId}&output=json&is_json=1&count=20&from=user_profile_app&version=2&as={as}&cp={cp}&callback=jsonp4'
    TOUTIAO_URL = 'https://www.toutiao.com/api/pc/feed/?category=pc_profile_ugc&utm_source=toutiao&visit_user_id={uid}&max_behot_time={max_behot_time}'

    def prepare(self, save):
        super(ToutiaoListHandler, self).prepare(save)
        uid = save['request']['hard_code'][0]['value']
        if not 'save' in self.task or not self.task['save']:
            self.task['save'] = {}
        ctime = self.task['save'].get('timestamp', 0)
        if not self.task['save'].get('honey') or not self.task['save'].get('mediaId') or self.crawl_id - int(ctime) > self.EXPIRE:
            crawler = self.get_crawler({"crawler": "selenium", "method": "open", "proxy": "never"})
            request_params = copy.deepcopy(self.request_params)
            request_params['method'] = 'open'
            crawler.crawl(**request_params)
            getHoneyjs='return (ascp.getHoney())'
            honey = dict(crawler._driver.execute_script(getHoneyjs))
    #        _signatureJs='return TAC.sign('+ uid +')'
    #        self.debug("%s sign js: %s" % (self.__class__.__name__, _signatureJs))
    #        _signature = crawler._driver.execute_script(_signatureJs)
    #        save['_signature'] = _signature
            mediaIdJs = 'return userInfo.mediaId'
            mediaId = crawler._driver.execute_script(mediaIdJs)
            self.task['save']['mediaId'] = mediaId
            self.task['save']['honey'] = honey
            del crawler
#        self.request_params['url'] = 'https://www.toutiao.com/c/user/article/?page_type=1&user_id=' + uid + '&max_behot_time=0&count=20&as='+ honey['as'] +'&cp='+ honey['cp'] +'&_signature='+ _signature
        self.request_params['url'] = utils.format_(self.task['url'], {"uid": uid, "mediaId": self.task['save']['mediaId'], "max_behot_time": 0, "as": self.task['save']['honey']['as'], "cp": self.task['save']['honey']['cp']})
        save['base_url'] = self.request_params['url']
        self.request_params['headers'] = {'Host': 'www.toutiao.com'}

#    def on_next(self, save):
#        """
#        下一页解析
        #"""
#        if self.page > 10:
#            raise  CDSpiderCrawlerMoreThanMaximum()
#        self.page += 1
#        tab = self.task.get('save', {}).get('tab', self.TAB_ARTICLE)
#        rule = {
#            "has_more": {
#                "filter": "@json:has_more"
#            },
#            "max_behot_time": {
#                "filter": "@json:next.max_behot_time"
#            }
#        }
#        parser = CustomParser(source=self.response['last_source'], ruleset=rule, log_level=self.log_level, url=self.response['final_url'])
#        parsed = parser.parse()
#        if 'has_more' in parsed and parsed['has_more'] == '1':
#            uid = save['request']['hard_code'][0]['value']
#            if tab == self.TAB_VIDEO:
#                save['next_url'] = self.request_params['url'] = self.VIDEO_URL.format(uid=uid, mediaId=self.task['save']['mediaId'], max_behot_time=parsed['max_behot_time'], **self.task['save']['honey'])
#            elif tab == self.TAB_TOUTIAO:
#                save['next_url'] = self.request_params['url'] = self.TOUTIAO_URL.format(uid=uid, mediaId=self.task['save']['mediaId'], max_behot_time=parsed['max_behot_time'])
#            else:
#                save['next_url'] = self.request_params['url'] = self.LIST_URL.format(uid=uid, mediaId=self.task['save']['mediaId'], max_behot_time=parsed['max_behot_time'], **self.task['save']['honey'])
#        else:
#            raise CDSpiderCrawlerNoNextPage(base_url=save.get("base_url", ''), current_url=save.get('request_url'))
