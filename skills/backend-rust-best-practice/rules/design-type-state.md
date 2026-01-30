---
title: Type-State Pattern
impact: HIGH
impactDescription: compile-time state machine validation, prevents invalid operations
tags: design, type-system, state-machine, validation
---

## Type-State Pattern

Encode allowed state transitions in the type system to prevent invalid operations at compile time.

**Why this pattern exists:**

1.  **Compile-Time Safety**: Catch invalid state usage before the code runs.
2.  **Self-Documenting Code**: Type signatures clearly define valid operations for each state.
3.  **Elimination of Runtime Checks**: Remove needing to check `if self.state == State::Open` in every method.

**Incorrect (runtime checking):**

```rust
struct Connection {
    state: ConnectionState,  // Runtime check needed everywhere
}

impl Connection {
    fn send(&self, data: &[u8]) -> Result<(), Error> {
        if self.state != ConnectionState::Open {
            return Err(Error::NotConnected);  // Runtime error possible
        }
        // ...
    }
}
```

**Correct (compile-time enforcement):**

```rust
use std::marker::PhantomData;

struct Closed;
struct Open;

struct Connection<State> {
    inner: TcpStream,
    _state: PhantomData<State>,
}

impl Connection<Closed> {
    // Only available when state is Closed
    fn connect(addr: &str) -> Result<Connection<Open>, Error> {
        let stream = TcpStream::connect(addr)?;
        Ok(Connection { inner: stream, _state: PhantomData })
    }
}

impl Connection<Open> {
    // Only available when state is Open
    fn send(&mut self, data: &[u8]) -> Result<(), Error> {
        self.inner.write_all(data)?;
        Ok(())
    }

    fn close(self) -> Connection<Closed> {
        Connection { inner: self.inner, _state: PhantomData }
    }
}

// Usage example
// let conn = Connection::connect("127.0.0.1:8080")?; // Connection<Open>
// conn.send(b"hello")?; // OK
// let conn = conn.close(); // Connection<Closed>
// conn.send(b"fail"); // Compile Error: no method named `send` found for struct `Connection<Closed>`
```

**Real-world application:**

- **Builder Patterns**: Enforcing required fields are set before `build()`.
- **Hardware Drivers**: Ensuring initialization before configuration.
- **Protocol Implementations**: Enforcing state transitions (e.g., Handshake -> Connected -> Authenticated).
