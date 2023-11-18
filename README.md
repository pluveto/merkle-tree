# Merkle Tree

[中文介绍](README.zh-CN.md)

This library implements the Merkle tree data structure, which can be used for Merkle proofs, block verification, etc.

This project mainly for learning and reference. Note that the code is not optimized for production use, Note that `content` field of tree node definition should be removed to avoid performance issue. You need to carefully review the code and test it before using it in production.

## Features

- Build and validate Merkle trees
- Node class supports snapshotting and copying
- Verify root hash matches block hash
- Get block location and proof in the tree
- Print tree structure

## Quick Start

```python
import merkle

# Build Merkle tree
values = [b'value1', b'value2', ...]
tree = MerkleTree(values, hash_fn) 

# Verify block is in tree
root_hash = tree.root.value
block_hash = b'value1'  
tree.verify_block(root_hash, block_hash)

# Get block location and proof
location = tree.get_location(block_hash)
proof = tree.get_proof(block_hash)
```

## API Documentation

### MerkleTree

- Initialize tree structure
    `__init__(self, values: List[bytes], hash_fn: HashFn) -> None`
- Get root node snapshot
    `@property root(self) -> Node`
- Compare tree structures
    `compare_trees(self, other: "MerkleTree") -> bool`
- Block verification
    `verify_block(self, root_hash: bytes, block_hash: bytes) -> bool`
- Get block location  
    `get_location(self, block_hash: bytes) -> Optional[List[int]]`
- Get block proof
    `get_proof(self, block_hash: bytes) -> Optional[List[bytes]]`
- Print tree structure
    `print_tree(self, brief: bool = True) -> None`

### Node

- Define node attributes  
    `__init__(self, left: Optional["Node"], right: Optional["Node"], value: bytes, content: bytes, is_copied: bool = False)`
- Copy nodes
    `copy(self) -> "Node"`

## Contributing

Contributions welcome! Please check code comments and tests for improvements.

## License

MIT
