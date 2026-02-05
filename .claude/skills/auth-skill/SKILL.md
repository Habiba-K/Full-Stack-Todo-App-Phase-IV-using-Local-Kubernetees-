---
name: auth-skill
description: Implement secure authentication flows including signup, signin, password hashing, JWT tokens, and Better Auth integration.
---

# Authentication Skill

## Instructions

1. **User registration (Signup)**
   - Validate user input (email, password, username)
   - Enforce strong password rules
   - Prevent duplicate accounts
   - Store users securely in the database

2. **User login (Signin)**
   - Verify credentials against stored hashes
   - Return clear authentication errors
   - Protect against brute-force attacks
   - Maintain consistent response timing

3. **Password hashing**
   - Use modern hashing algorithms (bcrypt, argon2, or scrypt)
   - Apply unique salts per user
   - Never store plain-text passwords
   - Support password rehashing when algorithms change

4. **JWT authentication**
   - Generate signed JWT access tokens
   - Include minimal, non-sensitive claims
   - Set appropriate expiration times
   - Verify tokens on protected routes

5. **Better Auth integration**
   - Configure Better Auth providers
   - Handle session management
   - Support token refresh flows
   - Integrate with frontend auth state

## Best Practices
- Use HTTPS for all auth-related requests
- Apply rate limiting on signup and signin
- Store secrets and keys in environment variables
- Rotate JWT secrets periodically
- Follow least-privilege access control
- Log auth events without exposing sensitive data

## Example Structure
```ts
// Signup
const hashedPassword = await hash(password);

await db.user.create({
  email,
  password: hashedPassword,
});

// Signin
const isValid = await verify(password, user.password);

if (!isValid) throw new Error("Invalid credentials");

// JWT
const token = jwt.sign(
  { userId: user.id },
  process.env.JWT_SECRET,
  { expiresIn: "15m" }
);
