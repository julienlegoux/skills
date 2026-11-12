---
type: llm
weight: 2
---

The user is a baker with no technical background who gave a one-line request. A successful response:

- asks about the need: who places or handles the orders, how orders are handled today, or what "working" would look like for the bakery;
- asks NO question the baker would need explained first — nothing about programming languages, frameworks, databases, hosting, architecture, APIs or repositories;
- is written in French, in plain words.

Asking which device they would use it on (phone, tablet, computer) is a question about the need, not a technical one, and is fine.

Fail if a technical choice is put to the user as a question, or if the response talks about files, folders or the repository.
