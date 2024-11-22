from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

RESULTS = 'results'

BOT_NAME = 'pep_parse'

NEWSPIDER_MODULE = f'{BOT_NAME}.spiders'

SPIDER_MODULES = [NEWSPIDER_MODULE]

ROBOTSTXT_OBEY = True

ITEM_PIPELINES = {
    'pep_parse.pipelines.PepParsePipeline': 300,
}

FEEDS = {
    f'{RESULTS}/pep_%(time)s.csv': {
        'format': 'csv',
        'fields': ['number', 'name', 'status'],
    },
}
