# Final Year Viva Questions & Answers

## Technical Questions

**Q1: Why did you choose FastAPI over Flask or Django?**
> **Answer**: FastAPI is asynchronous by default (`async`/`await`), offering higher performance for concurrent AI requests. It also provides automatic Swagger UI documentation, which speeds up development and testing of our REST APIs.

**Q2: What is RAG and why is it used here?**
> **Answer**: RAG (Retrieval Augmented Generation) allows the LLM to access a specific set of external data (our curated course list) before answering. This prevents "hallucinations" (making things up) and ensures students get recommended actual, existing links rather than dead ones.

**Q3: How are the "Reminders" implemented?**
> **Answer**: We use a background task scheduler. In a production environment, we might use Celery + Redis, but for this local prototype, we use `APScheduler` which runs in the same process loop, checking for scheduled notification times without blocking the main thread.

**Q4: Explain how ChromaDB works in your project.**
> **Answer**: ChromaDB is a vector database. It converts text (like "Python tutorial") into mathematical vectors (arrays of numbers). When a user searches "Learn coding", the system compares the vector of the query with the stored vectors using Cosine Similarity to find the closest matches.

## Product/Service Questions

**Q1: How does this differ from just asking ChatGPT?**
> **Answer**: ChatGPT doesn't remember your specific syllabus or progress. Our system maintains a "State of Learning" (checkboxes, completed modules) and specifically constraints its answers to free, high-quality resources we've indexed, filtering out spam or paid content.

**Q2: Can this scale to thousands of users?**
> **Answer**: Currently tailored for local deployment. To scale, we would move the ChromaDB to a cloud instance (e.g., Pinecone or AWS OpenSearch) and deploy the FastAPI backend on a container orchestration platform like Kubernetes.
