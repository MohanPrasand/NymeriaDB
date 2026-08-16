# NymeriaDB

NymeriaDB is a lightweight key-value database written in Python to explore the internals of modern storage engines.

It is built around a Log-Structured Merge (LSM) Tree architecture with immutable SSTables and Write-Ahead Logging (WAL) for durability.

## Features

- [x] AVL Tree MemTable
- [x] Immutable SSTables
- [x] Multi-level LSM Tree
- [x] Compaction
- [x] Tombstones
- [x] Bloom Filters
- [x] Write-Ahead Log (WAL)
- [x] Crash Recovery
- [x] Manifest
- [ ] Sparse Index
- [ ] Background Compaction
- [ ] Distributed Design

## Roadmap

### Storage Engine
- [x] LSM Tree
- [x] WAL
- [x] Manifest
- [ ] Sparse Index
- [ ] Compression
- [ ] Block Cache

### Distributed Database
- [ ] Replication
- [ ] Leader Election
- [ ] Sharding

### AI Integration
- [ ] MCP Server
- [ ] Long-term AI Memory
