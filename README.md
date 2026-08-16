# NymeriaDB

NymeriaDB is a key-value database built from scratch in Python.

It implements an LSM-tree-based storage engine with durability, crash recovery, multiple databases, and a TCP server/client architecture.

## Architecture

```text
                         ┌───────────────┐
                         │   NymeriaDB   │
                         │    Server     │
                         └───────┬───────┘
                                 │
                  ┌──────────────┴──────────────┐
                  │                             │
           ┌──────▼──────┐               ┌──────▼──────┐
           │  Session A  │               │  Session B  │
           └──────┬──────┘               └──────┬──────┘
                  │                             │
                  └──────────────┬──────────────┘
                                 │
                         ┌───────▼───────┐
                         │  DBAssigner   │
                         │ Shared DB Map │
                         └───────┬───────┘
                                 │
              ┌──────────────────┼──────────────────┐
              │                  │                  │
       ┌──────▼──────┐    ┌──────▼──────┐    ┌──────▼──────┐
       │ Database A  │    │ Database B  │    │ Database C  │
       └──────┬──────┘    └──────┬──────┘    └─────────────┘
              │                  │
        ┌─────▼─────┐      ┌─────▼─────┐
        │    WAL    │      │    WAL    │
        └─────┬─────┘      └───────────┘
              │
        ┌─────▼─────┐
        │ LSM Tree  │
        └─────┬─────┘
              │
       ┌──────┴──────┐
       │             │
  ┌────▼────┐   ┌────▼─────┐
  │MemTable │   │ SSTables │
  │  (AVL)  │   │ L0/L1/L2 │
  └─────────┘   └──────────┘
```
## Storage Engine
### Write Path

```text
INSERT / DELETE
       │
       ▼
      WAL
       │
       ▼
MemTable (AVL Tree)
       │
       │ MemTable reaches threshold
       ▼
   SSTable (L0)
       │
       │ Level reaches capacity
       ▼
   Compaction
       │
       ▼
   L1 / L2 SSTables
```

Deletes are stored as tombstones and handled during reads and compaction

### Read Path
```text
GET key
   │
   ▼
MemTable
   │
   ├── Found ──────────────► Return value
   │
   ▼
Bloom Filter
   │
   ├── Definitely absent ──► Skip SSTable
   │
   ▼
SSTable search
   │
   ├── Tombstone ──────────► Return None
   └── Value found ────────► Return value
```

## Durability and Recovery

NymeriaDB uses two persistence mechanisms.

## Write-Ahead Log

Every write is recorded in the WAL before being applied to the in-memory MemTable.

On restart:

```text
Manifest restores SSTables
          +
WAL replays unflushed writes
          =
Recovered database state
```

## Manifest

The manifest persists SSTable metadata, including:

* SSTable level
* Key range
* File path
* Serialized Bloom filter

This allows the database to rebuild its SSTable structure after restart.

## Multiple Databases

NymeriaDB supports multiple named databases.

A shared DBAssigner ensures that all sessions selecting the same database receive the same live Database instance:

```text
Session A ──┐
            ├── Database("food")
Session B ──┘       │
                    └── Shared MemTable / WAL / LSM Tree
```
This prevents separate sessions from maintaining inconsistent in-memory state.

## Networking

NymeriaDB exposes a TCP server and CLI client.

```text
Client
  │
  │ TCP
  ▼
Server
  │
  ▼
Session Handler
  │
  ▼
DBAssigner
  │
  ▼
Database
```

The database has also been tested remotely from an Android device using Termux.

Example:
```text
NymeriaDB> select food-rating
Database selected: food-rating

NymeriaDB> insert pizza 5
Inserted key: pizza, value: 5

NymeriaDB> get pizza
Value for key pizza: 5

NymeriaDB> delete pizza
Deleted key: pizza
```

## Current Features

- [x] AVL Tree MemTable
- [x] LSM Tree
- [x] SSTables
- [x] Multi-level compaction
- [x] Tombstones for deletes
- [x] Bloom Filters
- [x] Write-Ahead Log (WAL)
- [x] WAL recovery on restart
- [x] Manifest-based SSTable metadata persistence
- [x] Crash recovery
- [x] Multiple named databases
- [x] Shared database instances across sessions
- [x] TCP server
- [x] CLI client
- [x] Remote client connections
- [x] Session handling

## Roadmap

### Database Improvements

- [ ] Concurrent client handling
- [ ] Thread-safe database operations
- [ ] Automated tests
- [ ] Sparse indexing / faster SSTable lookups
- [ ] Background compaction
- [ ] Configurable MemTable and Bloom filter sizes

### Distributed NymeriaDB

- [ ] Multiple database nodes
- [ ] Node discovery
- [ ] Node-to-node communication
- [ ] Request routing
- [ ] Data replication
- [ ] Replication strategy and consistency model
- [ ] Failure detection
- [ ] Leader election / consensus
- [ ] Data sharding / partitioning
- [ ] Distributed recovery and rebalancing

## Project Goal

NymeriaDB is a learning project focused on understanding how database and distributed storage systems work internally by implementing their core components from scratch.