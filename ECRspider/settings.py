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
TMALL_COOKIES = "l=ArW1blTT7/MyUPxFDUg4cU5BRTtslmk5; cna=TNDuEJujAC8CAST7GReO/QDK; csg=2db8643f; OZ_SI_2061=sTime=1517661159&sIndex=21; OZ_1U_2061=vid=va75abe8857307.0&ctime=1517759965&ltime=1517661221; OZ_1Y_2061=erefer=https%3A//s.taobao.com/search%3Fq%3D%25E7%2594%25B7%25E5%25A4%2596%25E5%25A5%2597+%25E4%25BC%2598%25E8%25A1%25A3%25E5%25BA%2593%26imgfile%3D%26js%3D1%26stats_click%3Dsearch_radio_all%253A1%26initiative_id%3Dstaobaoz_20180203%26ie%3Dutf8&eurl=https%3A//detail.tmall.com/item.htm%3Fspm%3Da230r.1.14.16.1cc671e9L2uKaf%26id%3D561988679314%26ns%3D1%26abbucket%3D15&etime=1517661221&ctime=1517759965&ltime=1517661221&compid=2061; hng=CN%7Czh-CN%7CCNY%7C156; uc1=cookie14=UoTdfDEl4JIjlg%3D%3D&lng=zh_CN&cookie16=UIHiLt3xCS3yM2h4eKHS9lpEOw%3D%3D&existShop=true&cookie21=VFC%2FuZ9ajCNfDyoh%2FQeWRQ%3D%3D&tag=8&cookie15=V32FPkk%2Fw0dUvg%3D%3D&pas=0; uc3=sg2=V37kWFknXBxaZr9JnMbtm7t24ADUFEOsuBnT6vNhQig%3D&nk2=GcAxdWUv0%2B%2F5%2BfHsuf0%3D&id2=VAYrG49eenc%3D&vt3=F8dBz4bQQ0W7g31kE1Y%3D&lg2=UtASsssmOIJ0bQ%3D%3D; tracknick=zhangliangdian; _l_g_=Ug%3D%3D; ck1=; unb=77305330; lgc=zhangliangdian; cookie1=BqqhBNXWMkhjhhOD1Al7cPrsDdCxkwOFao6%2FDp1ICy4%3D; login=true; cookie17=VAYrG49eenc%3D; cookie2=1a2b0b41b1828b963f7f9596740cb433; _nk_=zhangliangdian; t=66bbe08ae7c82c3656cf01549d1688b2; uss=; skt=4ae76607686dec59; _tb_token_=ef3be5bad36bb; ubn=p; ucn=center; isg=BM7OkzwrGE7hn6526D3UcIp6H6RQ55MvfYGh7PgXMVGMW261YN_iWXQdl4c3w4ph"


TAOBAO_COOKIES = "miid=971779310573469703; UM_distinctid=15bb022018b11-0e846e8e5ef731-414a0229-100200-15bb022018c114; l=AldXdySp3Iwxot6vM3a643JeZ8Ghkyv-; hng=CN%7Czh-CN%7CCNY%7C156; thw=cn; v=0; _tb_token_=ee8313e6efa78; ubn=p; uc1=cookie14=UoTcCijX27kZOw%3D%3D&lng=zh_CN&cookie16=URm48syIJ1yk0MX2J7mAAEhTuw%3D%3D&existShop=true&cookie21=WqG3DMC9Ed9Ujk%2B1SA%2FENQ%3D%3D&tag=8&cookie15=U%2BGCWk%2F75gdr5Q%3D%3D&pas=0; uc3=sg2=V37kWFknXBxaZr9JnMbtm7t24ADUFEOsuBnT6vNhQig%3D&nk2=GcAxdWUv0%2B%2F5%2BfHsuf0%3D&id2=VAYrG49eenc%3D&vt3=F8dBzWfePunTLBi3qro%3D&lg2=V32FPkk%2Fw0dUvg%3D%3D; existShop=MTUwNTM1MzE0Nw%3D%3D; lgc=zhangliangdian; tracknick=zhangliangdian; cookie2=1f5dfbcb3fe48bb2f75c50b49154733b; sg=n05; mt=np=&ci=-1_1; cookie1=BqqhBNXWMkhjhhOD1Al7cPrsDdCxkwOFao6%2FDp1ICy4%3D; unb=77305330; skt=d7709c62bed9a91f; t=66bbe08ae7c82c3656cf01549d1688b2; _cc_=WqG3DMC9EA%3D%3D; tg=0; _l_g_=Ug%3D%3D; _nk_=zhangliangdian; cookie17=VAYrG49eenc%3D; cna=TNDuEJujAC8CAST7GReO/QDK; isg=AoSEcX8rgc7HcDTQjq9-DvQIVQLaiZoPs1Pbip4lEc8SySSTxq14l7pvfW7K"


JD_COOKIES = "sc_t=2; DeviceId=897875680be34c7391b4b13a0747d14b; DeviceSeq=34a17f054a1f450f85077ba21634de8c; ipLocation=%u5317%u4EAC; ipLoc-djd=1-72-2799-0; user-key=b490b69f-d85a-4210-8420-2d0b031ce646; cn=0; __jdv=122270672|direct|-|none|-|1516583766993; PCSYCityID=1303; qr_t=c; alc=VCRUAjevVMvYosgm95/aOA==; _t=nzd7dUM1+7bhHsHZqZ1HR27HcVb0l1fVbBjn41wxuuc=; wlfstk_smdl=yw7l16kn9jwao66uht5z78a95elxxjfw; _jrda=3; _jrdb=1517761903521; login_c=1; mp=13615025898; TrackID=1aoaaJfDausb29TrKVakNh2BHurWGP_GZ23FgIkfK-qxYKU1iIu4R0dt2Q0szzFp52KjSQDsQ95x5mfg6tciUgrkVv5XRuy1k3in2DDnpN6o; pinId=f9ISTL07P4DHrNnP9Iig-g; pin=zhangliangdian; unick=zhangliangdian; thor=276D517A3DEEF2D76321BE99A893E234328B12BA21EC961A7598B2D16E2A2555AF4D2AE8D5969DE2E749C45ED61ECF98E4EC66007E0CDBF95FD00CEB20247DD272A8A57AAF32C27462761EED1AB930B9F7B55F3BD58F58D2C3982DAE822E3BF4E20C554C52AB1DB868DEE8759C2BDEC5154968DFED7B71DD5693A1CD998FA05E28619DA1FF26DCFC5CA160F4BECA6C76; ol=1; _tp=Q3laENvB%2B863wmebIQ1ecA%3D%3D; _pst=zhangliangdian; ceshi3.com=201; __jda=122270672.15149059540401105026100.1514905954.1517282238.1517761900.7; __jdb=122270672.5.15149059540401105026100|7.1517761900; __jdc=122270672; __jdu=15149059540401105026100; 3AB9D23F7A4B3C9B=S4OELVHASYI52NXXD4D6N7IAUBPZJ5XLG63N67VMHGCXMPVBLFBEJVLRKOAD77O6T2TD7PAOULJUQXIGRF6IEMDRUU"



























































