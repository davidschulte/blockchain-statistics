from blockchain_parser.transaction import Transaction as ParserTx
from blockchain_parser.transaction import Input as ParserIn
from blockchain_parser.transaction import Output as ParserOut


class Transaction:

    def __init__(self, tx: ParserTx):
        self.id = tx.hash
        self.inputs = [Input(p_in, tx.hash) for p_in in tx.inputs]
        self.outputs = [Output(p_out, tx.hash, output_no) for output_no, p_out in enumerate(tx.outputs) if p_out.value > 0]
        self.n_inputs = len(self.inputs)
        self.n_outputs = len(self.outputs)
        self.is_standard = self.check_if_standard()

    def check_if_standard(self):
        for output in self.outputs:
            if not output.is_standard:
                return False

        return True

class Input:

    def __init__(self, input_: ParserIn, tx_id: str):
        self.tx_id = tx_id
        self.tx_from = input_.transaction_hash
        self.tx_output_no = input_.transaction_index


class Output:

    def __init__(self, output: ParserOut, tx_id: str, output_no: int):
        self.is_standard = output.type != "OP_RETURN"

        if self.is_standard:
            self.tx_id = tx_id
            self.output_no = output_no
            self.wallet = output.addresses[0].address
            self.value = output.value

