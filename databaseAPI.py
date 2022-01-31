import mysql.connector
from transaction_objects import Transaction

LOGIN_DATA = {'host': 'localhost',
              'user': 'david',
              'passwd': 'bcdb4deda',
              'database': 'bitcoindb'}

# TABLES = ['blocks', 'transactions', 'outputs', 'inputs']
TABLES = {'blocks':         ['block_id BINARY(32) PRIMARY KEY',
                            'n_transactions SMALLINT UNSIGNED NOT NULL',
                            'timestamp DATETIME NOT NULL'],

          'transactions':   ['tx_id BINARY(32) PRIMARY KEY',
                             'block_id BINARY(32) NOT NULL'],

          'inputs':         ['tx_to_id BINARY(32) NOT NULL',
                             'tx_from_id BINARY(32) NOT NULL',
                             'output_no SMALLINT UNSIGNED NOT NULL',
                             'PRIMARY KEY (tx_from_id, output_no)'],

          'outputs':        ['tx_from_id BINARY(32) NOT NULL',
                             'output_no SMALLINT UNSIGNED NOT NULL',
                             'wallet_id VARCHAR(46) NOT NULL',
                             'value BIGINT UNSIGNED NOT NULL',
                             'PRIMARY KEY (tx_from_id, output_no)'],

          'wallets':        ['wallet_id VARCHAR(46) NOT NULL',
                             'tx_id BINARY(32) NOT NULL',
                             'input_output BIT(1) NOT NULL',
                             'value BIGINT UNSIGNED NOT NULL',
                             'PRIMARY KEY (wallet_id, tx_id, input_output)']}


JOIN_COLUMNS = {repr(['blocks', 'transactions']): [['block_id', 'block_id']],
                repr(['inputs', 'transactions']): [['tx_to_id', 'tx_id']],
                repr(['outputs', 'transactions']): [['tx_from_id', 'tx_id']],
                repr(['inputs', 'outputs']): [2*['tx_from_id'], 2*['output_no']]}


class DatabaseAPI:

    def __init__(self):
        self.db = mysql.connector.connect(**LOGIN_DATA)
        self.cursor = self.db.cursor()

    def create_tables(self):

        for table_name, table_attributes in TABLES.items():
            attributes_str = ', '.join(table_attributes)
            self.cursor.execute(f'CREATE TABLE IF NOT EXISTS {table_name} ({attributes_str})')
        # self.cursor.execute('CREATE TABLE IF NOT EXISTS blocks (block_id BINARY(32) PRIMARY KEY, n_transactions INT, timestamp DATETIME)')
        # self.cursor.execute('CREATE TABLE IF NOT EXISTS transactions (tx_id BINARY(32) PRIMARY KEY, block_id BINARY(32), n_inputs BIT(5), n_outputs BIT(5))')
        # self.cursor.execute('CREATE TABLE IF NOT EXISTS inputs (tx_to_id BINARY(32), tx_from_id BINARY(32), tx_output_no BIGINT, '+
        #                     'PRIMARY KEY (tx_from_id, tx_output_no))')
        # self.cursor.execute('CREATE TABLE IF NOT EXISTS outputs (tx_from_id BINARY(32), tx_output_no BIT(5), '+
        #                     'wallet VARCHAR(46), value BIGINT, PRIMARY KEY (tx_from_id, tx_output_no))')

        self.db.commit()

    def reset_database(self):
        confirmation = input("Are you sure that you want to reset the database? \n"
                             "This will delete everything. (Y/n)")
        if confirmation == "Y":
            self.drop_tables()
            self.create_tables()
            print("Database reset complete")
        else:
            print("Database reset aborted")

    def drop_tables(self):
        for t in TABLES.keys():
            self.cursor.execute('DROP TABLE IF EXISTS {}'.format(t))

    def get_query_generator(self, q):
        self.cursor.execute(q)

        for row in self.cursor.fetchall():
            yield row

    def get_query_list(self, q):
        self.cursor.execute(q)

        return self.cursor.fetchall()

    def join_tables(self, tables: list):
        join_str = tables[0]
        for i in range(len(tables)-1):
            to_connect = tables[i:i+2]
            order = sorted(range(len(to_connect)), key=lambda k: to_connect[k])
            to_connect = [to_connect[o] for o in order]
            join_cols = JOIN_COLUMNS[repr(to_connect)]
            join_str += f' INNER JOIN {tables[i+1]} ON {tables[i]}.{join_cols[0][order[0]]} = {tables[i+1]}.{join_cols[0][order[1]]}'
            if len(join_cols) == 2:
                join_str += f' AND {tables[i]}.{join_cols[1][order[0]]} = {tables[i+1]}.{join_cols[1][order[1]]}'

        return join_str

    def add_block(self, block):
        self.cursor.execute(f'''
                                INSERT IGNORE INTO blocks (block_id, n_transactions, timestamp) VALUES
                                (UNHEX('{block.hash}'), {block.n_transactions}, '{str(block.header.timestamp)}')''')
        for parser_tx in block.transactions:
            self.add_transaction(parser_tx, block.hash)

    def add_transaction(self, parser_tx, block_hash):
        tx = Transaction(parser_tx)

        if not tx.is_standard:
            return

        self.cursor.execute(f'''
                        INSERT IGNORE INTO transactions (tx_id, block_id, n_inputs, n_outputs) VALUES
                        (UNHEX('{tx.id}'), UNHEX('{block_hash}'), {tx.n_inputs}, {tx.n_outputs})''')

        for input_ in tx.inputs:
            self.cursor.execute(f'''
                        INSERT IGNORE INTO inputs (tx_to_id, tx_from_id, tx_output_no) VALUES
                        (0x{input_.tx_id}, 0x{input_.tx_from}, {input_.tx_output_no})''')

        for output in tx.outputs:
            self.cursor.execute(f'''
                        INSERT IGNORE INTO outputs (tx_from_id, tx_output_no, wallet, value) VALUES
                        (UNHEX('{output.tx_id}'), {output.output_no}, '{output.wallet}', {output.value})''')

        self.db.commit()

    def compute_wallets_table(self):
        self.cursor.execute(f'''
                                INSERT IGNORE INTO outputs (tx_from_id, tx_output_no, wallet, value) VALUES
                                (UNHEX('{output.tx_id}'), {output.output_no}, '{output.wallet}', {output.value})''')

        self.db.commit()
