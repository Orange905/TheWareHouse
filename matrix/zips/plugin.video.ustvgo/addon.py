import routing
from xbmcgui import ListItem
from xbmcplugin import addDirectoryItem, endOfDirectory
import xbmcplugin
from bs4 import BeautifulSoup
import requests
import socket
import requests.packages.urllib3.util.connection as urllib3_cn
import re
from datetime import datetime, timezone, timedelta
import random
import urllib.parse

urllib3_cn.allowed_gai_family = lambda: socket.AF_INET  # Uses IPv4 over IPv6
plugin = routing.Plugin()

def random_ua():
    ua_list = [
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36 RuxitSynthetic/1.0 v2272396916161516908 t7889551165227354132',
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36 RuxitSynthetic/1.0 v4596890125213045288 t4157550440124640339',
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36 RuxitSynthetic/1.0 v7496848312646576374 t7607367907735283829',
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36 RuxitSynthetic/1.0 v2804496347624254793 t1191530496833852085',
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36 RuxitSynthetic/1.0 v3736745345210846356 t1236787695256497497',
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36 RuxitSynthetic/1.0 v8557470257436417323 t7889551165227354132',
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36 RuxitSynthetic/1.0 v2471178984251391048 t4157550440124640339',
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36 RuxitSynthetic/1.0 v3190326415964944516 t6281935149377429786',
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36 RuxitSynthetic/1.0 v4056739060456661247 t6331743126571670211',
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36 RuxitSynthetic/1.0 v1191323528017047915 t3345461284722333977']
    return random.choice(ua_list)

@plugin.route('/')
def index():
    addDirectoryItem(plugin.handle, plugin.url_for(show_live, "USTVGO"), ListItem('USTvGo'), True)
    endOfDirectory(plugin.handle)

@plugin.route('/categories/LiveTV/<provider>')
def show_live(provider):
    headers = {
        'user-agent': random_ua(),
        'referer': '',
    }
    if provider == 'USTVGO':
        channel_key = {'ABC ': 'ABC', 'ABC 7 New York': 'ABCNY', 'ACC Network': 'ACCN', 'AMC ': 'AMC',
                       'Animal ': 'Animal', 'BBCAmerica': 'BBCAmerica', 'Big Ten Network': 'BTN',
                       'Boomerang ': 'Boomerang', 'Bravo ': 'Bravo', 'C-SPAN': 'CSPAN', 'CBS ': 'CBS',
                       'CBS 2 New York': 'CBSNY', 'CBS Sports Network': 'CBSSN', 'Cinemax': 'Cinemax', 'CMT': 'CMT',
                       'Cartoon Network': 'CN', 'CNBC ': 'CNBC', 'CNN ': 'CNN', 'Comedy ': 'Comedy', 'CW ': 'CW',
                       'CW 11 New York': 'CWNY', 'Destination America': 'DA',
                       'Disney ': 'Disney', 'DisneyJr ': 'DisneyJr', 'DisneyXD ': 'DisneyXD',
                       'Do it yourself ( DIY ) ': 'DIY', 'E!': 'E', 'ESPN2 ': 'ESPN2',
                       'ESPNU': 'ESPNU', 'ESPNews': 'ESPNews', 'FoodNetwork ': 'FoodNetwork', 'FOX ': 'FOX',
                       'FOX 5 New York': 'FOXNY', 'FoxBusiness ': 'FoxBusiness', 'FoxNews': 'FoxNews',
                       'Freeform ': 'Freeform', 'Fox Sports 2 (FS2)': 'FS2', 'FX': 'FX',
                       'FX Movie Channel ': 'FXMovie', 'FXX ': 'FXX',
                       'Game Show Network ': 'GSN', 'Hallmark Channel ': 'Hallmark', 'HGTV ': 'HGTV',
                       'HLN': 'HLN', 'Hallmark Movies & Mysteries': 'HMM',
                       'Lifetime': 'Lifetime',
                       'Lifetime Movie Network': 'LifetimeM', 'MLB Network': 'MLB', 'Motor Trend': 'MotorTrend',
                       'MSNBC': 'MSNBC', 'MTV': 'MTV','Nat Geo Wild': 'NatGEOWild',
                       'NFL RedZone': 'NFLRZ', 'Nickelodeon ': 'Nickelodeon',
                       'Nicktoons ': 'Nicktoons', 'One America News Network': 'OAN',
                       'Oprah Winfrey Network (OWN) ': 'OWN', 'Olympic Channel ': 'OLY', 'Oxygen ': 'Oxygen',
                       'PBS ': 'PBS', 'POP ': 'POP', 'Science ': 'Science',
                       'SEC Network': 'SECN', 'StarZ ': 'StarZ', 'SundanceTV ': 'SundanceTV',
                       'SYFY ': 'SYFY', 'TBS ': 'TBS', 'Telemundo ': 'Telemundo',
                       'TLC ': 'TLC', 'Travel Channel ': 'Travel',
                       'truTV ': 'TruTV', 'TV Land ': 'TVLand', 'The Weather Channel': 'TWC',
                       'We TV ': 'WETV', 'WWE Network': 'WWE',
                       'YES Network': 'YES'}
        m3u8 = f'https://h5.ustvgo.la_tobereplaced_myStream/playlist.m3u8?wmsAuthSign=c2VydmVyX3RpbWU9MS8yOS8yMDIyIDY6Mjg6MjggQU0maGFzaF92YWx1ZT1aWGdNakRreFY2bElqckdYT2Nha1RBPT0mdmFsaWRtaW51dGVzPTI0MA=='
        soup = BeautifulSoup(
            requests.get('https://ustvgo.tv').content, 'html.parser')
        channels_list = soup.find('div', {'class': 'entry-content'}).find_all('a')
        for channel in channels_list:
            try:
                channel_soup = BeautifulSoup(
                    requests.get(channel['href']).content, 'html.parser')
                channel_url = 'https://ustvgo.tv/' + \
                              channel_soup.find('div', {'class': 'iframe-container'}).find('iframe')['src']
                headers['referer'] = channel_url
                response = requests.get(channel_url, headers=headers)
                php_soup = BeautifulSoup(response.content, 'html.parser')
                m3u8 = re.search(r"var hls_src='(.*?)'", str(php_soup)).group(1)
                m3u8 = m3u8.replace(f'/{channel_key[channel.text]}/', '_tobereplaced_')
                break
            except:
                pass
        for channel in channels_list:
            try:
                title = channel.text
                li = ListItem(title)
                li.setInfo('video', {'title': title, 'mediatype': 'video'})
                m3u8_url = m3u8.replace('_tobereplaced_', f'/{channel_key[channel.text]}/')
                addDirectoryItem(plugin.handle, m3u8_url, li)
            except:
                pass
    xbmcplugin.addSortMethod(plugin.handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    endOfDirectory(plugin.handle)

if __name__ == '__main__':
    plugin.run()