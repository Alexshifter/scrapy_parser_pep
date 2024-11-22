import csv
from collections import defaultdict
from datetime import datetime, timezone

from pep_parse.settings import BASE_DIR, RESULTS_DIR


class PepParsePipeline:
    def __init__(self):
        self.results_dir = BASE_DIR / RESULTS_DIR

    def open_spider(self, spider):
        self.status_summary = defaultdict(int)

    def process_item(self, item, spider):
        self.status_summary[item['status']] += 1
        return item

    def close_spider(self, spider):
        cur_datetime = datetime.now(timezone.utc).strftime('%Y-%m-%d_%H-%M-%S')
        csv_file = self.results_dir / f'status_summary_{cur_datetime}.csv'
        self.status_summary['Total'] = sum(self.status_summary.values())
        rows = [
            {'Статус': i, 'Количество': self.status_summary[i]}
            for i in self.status_summary
        ]
        with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Статус', 'Количество']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
