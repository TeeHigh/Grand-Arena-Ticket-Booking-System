# Grand-Arena-Ticket-Booking-System – Design Overview

This project implements a **concurrency-safe ticket reservation system** using FastAPI and PostgreSQL.  
It is designed to handle **high traffic**, **prevent double booking**, and enforce **time-bound seat reservations**.

---

## Core Problem

The system manages a limited number of seats that can be temporarily reserved by users.  
A seat may only be held for **5 minutes**, after which it must automatically become available again if not confirmed.

The system must guarantee:
- No seat is ever double-booked
- Concurrent requests do not corrupt state
- Expired reservations are handled correctly, even under failure or delay

---

## Seat States

Each seat exists in one of the following states:

- **AVAILABLE** – The seat can be reserved
- **RESERVED** – The seat is temporarily held for a user (5-minute window)
- **CONFIRMED** – The seat has been sold and can no longer be reserved

### Valid State Transitions

- AVAILABLE → RESERVED  
- RESERVED → CONFIRMED  
- RESERVED → AVAILABLE (on expiration)

---

## Concurrency and Consistency Guarantees

### Row-Level Locking
All reservation and confirmation operations use **database row-level locks** to ensure that concurrent requests cannot modify the same seat simultaneously.

This guarantees:
- Zero overselling
- Deterministic behavior under high load
- Correct handling of simultaneous requests

### Transactions
All state changes occur within database transactions, ensuring atomicity and consistency even if a request fails midway.

---

## Reservation Expiration Strategy (Defense in Depth)

The system enforces seat expiration using **two complementary mechanisms**:

### 1. Expiry Checks on Access (Correctness)
Whenever a seat is accessed for reservation or confirmation:
- The system checks whether an existing reservation has expired
- Expired reservations are immediately treated as **AVAILABLE**
- This guarantees correctness even if background jobs are delayed

### 2. Background Cleanup Job (Hygiene)
A scheduled background worker periodically:
- Finds expired reservations
- Resets them to **AVAILABLE**
- Keeps seat listings accurate and the database clean

This separation ensures:
- Correct behavior at all times
- Clean and up-to-date availability views

---

## Idempotency Handling

Seat reservation operations are **logically idempotent**:
- If a user retries a reservation request for the same seat, the system returns success without creating duplicate state
- This protects against double clicks and poor network conditions

Explicit idempotency keys are not required for seat reservation, but would be necessary for irreversible operations such as payments.

---

## Architecture Overview

- **Routers** handle HTTP requests and responses
- **Service layer** enforces business rules (expiry, ownership, state transitions)
- **Database layer** guarantees consistency, locking, and persistence
- **Background worker** handles cleanup of expired reservations

This separation keeps the system maintainable, testable, and scalable.

---

## Design Rationale

This project prioritizes:
- Correctness over convenience
- Explicit handling of edge cases
- Real-world backend design patterns

The goal is not just to make the system work, but to demonstrate how high-concurrency systems are designed and reasoned about in production environments.
