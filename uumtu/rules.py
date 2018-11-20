from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

rules = {
    'xinggan': (
        Rule(LinkExtractor(allow='xinggan\/.*\.html', restrict_xpaths='//div[@id="mainbodypul"]//a'), callback='parse_item'),
        Rule(LinkExtractor(restrict_xpaths='//div[contains(@class, "both")]//a[contains(., "下一页")]'))
    )
}