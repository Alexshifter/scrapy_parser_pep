from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

RESULTS_DIR = 'results'

BOT_NAME = 'pep_parse'

NEWSPIDER_MODULE = f'{BOT_NAME}.spiders'

SPIDER_MODULES = [f'{NEWSPIDER_MODULE}']

ROBOTSTXT_OBEY = True

ITEM_PIPELINES = {
    'pep_parse.pipelines.PepParsePipeline': 300,
}

FEEDS = {
    RESULTS_DIR + '/pep_%(time)s.csv': {
        'format': 'csv',
        'fields': ['number', 'name', 'status'],
    },
}
