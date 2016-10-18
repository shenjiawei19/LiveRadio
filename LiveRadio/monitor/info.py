# -*- coding: utf-8 -*-
import requests
from HTMLParser import HTMLParser
import sys



def _attr(attrs, name):
    for attr in attrs:
        if attr[0] == name:
            return attr[1]
    return None


class PoemParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.line = 0
        self.produce = False


    def handle_starttag(self, tag, attr):

        if tag == 'td' :
            self.produce = True


    def handle_data(self, data):
        '''
        一月：January
        二月：February
        三月：March
        四月：April
        五月：May
        六月：June
        七月：July
        八月：August
        九月：September
        十月：October
        十一月：November
        十二月：December
        '''
        if self.produce :
            self.line = self.line + 1
            if self.line > 1 and self.line < 4:
                info = data.strip().split(' ')
                if info[0] == 'January':
                    month = '01'
                elif info[0] == 'February':
                    month = '02'
                elif info[0] == 'March':
                    month = '02'
                elif info[0] == 'April':
                    month = '03'
                elif info[0] == 'May':
                    month = '04'
                elif info[0] == 'June':
                    month = '05'
                elif info[0] == 'July':
                    month = '06'
                elif info[0] == 'August':
                    month = '07'
                elif info[0] == 'September':
                    month = '08'
                elif info[0] == 'October':
                    month = '09'
                elif info[0] == 'November':
                    month = '10'
                elif info[0] == 'December':
                    month = '11'
                date = info[2]+'-'+month+'-'+info[1][:2]
                date = '"' + date + '",'
                print date,

    def handle_endtag(self, tag):
        if tag == 'td':
            self.produce = False


def get_info(file):
    for n in file:
        line = n.split(' ')
        ip = '"'+line[0]+'",'
        print ip,
        size =  line[1][:-2]
        url = 'http://www.dell.com/support/home/en/en/cnbsd1/product-support/servicetag/'+line[1][:-2]+'/warranty/'
        yield url


def get_date(urls):
    cok = {'Cookie':'X-Akamai-FEO-Browser-State=RV; s_vi=[CS]v1|2BE74ADF052AB186-40000300600199A6[CE]; AMCV_4DD80861515CAB990A490D45%40AdobeOrg=1999109931%7CMCIDTS%7C17051%7CMCMID%7C82451005222353167524536139373804168510%7CMCAAMLH-1473761341%7C11%7CMCAAMB-1473761342%7CNRX38WO0n5BH8Th-nqAG_A%7CMCAID%7C2BE74ADF052AB186-40000300600199A6; tntSTPdevice=desktop; tntDemand=RGVsbEluZHVzdHJ5PSB8IEluZHVzdHJ5PSB8IFN1Yl9JbmR1c3RyeT0gfCBjb21wYW55TmFtZT0gfCBlbXBDb3VudD0%3D; GAAnon=90c0ba38-ff57-4b49-b86c-e9294ebd16b0; StormPCookie=bandwidth=NA&js=1; SITESERVER=ID=3a71c7a6babc492094d4acaae203b243; IPERCEPTIONS_NextGen=0; rumCki=false; sessionTime=Wed%20Sep%2007%202016%2011%3A36%3A17%20GMT%2B0800%20%28CST%29; eds=rfgdobplhcp3tlrniym1pbtq; ASP.NET_SessionId=errlzri1jwgxolvho1fsyqe2; IPE_S_NextGen=0; s_channelstack=%5B%5B%27Direct%2520Load%27%2C%271473156543131%27%5D%2C%5B%27Direct%2520Load%27%2C%271473213476678%27%5D%2C%5B%27Direct%2520Load%27%2C%271473217484622%27%5D%2C%5B%27Direct%2520Load%27%2C%271473226729778%27%5D%5D; s_vnum=1504692543137%26vn%3D4; lvs=th%3Dbrowse-consumer; DaisContext=B84eZTyLt3tBG2zs8ks40I/jTlTEgbnXTjNJELCqZ2WO1P715byGVg==; GAAuth=drwyIpfYEqtjYjtg9AVe5966DoGqHMLSDlWUGXT5eOFH6B5KaTJhb2cpw6NB4U0UtYwLMQoXDrYfgih2oYQALqzGS6SAHkIMIhc4Zg8rCtSRu0Uejl7T1WYJtt0lMOJkJGLKEntgl+zlnSxZU5Hq6jyDwf7+qkacgdxKN2bsNlyuCcXPllGpPF1oit/+utgHIKC13JYasrtzeW8iEv6jQZrUCCEuNH15ix8KKFBOB+MOOiFvfoFFNZy9d1yDrcFWHHsMR2bpqPQnAL7+BoUPAz+3lC0Ye+/uExdzdzPCXRtjb7Yefz6mpXksX20a89g6vAtnNuxdTdzaaxP++1HPEJbGxNFYTCVIUbG0h+7xH9SmmSGmmSlDy/LIyvr+r1uj2MTzFDr4lVP4MTtYKQrFACqLFulpElt57zvKb/AtWEFfWFBmd9DPiA==; dais-c=NHzo9NJnZslV6ebfp/6FZ1uCULmESMuOMRBvGt5YTt0t6banyjPdbAKQbwTenVGFAebLaJlGu15NIqr2nyQZlexqWSTZ/aYIPmCPaexO+QMINgDjYV+1SfGzG531pgP8ZGbD+RtnvtRow6RR9tOLeu8bx8J55eUd6XMQgG2odprmRplrl8UJqrJChpqh6ROLTEZY1mPC56bL5DVnaUEE3w==; dais-s=aCA9O3stOeAiZM4QH5cbsT1DppKSphx8dV2nPyxoJcLhN+YiA8iwiIU/xWWFBBUtY293p5NR9p2glftfFNkNgIuxyaIW1FKurv9SBtZiQ1w=; GAFED_Session=L91/fJV28vv7x4yc9n0edp5JpMscCJVipRiqU92kD4rZVMwMYrgpOixtwxC8qU2H; GAFed_Identity=6E3djpm90VsS8+AuCDwJH0NlPNEiY5ZEmiTQZWr+jiCVZGn6Ri+sYx2//h129BC9EVePQ9neRPq9DVGaF+UvghvgNBTmKADeRi1PKV7QFBMUDrcOAttPspfq3exVQTMj39UbInA/QZadXzPNO55vCSbhKz7F2cS9IFbdMcFSH6hC3ImF8//qM0zjwB/AoUtEY9OQvY7DFHeOxe+3fV3eMg==; Profile=8fff98a8-6e91-4740-af7c-b40c6b1c82de; eSupId=SID=da3ebb32-a66c-4c2e-b58f-a107431d42ea; OLRProduct=OLRProduct=G8964D2|; lwp=c=us&l=en&cs=19&s=dhs; eSupportSegment=c=us&l=en&cs=19&s=dhs; mbox=PC#1473156541683-401884.24_2#1474438600|session#1473226729287-531542#1473230860; s_c49=c%3Dus%26l%3Den%26s%3Ddhs%26cs%3D19%26servicetag%3Dg8964d2%26systemid%3Dpoweredge-r430; gpv_pn=us%7Cen%7Cdhs%7C19%7Cesupport-home%7Cproductsupport%7Cservicetag; s_depth=2; s_sq=%5B%5BB%5D%5D; s_cc=true; LastVisit=Wed%2C%2007%20Sep%202016%2006%3A16%3A42%20GMT; cidlid=%3A%3A; s_dl=1; s_hwp=19%7C%7Cnull%7C%7C7%3A9%3A2016%3A14%3A16%7C%7CN%7C%7CN%7C%7Cnull%7C%7CNaN%7C%7Cnull%7C%7Cnull%7C%7CN%7C%7Cnull%7C%7Cnull%7C%7Cg8964d2; s_invisit=true; s_ppv=us%257Cen%257Cdhs%257C19%257Cesupport-home%257Cproductsupport%257Cservicetag%2C27%2C27%2C678'}
    for url in urls:
        r = requests.get(url, cookies=cok)
        parser = PoemParser()
        parser.feed(r.content)
        print ''


if __name__ == '__main__':
    # 格式"10.0.2.33","2011-09-06","2014-09-07"

    f = open('DELL_SN.txt', 'r+')
    urls  = get_info(f)
    data = get_date(urls)
    f.close()