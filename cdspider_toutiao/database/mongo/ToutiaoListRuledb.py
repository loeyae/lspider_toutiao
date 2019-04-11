#-*- coding: utf-8 -*-

# Licensed under the Apache License, Version 2.0 (the "License"),
# see LICENSE for more details: http://www.apache.org/licenses/LICENSE-2.0.

"""
:author:  Zhang Yi <loeyae@gmail.com>
:date:    2018-1-9 21:30:20
:version: SVN: $Id: Resultdb.py 2338 2018-07-08 05:58:24Z zhangyi $
"""
import time
from cdspider_toutiao.database.base import ToutiaoListRuleDB as BaseToutiaoListRuleDB
from cdspider.database.mongo.Mongo import Mongo, SplitTableMixin

class ToutiaoListRuleDB(Mongo, BaseToutiaoListRuleDB, SplitTableMixin):

    __tablename__ = 'toutiao_list_rule'

    incr_key = 'toutiao_list_rule'

    def __init__(self, connector, table=None, **kwargs):
        super(ToutiaoListRuleDB, self).__init__(connector, table = table, **kwargs)
        self._check_collection()

    def insert(self, obj = {}):
        obj.setdefault("ctime", int(time.time()))
        obj['uuid'] = self._get_increment(self.incr_key)
        super(ToutiaoListRuleDB, self).insert(setting=obj)
        return obj['uuid']

    def update(self, id, obj = {}):
        obj['utime'] = int(time.time())
        return super(ToutiaoListRuleDB, self).update(setting=obj, where={"uuid": id})

    def get_detail(self, id, select=None):
        return self.get(where={"uuid": id}, select=select)

    def get_list(self, where = {}, select = None, **kwargs):
        kwargs.setdefault('sort', [('uuid', 1)])
        return self.find(where=where, select=select, **kwargs)

    def get_count(self, where = {}, select = None, **kwargs):
        return self.count(where=where, select=select, **kwargs)

    def _check_collection(self):
        self._list_collection()
        suffix = time.strftime("%Y%m")
        name = super(ToutiaoListRuleDB, self)._collection_name(suffix)
        if not name in self._collections:
            self._create_collection(name)

    def _create_collection(self, table):
        collection = self._db.get_collection(table)
        indexes = collection.index_information()
        if not 'uuid' in indexes:
            collection.create_index('rid', unique=True, name='rid')
        if not 'status' in indexes:
            collection.create_index('status', name='status')
        if not 'ctime' in indexes:
            collection.create_index('ctime', name='ctime')
        self._collections.add(table)
