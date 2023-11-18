import dataclasses

from typing import Callable, Optional, List

HashFn = Callable[[bytes], bytes]


def bytes_xor(a: bytes, b: bytes) -> bytes:
    assert len(a) == len(b), "length of a and b should be equal"
    return bytes([_a ^ _b for _a, _b in zip(a, b)])


def verify_proof(
    root_hash: bytes, block_hash: bytes, proof: List[bytes], hash_fn: HashFn
) -> bool:
    """verify if a block hash is in a Merkle Tree with a given root hash and proof"""
    current_hash = block_hash
    for sibling_hash in reversed(proof):
        current_hash = hash_fn(bytes_xor(current_hash, sibling_hash))

    return current_hash == root_hash


@dataclasses.dataclass
class Node:
    """
    Represents a binary tree node, in our case a Merkle Tree node.

    Attributes:
        left: left child node
        right: right child node
        value: hash value of the node
        content: content of the node
        is_copied: whether the node is a copy, this is because we duplicate
            the last element if the number of elements is odd when building
    """

    left: Optional["Node"]
    right: Optional["Node"]
    value: bytes
    content: bytes  # just for debugging, remove in production
    is_copied: bool = False

    def __str__(self) -> str:
        return self.value.decode("utf-8")

    def copy(self) -> "Node":
        """
        Get the duplication of the node.
        We mark the node with copied=True when duplicating the last element.
        """
        return Node(self.left, self.right, self.value, self.content, True)


class MerkleTree:
    """
    Represents a Merkle Tree, for which every leaf node is labelled with the hash
    of a data block, and every non-leaf node is labelled with the crypto hash of
    the labels of its child nodes. It is used to verify the integrity of blocks.
    """

    def __init__(self, values: List[bytes], hash_fn: HashFn) -> None:
        self._hash_fn = hash_fn
        self._root: Node = self._buildTree(values)

    def __str__(self) -> str:
        return self._root.value.hex()

    @property
    def root(self) -> Node:
        """
        get the duplication of root node of the Merkle Tree
        """
        return self._root.copy()

    def _buildTree(self, values: List[bytes]) -> Node:
        leaves: List[Node] = [Node(None, None, self._hash_fn(e), e) for e in values]
        return self._buildTreeRec(leaves)

    def _buildTreeRec(self, nodes: List[Node]) -> Node:
        # duplicate last elem if odd number of elements
        if len(nodes) % 2 == 1:
            nodes.append(nodes[-1].copy())

        half: int = len(nodes) // 2
        if len(nodes) == 2:
            value = self._hash_fn(bytes_xor(nodes[0].value, nodes[1].value))
            return Node(nodes[0], nodes[1], value, nodes[0].content + nodes[1].content)

        left: Node = self._buildTreeRec(nodes[:half])
        right: Node = self._buildTreeRec(nodes[half:])
        value: bytes = self._hash_fn(bytes_xor(left.value, right.value))
        return Node(left, right, value, left.content + right.content)

    def compare_trees(self, other: "MerkleTree") -> bool:
        """
        Compare the root hashes of two Merkle Trees
        """
        return self._root.value == other._root.value

    def verify_block(self, root_hash: bytes, block_hash: bytes) -> bool:
        """
        Verify if a block hash is in a Merkle Tree with a given root hash
        """
        return self._root.value == root_hash and self._verify_block_rec(
            self._root, block_hash
        )

    def _verify_block_rec(self, node: Optional[Node], block_hash: bytes) -> bool:
        if node is None:
            return False

        return (
            node.value == block_hash
            or self._verify_block_rec(node.left, block_hash)
            or self._verify_block_rec(node.right, block_hash)
        )

    def get_location(self, block_hash: bytes) -> Optional[List[int]]:
        """
        Get the location of a block hash in a Merkle Tree
        """
        return self._get_location_rec(self._root, block_hash, [])

    def _get_location_rec(
        self, node: Optional[Node], block_hash: bytes, path: List[int]
    ) -> Optional[List[int]]:
        if node is None:
            return None

        if node.value == block_hash and not node.is_copied:
            return path

        left_path = self._get_location_rec(node.left, block_hash, path + [0])
        if left_path is not None:
            return left_path

        right_path = self._get_location_rec(node.right, block_hash, path + [1])
        if right_path is not None:
            return right_path

        return None

    def get_proof(self, block_hash: bytes) -> Optional[List[bytes]]:
        """
        Get the proof of a block hash in a Merkle Tree.
        The proof is a list of sibling hashes of the block hash.

        Note:
            This function returns hashes in the top-down order. So, don't forget
            to reverse the list when you want to verify the proof.
        """
        location = self.get_location(block_hash)
        if location is None:
            return None

        return self._get_proof_rec(self._root, location, 0, [])

    def _get_proof_rec(
        self, node: Optional[Node], location: List[int], index: int, proof: List[bytes]
    ) -> Optional[List[bytes]]:
        if node is None or index >= len(location):
            return proof

        if node.right and location[index] == 0:
            proof.append(node.right.value)
            return self._get_proof_rec(node.left, location, index + 1, proof)

        elif node.left and location[index] == 1:
            proof.append(node.left.value)
            return self._get_proof_rec(node.right, location, index + 1, proof)

        return None

    def print_tree(self, brief: bool = True) -> None:
        """
        Print the Merkle Tree in a tree structure.
        """
        self._print_tree_rec(self._root, 0, brief)

    def _print_tree_rec(self, node: Optional[Node], level: int, brief: bool) -> None:
        """helper function for print_tree"""
        if node is None:
            return

        value = (node.value[:4] if brief else node.value).hex()
        content = node.content
        print(f'{"    " * level}{value=}, {content=}')
        self._print_tree_rec(node.left, level + 1, brief)
        self._print_tree_rec(node.right, level + 1, brief)
