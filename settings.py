# -*- coding: utf-8 -*-

# Scrapy settings for ECRspider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'ECRspider'

SPIDER_MODULES = ['ECRspider.spiders']
NEWSPIDER_MODULE = 'ECRspider.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'ECRspider (+http://www
USER_AGENT = 'MMozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'

REDIRECT_ENABLED = False

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 3
# DEPTH_LIMIT = 2

# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# -----------------
# LOG等级指定，默认是'DEBUG',抓取的时候每个item获取的内容都会被输出
LOG_LEVEL = 'WARNING'

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    'accept': '*/*',
    'accept-encoding': 'gzip, deflate, sdch',
    'accept-language': 'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4',
    'Connection': 'keep-alive',
    'User-Agent': 'MMozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
    # 'referer': 'https://list.tmall.com/search_product.htm?&q=%CA%D5%D2%F8%BB%FA&sort=d&style=g'
    # 'referer': 'https://www.baidu.com'
}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'ECRspider.middlewares.EcrspiderSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'ECRspider.middlewares.MyCustomDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html


# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'


# ------------------------------------------------ 数据库配置信息 ------------------------------------------
# ------- MongoDB ----------------
MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
MONGODB_DBNAME = 'ECR_OnlineStore'
TMALL_MONGODB_DOCNAME = 'Tmall'
TAOBAO_MONGODB_DOCNAME = 'Taobao'
JD_MONGODB_DOCNAME = 'JD'
Neg_MONGODB_DOCNAME = 'NegativeReviews'
Pos_MONGODB_DOCNAME = 'PositiveRevies'

# ------------------------------------------------ 配置cookies ---------------------------------------------
# 先用账号登录对应网站，然后将其cookie复制下来；注意cookie是有时限的，如果被Ban，请重新登录，更换cookie
# Disable cookies (enabled by default)
COOKIES_ENABLED = True
TMALL_COOKIES = "l=AqamBNkOsVN0kzXwdCAV9mzZdhIp--pE; cna=CzEPELw5vV8CATs8BAFWDLTM; tk_trace=1; hng=; uc1=cookie14=UoTde95ytHr7PA%3D%3D&lng=zh_CN&cookie16=WqG3DMC9UpAPBHGz5QBErFxlCA%3D%3D&existShop=false&cookie21=Vq8l%2BKCLiYYu&tag=8&cookie15=V32FPkk%2Fw0dUvg%3D%3D&pas=0; uc3=sg2=VAEMDmcmJM%2FJvU6T0NEFGNma4Wn6tMB9jo4YrkIsYFQ%3D&nk2=symkLBaCnbDezrL8MP2K5Q%3D%3D&id2=UNQySk1K9%2FKjHQ%3D%3D&vt3=F8dBzLOVV2v%2BMY3LG88%3D&lg2=UIHiLt3xD8xYTw%3D%3D; tracknick=%5Cu5C0F%5Cu732A%5Cu4F69%5Cu5947peggy004; _l_g_=Ug%3D%3D; ck1=; unb=3458027292; lgc=%5Cu5C0F%5Cu732A%5Cu4F69%5Cu5947peggy004; cookie1=VW6%2Fe91k6k%2FAPcturenj1DlMR5xzcKCXrlA0ewEzcGA%3D; login=true; cookie17=UNQySk1K9%2FKjHQ%3D%3D; cookie2=1726483d88152d68a8bafc418fd72214; _nk_=%5Cu5C0F%5Cu732A%5Cu4F69%5Cu5947peggy004; t=ad501519a5f02e5286d1d04e57dc40c5; uss=BvHWbrKZk7WjzlCqnGvbVsZAa4uhhl80ZeQTFfPX9jbAEwxdpFsYRGQ%2FHQ%3D%3D; skt=21e3fe019d6eb640; _tb_token_=33be33ba6387e; ctoken=8ZyMk9MCFWHhgqIebNzViceland; _m_h5_tk=12e21345aeea6f082a4c3ce711f70779_1510817218502; _m_h5_tk_enc=2278035251940b9edfc16ce026c44b80; sm4=350100; isg=AgoK6mMJZEiHRusy0G5fw9RyW_AA750Rexq2ZpRCJd3oR6sBfYoXZG35I7ZU"


TAOBAO_COOKIES = "miid=971779310573469703; UM_distinctid=15bb022018b11-0e846e8e5ef731-414a0229-100200-15bb022018c114; l=AldXdySp3Iwxot6vM3a643JeZ8Ghkyv-; hng=CN%7Czh-CN%7CCNY%7C156; thw=cn; v=0; _tb_token_=ee8313e6efa78; ubn=p; uc1=cookie14=UoTcCijX27kZOw%3D%3D&lng=zh_CN&cookie16=URm48syIJ1yk0MX2J7mAAEhTuw%3D%3D&existShop=true&cookie21=WqG3DMC9Ed9Ujk%2B1SA%2FENQ%3D%3D&tag=8&cookie15=U%2BGCWk%2F75gdr5Q%3D%3D&pas=0; uc3=sg2=V37kWFknXBxaZr9JnMbtm7t24ADUFEOsuBnT6vNhQig%3D&nk2=GcAxdWUv0%2B%2F5%2BfHsuf0%3D&id2=VAYrG49eenc%3D&vt3=F8dBzWfePunTLBi3qro%3D&lg2=V32FPkk%2Fw0dUvg%3D%3D; existShop=MTUwNTM1MzE0Nw%3D%3D; lgc=zhangliangdian; tracknick=zhangliangdian; cookie2=1f5dfbcb3fe48bb2f75c50b49154733b; sg=n05; mt=np=&ci=-1_1; cookie1=BqqhBNXWMkhjhhOD1Al7cPrsDdCxkwOFao6%2FDp1ICy4%3D; unb=77305330; skt=d7709c62bed9a91f; t=66bbe08ae7c82c3656cf01549d1688b2; _cc_=WqG3DMC9EA%3D%3D; tg=0; _l_g_=Ug%3D%3D; _nk_=zhangliangdian; cookie17=VAYrG49eenc%3D; cna=TNDuEJujAC8CAST7GReO/QDK; isg=AoSEcX8rgc7HcDTQjq9-DvQIVQLaiZoPs1Pbip4lEc8SySSTxq14l7pvfW7K"


JD_COOKIES = "TrackID=1xpuJQb4Hndy6jWyBgLQQs28t2OWxQ4B8TKasUE93eue2ZX368lG0llQSxBNlAMPVv4-01bR5tveCs7as0YwW3SbspmWmsR4TLN05F2kYdPE; pinId=V-ByV_rOkZP-MVWBqe2b5D_Lll-QKRdB; pin=%E5%B0%8F%E7%8C%AA%E4%BD%A9%E5%A5%87peggy004; unick=%E5%B0%8F%E7%8C%AA%E4%BD%A9%E5%A5%87peggy004; _tp=GL3RtBxDW%2BH0pTrwBBQSxklURDs96s7iCnPycEqkPGuBtqBl2YKVwtbSu4t6S1YF; _pst=%E5%B0%8F%E7%8C%AA%E4%BD%A9%E5%A5%87peggy004; ipLoc-djd=1-72-4137-0; areaId=1; __jdv=122270672|direct|-|none|-|1510820369123; __jda=122270672.1904477311.1505720613.1509343208.1510820369.6; __jdb=122270672.2.1904477311|6.1510820369; __jdc=122270672; user-key=accbb3a1-0e27-44a6-8c72-cdfa9a08516e; cn=0; __jdu=1904477311; 3AB9D23F7A4B3C9B=U4OX47SQGXWQ4HJOVPSCPRFXSQQW7HSEMMATE4CMPDPPU4DBJDHR33NWL4BJBH6HXKBDORRWHAHCDYDIU6HTTCJRBE"









































