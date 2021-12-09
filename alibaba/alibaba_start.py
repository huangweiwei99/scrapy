import datetime
# db.createUser({'user':'alibaba','pwd':'123456','roles':[{role:"userAdminAnyDatabase",db:"site"}]});
# db.createUser({"user":"alibaba","pwd":"@123456-","roles":[{role:"userAdminAnyDatabase",db:"site"}]})
# db.createUser()
import pytz
from scrapy import cmdline
today = datetime.datetime.now(pytz.timezone('PRC')).strftime("%Y-%m-%d_%H-%M-%S")
# cmdline.execute(['scrapy', 'crawl', 'detail'])
# cmdline.execute(['scrapy', 'crawl', 'tranaction_countries'])
# cmdline.execute(['scrapy', 'crawl', 'tranaction_overview'])
cmdline.execute(['scrapy', 'crawl', 'more_detail',
                 '-o', '{0}_{1}.json'.format('S009', today)
                 ])
# cmdline.execute(['scrapy', 'crawl', 'top-ranking-products'])
# cmdline.execute(['scrapy', 'crawl', 'search_result_by_keyword',
#                  '-o', '{0}_{1}.csv'.format('关键字结果', today)
#                  ])

# cmdline.execute(['scrapy', 'crawl', 'products_in_shops',
#                  '-o', '{0}_{1}.json'.format('products_in_shops', today)
#                  ])