# Merkle 树

该库实现了 Merkle 树的数据结构，可以用于 Merkle 证明、块验证等应用。

## 特性

- 支持建立和验证 Merkle 树
- 节点数据类支持快照和拷贝
- 验证根哈希是否匹配块哈希
- 获取块在树中的位置和证明
- 打印树结构

## 快速使用

```python
import merkle_tree

# 构建 Merkle 树
values = [b'value1', b'value2', ...]  
tree = MerkleTree(values, hash_fn)

# 验证块是否在树中
root_hash = tree.root.value
block_hash = b'value1'
tree.verify_block(root_hash, block_hash) 

# 获取块的位置和证明  
location = tree.get_location(block_hash)
proof = tree.get_proof(block_hash)
```

## API 说明

### MerkleTree

- 初始化树结构
    `__init__(self, values: List[bytes], hash_fn: HashFn) -> None`
- 获取根节点快照
    `@property root(self) -> Node`
- 树结构比较
    `compare_trees(self, other: "MerkleTree") -> bool`
- 块验证
    `verify_block(self, root_hash: bytes, block_hash: bytes) -> bool`
- 获取块位置
    `get_location(self, block_hash: bytes) -> Optional[List[int]]`
- 获取块证明
    `get_proof(self, block_hash: bytes) -> Optional[List[bytes]]`
- 打印树结构
    `print_tree(self, brief: bool = True) -> None`

### Node

- 定义树节点属性和方法
    `__init__(self, left: Optional["Node"], right: Optional["Node"], value: bytes, content: bytes, is_copied: bool = False)`
- 拷贝节点
    `copy(self) -> "Node"`

## 参与贡献

欢迎贡献新功能和报告问题!可以参考代码注释和测试进行改进。

## 许可

MIT
