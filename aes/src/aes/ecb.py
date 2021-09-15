from . import common


class ECB:
    def __init__(self, key, rounds=10):
        self.rounds = rounds
        self._key_matrices = self.__expand_key(key)

    def __expand_key(self, key):
        """
        Initialize round keys with raw key material.
        """
        key_columns = common.bytes2matrix(key)
        iteration_size = len(key) // 4

        # cach iteration has exactly as many columns as the key material.
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
        cryptogram = common.bytes2matrix(plaintext)

        common.add_round_key(cryptogram, self._key_matrices[0])

        for i in range(1, self.rounds):
            common.sub_bytes(cryptogram)
            common.shift_rows(cryptogram)
            common.mix_columns(cryptogram)
            common.add_round_key(cryptogram, self._key_matrices[i])

        common.sub_bytes(cryptogram)
        common.shift_rows(cryptogram)
        common.add_round_key(cryptogram, self._key_matrices[-1])

        return common.matrix2bytes(cryptogram)

    def decrypt(self, cryptogram):
        """
        Decrypt a cryptogram with the given key.
        """
        plaintext = common.bytes2matrix(cryptogram)

        common.add_round_key(plaintext, self._key_matrices[-1])
        common.inv_shift_rows(plaintext)
        common.inv_sub_bytes(plaintext)

        for i in range(self.rounds - 1, 0, -1):
            common.add_round_key(plaintext, self._key_matrices[i])
            common.inv_mix_columns(plaintext)
            common.inv_shift_rows(plaintext)
            common.inv_sub_bytes(plaintext)

        common.add_round_key(plaintext, self._key_matrices[0])

        return common.matrix2bytes(plaintext)