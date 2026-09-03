# 运行参数

## rebuild_resident

用于需要刷新常驻快照时。

适用：

- resident 明显过期。
- 多条高价值事实写入后。
- 关键约束变化后。

## sync_index

用于需要刷新检索索引时。

适用：

- 写入多条可检索候选。
- 检索结果明显落后。
- 新增重要 factual/procedural 内容。

## run_lifecycle

用于生命周期治理。

适用：

- 需要清理过期内容。
- 需要治理低价值候选。
- 需要阶段性整理 memory。
