import csv
from datetime import datetime, timezone

from pep_parse.settings import BASE_DIR


class PepParsePipeline:

    def open_spider(self, spider):
        self.status_summary = dict()
        self.results_dir = BASE_DIR / 'results'

    def process_item(self, item, spider):
        self.status_summary[item['status']] = (
            self.status_summary.get(item['status'], 0) + 1)
        return item

    def close_spider(self, spider):
        cur_datetime = datetime.now(timezone.utc).strftime('%Y-%m-%d_%H-%M-%S')
        csv_file = self.results_dir / f'status_summary_{cur_datetime}.csv'
        with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Статус', 'Количество']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for i in self.status_summary:
                writer.writerow(
                    {'Статус': i, 'Количество': self.status_summary[i]}
                )
            writer.writerow(
                {
                    'Статус': 'Total',
                    'Количество': sum(self.status_summary.values())
                }
            )
