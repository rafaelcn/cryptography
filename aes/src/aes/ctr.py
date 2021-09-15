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

    def __split_blocks(self, message, block_size=16):
        return [message[i:i+16] for i in range(0, len(message), block_size)]

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

    def encrypt_block(self, plaintext):

        plain_state = common.bytes2matrix(plaintext)

        common.add_round_key(plain_state, self._key_matrices[0])

        for i in range(1, self.rounds):
            common.sub_bytes(plain_state)
            common.shift_rows(plain_state)
            common.mix_columns(plain_state)
            common.add_round_key(plain_state, self._key_matrices[i])

        common.sub_bytes(plain_state)
        common.shift_rows(plain_state)
        common.add_round_key(plain_state, self._key_matrices[-1])

        return common.matrix2bytes(plain_state)

    def decrypt_block(self, ciphertext):
        cipher_state = common.bytes2matrix(ciphertext)

        common.add_round_key(cipher_state, self._key_matrices[-1])
        common.inv_shift_rows(cipher_state)
        common.inv_sub_bytes(cipher_state)

        for i in range(self.rounds - 1, 0, -1):
            common.add_round_key(cipher_state, self._key_matrices[i])
            common.inv_mix_columns(cipher_state)
            common.inv_shift_rows(cipher_state)
            common.inv_sub_bytes(cipher_state)

        common.add_round_key(cipher_state, self._key_matrices[0])

        return common.matrix2bytes(cipher_state)

    def encrypt(self, plaintext):
        blocks = []
        nonce = self.iv

        for plaintext_block in self.__split_blocks(plaintext):
            block = self.__xor_bytes(plaintext_block,
                                     self.encrypt_block(nonce))
            blocks.append(block)
            nonce = self.__inc_bytes(nonce)

        return b''.join(blocks)

    def decrypt(self, ciphertext):

        blocks = []
        nonce = self.iv

        for ciphertext_block in self.__split_blocks(ciphertext):
            block = self.__xor_bytes(ciphertext_block,
                                     self.encrypt_block(nonce))
            blocks.append(block)
            nonce = self.__inc_bytes(nonce)

        return b''.join(blocks)
