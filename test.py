# -*- coding: utf-8 -*-
import requests
from lxml import etree

if __name__ == '__main__':
    lxml = requests.get("https://weibo.com/p/aj/album/loading?ajwvr=6&type=like&owner_uid=3583824010&viewer_uid=5337887050&page=2&page_id=1005053583824010&ajax_call=1&__rnd=1560915553987", cookies = {
        "Cookie": "ALF=1563504539; SCF=AvFcHra0tEMGlbvZdXLvJ2Wn4NQdR305ku3AtzKgo5OWUuRTOVKfkvHy80vG9QXWsOVpIaACVemnZ3xOfuGf4pI.; SUB=_2A25wDdKBDeRhGeNN6FUZ-CnMzjyIHXVT8f7JrDV6PUJbktAKLUHWkW1NSbRi0iIETWzk0wr_nyg91pMCdKSSCnzY; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WW7gDDG6IBdJJuSk_Mrf-AV5JpX5K-hUgL.Fo-0e0MR1hM7SK52dJLoI7yNqPxyMcLkd5tt; SUHB=0vJYNju_fK5Gec; SSOLoginState=1560912594; MLOGIN=1; _T_WM=37451492514; WEIBOCN_FROM=1110006030; M_WEIBOCN_PARAMS=luicode%3D20000174%26uicode%3D20000174"
    }).content
    # body = etree.HTML(lxml)
    data = eval(lxml)
    print(data['data'])
