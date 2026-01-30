# Architecture: The Actor Model (Actix Style)

**Context**: Managing complex concurrent state where lock contention is high or logic is event-driven.
**Rule**: Encapsulate state within an `Actor`. Interactions happen _only_ via asynchronous messages. This serializes access to state without explicit Mutexes.

## Implementation

```rust
struct DbActor {
    connection: DbConnection,
}

struct QueryMsg(String);
impl Message for QueryMsg { type Result = String; }

impl Handler<QueryMsg> for DbActor {
    type Result = String;

    fn handle(&mut self, msg: QueryMsg, _: &mut Context<Self>) -> Self::Result {
        self.connection.query(&msg.0)
    }
}
```
