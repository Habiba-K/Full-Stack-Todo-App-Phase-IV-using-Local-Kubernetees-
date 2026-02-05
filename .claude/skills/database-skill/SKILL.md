---
name: database-skill
description: Create and manage database tables, migrations, and schema design. Use for PostgreSQL and relational database development.
---

# Database Skill – Tables, Migrations, Schema Design

## Instructions

1. **Schema Design**
   - Design normalized, scalable schemas
   - Choose appropriate data types
   - Define primary keys and relationships
   - Apply constraints (NOT NULL, UNIQUE, CHECK)

2. **Table Creation**
   - Write clear and maintainable `CREATE TABLE` statements
   - Use naming conventions consistently
   - Add indexes for frequently queried columns
   - Include timestamps (`created_at`, `updated_at`) where appropriate

3. **Migrations**
   - Create forward and rollback migrations
   - Ensure migrations are idempotent and safe
   - Separate schema changes from data migrations
   - Maintain migration order and versioning

4. **Relationships**
   - Implement foreign keys correctly
   - Define cascade rules thoughtfully
   - Avoid unnecessary joins
   - Optimize for query patterns

## Best Practices
- Prefer explicit schemas over implicit behavior
- Avoid premature optimization, but index wisely
- Keep migrations small and reversible
- Document schema changes clearly
- Test migrations on staging before production
- Design with future scalability in mind

## Example Structure
```sql
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email TEXT NOT NULL UNIQUE,
  password_hash TEXT NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

CREATE INDEX idx_users_email ON users(email);
