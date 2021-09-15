from . import common


class ECB:
    """ECB is an abstraction over the Electronic Code Book mode of operation.

    """
    def __init__(self, key, rounds=10, bs=16):
        self.rounds = rounds
        self.block_size = bs
        self._key_matrices = self.__expand_key(key)

    def __expand_key(self, key):
        """
        Initialize round keys with raw key material.
        """
        key_columns = common.bytes2matrix(key)
        iteration_size = len(key) // 4

        # cache iteration has exactly as many columns as the key material.
        i = 1
        while len(key_columns) < (self.rounds + 1) * 4:
            # copy previous word.
            word = list(key_columns[-1])

            # perform schedule_core once every "row".
            if len(key_columns) % iteration_size == 0:
                # circular shift.
                word.append(word.pop(0))
                # map to s-box.
                word = [common.rijndael_box[b] for b in word]
                i += 1
            key_columns.append(word)

        # group key columns in 4x4 byte matrices.
        g = [key_columns[4*i: 4*(i+1)] for i in range(len(key_columns) // 4)]
        return g

    def encrypt(self, plaintext):
        """
        Encrypt a plaintext with the given key.
        """
        if len(plaintext) <= 0:
            return b''

        blocks = []

        for plaintext_block in common.split_blocks(plaintext):
            block = common.encrypt_block(plaintext_block, self.rounds,
                                         self._key_matrices)
            blocks.append(block)

        return b''.join(blocks)

    def decrypt(self, cryptogram):
        """
        Decrypt a cryptogram with the given key.
        """
        if len(cryptogram) <= 0:
            return b''

        blocks = []

        for cryptogram_block in common.split_blocks(cryptogram):
            block = common.decrypt_block(cryptogram_block, self.rounds,
                                         self._key_matrices)
            blocks.append(block)

        return b''.join(blocks)
