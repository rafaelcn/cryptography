from . import common


class CTR:
    def __init__(self, master_key, iv, rounds=10):
        self.iv = iv
        self.rounds = rounds
        self._key_matrices = self.__expand_key(master_key)

    def __xor_bytes(self, a, b):
        return bytes(i ^ j for i, j in zip(a, b))

    def __inc_bytes(self, a):
        out = list(a)
        for i in reversed(range(len(out))):
            if out[i] == 0xFF:
                out[i] = 0
            else:
                out[i] += 1
                break
        return bytes(out)

    def __expand_key(self, master_key):

        # Initialize round keys with raw key material.
        key_columns = common.bytes2matrix(master_key)
        iteration_size = len(master_key) // 4

        i = 1
        while len(key_columns) < (self.rounds + 1) * 4:
            # Copy previous word.
            word = list(key_columns[-1])

            # perform schedule_core once every "row".
            if len(key_columns) % iteration_size == 0:
                # circular shift.
                word.append(word.pop(0))
                # map to the rijndael box.
                word = [common.rijndael_box[b] for b in word]
                # XOR with first byte of the round column matrix, since the
                # others bytes of the round column table are 0.
                word[0] ^= common.round_column[i]
                i += 1
            # XOR with equivalent word from previous iteration.
            word = self.__xor_bytes(word, key_columns[-iteration_size])
            key_columns.append(word)

        # Group key words in 4x4 byte matrices.
        g = [key_columns[4*i: 4*(i+1)] for i in range(len(key_columns) // 4)]
        return g

    def encrypt(self, plaintext):

        blocks = []
        nonce = self.iv

        for plaintext_block in common.split_blocks(plaintext):
            block = self.__xor_bytes(plaintext_block,
                                     common.encrypt_block(nonce, self.rounds,
                                                          self._key_matrices))
            blocks.append(block)
            nonce = self.__inc_bytes(nonce)

        return b''.join(blocks)

    def decrypt(self, ciphertext):

        blocks = []
        nonce = self.iv

        for ciphertext_block in common.split_blocks(ciphertext):
            block = self.__xor_bytes(ciphertext_block,
                                     common.decrypt_block(nonce, self.rounds,
                                                          self._key_matrices))
            blocks.append(block)
            nonce = self.__inc_bytes(nonce)

        return b''.join(blocks)
