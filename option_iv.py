import json
import urllib2
import os
import hashlib
from prettytable import PrettyTable

symbols = ['NTNX', 'MSFT', 'SNAP', 'NVDA', 'AMD', 'BABA', 'SINA', 'JD', 'PTC', 'PYPL', 'SHOP', 'SQ', 'ATVI', 'MSFT', 'FB', 'AAPL', 'RGC', 'AMC', 'YUMC', 'YUM', 'DPZ', 'SHAK', 'PZZA', 'CMG', 'KO', 'BRK-B', 'DFS', 'COF', 'JPM', 'MS', 'BAC', 'ALK', 'DAL', 'JBLU', 'AAL', 'T', 'TMUS', 'VZ', 'KR', 'TGT', 'WMT', 'HD', 'LOW', 'BAC', 'TSLA']
dates = [1513296000,1516320000]
options_url = 'https://query1.finance.yahoo.com/v7/finance/options/%s?formatted=true&crumb=YurFu24iKIC&lang=en-US&region=US&date=%d&corsDomain=finance.yahoo.com'

# contains the options data
# [symbol, quote, strike, premium, iv, percentage_profit]
data = {}

class CachedReader:
  def __init__(self):
    # Create the cache directory
    self.cache_dir = 'cache'
    if not os.path.exists(self.cache_dir):
      os.mkdir(self.cache_dir)
  
  def get(self, url):
    cache_path = self.cache_dir + '/' + hashlib.md5(url).hexdigest()
    if os.path.exists(cache_path):
      return open(cache_path).read()
    else:
      content = urllib2.urlopen(url).read()
      open(cache_path, 'w').write(content)
      return content

for date in dates:
  data[date] = []

r = CachedReader()

for symbol in symbols:
  for date in dates:
    info = json.loads(r.get(options_url % (symbol, date)))
    # print data
    info = info['optionChain']['result'][0]
    quote = info['quote']['regularMarketPrice']
    options = info['options'][0]

    for option in options['calls']:
      if option['strike']['raw'] > quote:
        strike = option['strike']['raw']
        premium = option['lastPrice']['raw'] 
        iv = option['impliedVolatility']['raw']
        pp = ((strike + premium - quote) / quote) * 100.0
        data[date].append([symbol, quote, strike, premium, iv, pp])
        break

def cmp(a, b):
  if a[4] > b[4]:
      return -1
  elif a[4] == b[4]:
      if a[1] > b[1]:
          return 1
      else:
          return -1
  else:
      return 1

for date in dates:
  ddata = data[date]
  ddata.sort(cmp)
  x = PrettyTable(['Symbol', 'Quote', 'Strike', 'Premium', 'IV', 'PP'])
  for line in ddata:
    x.add_row(line)
  print x





