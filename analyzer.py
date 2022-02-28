from databaseAPI import DatabaseAPI
from transaction_objects import Input

class Analyzer:

    def __init__(self, db: DatabaseAPI):
        self.db = db
        self.cursor = db.cursor

    def check_input_address_present(self, input_: Input):
        pass

    def get_transactions_by_day(self):
        return self.db.get_query_generator(
            f'''SELECT MONTH(timestamp), DAY(timestamp), SUM(n_transactions) FROM blocks 
        GROUP BY MONTH(timestamp), DAY(timestamp) ORDER BY MONTH(timestamp), DAY(timestamp)''')

    def get_volume_by_day(self):
        return self.db.get_query_generator(
            f'''SELECT MONTH(timestamp), DAY(timestamp), SUM(value) FROM
        {self.db.join_tables(['blocks', 'transactions', 'outputs'])}
        GROUP BY MONTH(timestamp), DAY(timestamp) ORDER BY MONTH(timestamp), DAY(timestamp)''')

    def get_values(self):
        return self.db.get_query_generator(
            '''SELECT value FROM outputs ORDER BY RAND() LIMIT 10000'''
        )

    # def getget(self):
    #     self.cursor.execute(
    #         '''SELECT DAY(timestamp), MONTH(timestamp), YEAR(timestamp),
    #         SUM(value) AS volume, SUM(n_transactions) AS n_transactions
    #         from blocks INNER JOIN transactions ON blocks.block_id = transactions.block_id INNER JOIN
    #         outputs ON transactions.tx_id = outputs.tx_from_id
    #         GROUP BY YEAR(timestamp), MONTH(timestamp), DAY(timestamp)
    #         ORDER BY DAY(timestamp);'''
    #     )