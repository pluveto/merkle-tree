import hashlib
import unittest
from merkle_tree import MerkleTree, verify_proof


def sha256(val: bytes) -> bytes:
    return hashlib.sha256(val).digest()


class TestMerkleTree(unittest.TestCase):
    def setUp(self):
        """set up a MerkleTree with some testing data"""
        self._data = list(
            map(
                lambda x: x.encode("utf-8"),
                [
                    # https://en.wikipedia.org/wiki/Classical_Chinese_poetry
                    "Li Bai",
                    "Du Fu",
                    "Wang Wei",
                    "Bai Juyi",
                    "Su Shi",
                    "Li Shangyin",
                    "Li Qingzhao",
                    "Wang Anshi",
                ],
            )
        )
        self._hash_fn = sha256
        self._tree = MerkleTree(self._data, self._hash_fn)
        self._tree.print_tree()

    def test_verify_block(self):
        """test the verify_block method"""
        root_hash = self._tree.root.value
        for i in range(len(self._data)):
            block_hash = self._hash_fn(self._data[i])
            # verify if the block hash is in the tree
            self.assertTrue(self._tree.verify_block(root_hash, block_hash))

        # verify a invalid block hash
        self.assertFalse(
            self._tree.verify_block(root_hash, self._hash_fn("invalid".encode("utf-8")))
        )

    def test_get_location(self):
        """test the get_location method"""
        for i in range(len(self._data)):
            block_hash = self._hash_fn(self._data[i])
            location = self._tree.get_location(block_hash)
            # compare the location with the expected value location(block_hash)
            assert location is not None, "location should not be None"
            # location should conform to the binary counting sequence 000...111
            self.assertEqual(location, [int(x) for x in format(i, "b").zfill(3)])

        self.assertIsNone(
            self._tree.get_location(self._hash_fn("invalid".encode("utf-8")))
        )

    def test_get_proof(self):
        """test the get_proof method"""
        for i in range(len(self._data)):
            block_hash = self._hash_fn(self._data[i])
            # get the proof of the block hash in the tree
            proof = self._tree.get_proof(block_hash)
            assert proof is not None, "proof should not be None"
            self.assertEqual(len(proof), 3)
            self.assertTrue(
                verify_proof(self._tree.root.value, block_hash, proof, self._hash_fn),
                f"proof {proof} is invalid for block {block_hash}",
            )

        self.assertIsNone(
            self._tree.get_proof(self._hash_fn("invalid".encode("utf-8")))
        )

    def test_verify_proof(self):
        """test the verify_proof method"""
        root_hash = self._tree.root.value
        for i in range(len(self._data)):
            block_hash = self._hash_fn(self._data[i])
            # get the proof of the block hash in the tree
            proof = self._tree.get_proof(block_hash)
            assert proof is not None, "proof should not be None"
            self.assertTrue(verify_proof(root_hash, block_hash, proof, self._hash_fn))

        # verify a invalid proof
        self.assertFalse(
            verify_proof(
                root_hash, self._hash_fn("invalid".encode("utf-8")), [], self._hash_fn
            )
        )


if __name__ == "__main__":
    unittest.main()
