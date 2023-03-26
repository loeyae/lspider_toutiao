# -*- coding: utf-8 -*-
# Licensed under the Apache License, Version 2.0 (the "License"),
# see LICENSE for more details: http://www.apache.org/licenses/LICENSE-2.0.

__author__ = "Zhang Yi <loeyae@gmail.com>"
__date__ = "$2019-2-19 9:16:07$"

from setuptools import setup, find_packages

setup(
    name="cdspider_toutiao",
    version="0.1.1",
    description="数据采集框架头条采集",
    author='Zhang Yi',
    author_email='loeyae@gmail.com',
    license="Apache License, Version 2.0",
    url="https://github.com/loeyae/lspider_toutiao.git",
    install_requires=[
        'cdspider>=0.1.4',
        'cdspider_wemedia>=0.1.1',
    ],
    packages=find_packages(),

    entry_points={
        'cdspider.handler': [
            'toutiao-list=cdspider_toutiao.handler:ToutiaoListHandler',
        ]
    }
)
