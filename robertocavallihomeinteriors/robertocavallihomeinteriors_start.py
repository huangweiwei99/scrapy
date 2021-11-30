import datetime

import pytz
from scrapy import cmdline

# cmdline.execute(['scrapy', 'crawl', 'robertocavallihomeinteriors_detail'])

today = datetime.datetime.now(pytz.timezone('PRC')).strftime("%Y-%m-%d_%H-%M-%S")

cmdline.execute(['scrapy', 'crawl', 'robertocavallihomeinteriors_index',
                 '-o', '{0}_{1}.json'.format('robertocavallihomeinteriors', today)
                 ])
