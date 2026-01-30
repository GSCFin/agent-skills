---
id: data-001-type-safe-dsl
title: Enforce State with Type-Safe DSLs
impact: HIGH
---

# Enforce State with Type-Safe DSLs

## Context

Managing complex state transitions (like "Order Created" -> "Order Paid" -> "Order Shipped") using run-time checks (enums + `if` statements) is error-prone. It allows invalid states to be represented in memory.

## Rule

Use **Zero-Sized Types (ZSTs)** and **Traits** to enforce state transitions at compile time.

1.  Define a trait representing the capability or state (e.g., `OrderState`).
2.  Define ZSTs for each specific state (`Created`, `Paid`).
3.  Store the state in a generic parameter of your main struct.
4.  Implement methods only on the specific state types where they are valid.

## Examples

### Incorrect Code

Runtime checks for state validity.

```rust
struct Order {
    state: String,
    amount: u32,
}

impl Order {
    fn pay(&mut self) {
        if self.state != "Created" {
            panic!("Cannot pay for an order in state {}", self.state);
        }
        self.state = "Paid".to_string();
    }
}
```

### Correct Code

Compile-time state enforcement.

```rust
// States
struct Created;
struct Paid;

// State Machine
struct Order<State> {
    amount: u32,
    _state: std::marker::PhantomData<State>,
}

impl Order<Created> {
    pub fn pay(self) -> Order<Paid> {
        // Transition logic
        Order {
            amount: self.amount,
            _state: std::marker::PhantomData
        }
    }
}

// Usage
// let order = Order::new();
// let paid_order = order.pay(); // OK
// let double_paid = paid_order.pay(); // Compile Error!
```

## Champion Project: Diesel

Diesel uses this pattern to enforce SQL correctness. For example, you cannot call `.filter()` on a query that has already been turned into a specific SQL command, or mix types that don't match (comparing an Integer column to a String value).
