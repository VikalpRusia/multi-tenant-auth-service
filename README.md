# Auth Service for Multi tenant SAAS - Backend

## Problem Statement

### Tables

Please create these tables in PostgreSQL or MySQL using any migration tools. You can find the table schema on the last
page of this document.

**Tables:**

- User
- Organization
- Member
- Role

#### Relationships

- One User is part of Many Organizations.
- The Member table is a Many-to-Many mapping table.
- A User has a Role in an Organization.

#### Table Schema

##### Organization

- `name` = String, `nullable=False`
- `status` = Integer, `default=0`, `nullable=False`
- `personal` = Boolean, `default=False`, `nullable=True`
- `settings` = JSON, `default={}`, `nullable=True`
- `created_at` = BigInteger, `nullable=True`
- `updated_at` = BigInteger, `nullable=True`

##### User

- `email` = String, `unique=True`, `nullable=False`
- `password` = String, `nullable=False`
- `profile` = JSON, `default={}`, `nullable=False`
- `status` = Integer, `default=0`, `nullable=False`
- `settings` = JSON, `default={}`, `nullable=True`
- `created_at` = BigInteger, `nullable=True`
- `updated_at` = BigInteger, `nullable=True`

##### Member

- `org_id` = Integer, `ForeignKey("organization.id")`, `ondelete="CASCADE"`, `nullable=False`
- `user_id` = Integer, `ForeignKey("user.id")`, `ondelete="CASCADE"`, `nullable=False`
- `role_id` = Integer, `ForeignKey("role.id")`, `ondelete="CASCADE"`, `nullable=False`
- `status` = Integer, `nullable=False`, `default=0`
- `settings` = JSON, `default={}`, `nullable=True`
- `created_at` = BigInteger, `nullable=True`
- `updated_at` = BigInteger, `nullable=True`

##### Role

- `name` = String, `nullable=False`
- `description` = String, `nullable=True`
- `org_id` = Integer, `ForeignKey("organization.id")`, `ondelete="CASCADE"`, `nullable=False`

### APIs

Write the APIs below in any Python server framework. Test different scenarios and send us a GitHub repo link along with
the Postman export collection.

1. **Sign In**
    - Verify User encrypted password in User table.
    - Return a JWT Token (Access token and Refresh token).

2. **Sign Up**
    - Add a user entry.
    - Create a new organization (Get organization name and details as input).
    - Add a member entry with owner role.

3. **Reset Password**

4. **Invite Member**

5. **Delete Member**

6. **Update Member Role**

### APIs for Stats

1. Role-wise number of users.
2. Organization-wise number of members.
3. Organization-wise role-wise number of users.
4. Add "from" and "to" time filters and status filters to both APIs 3 and 4.

### Email APIs Test

Use any Email API (Twilio, Resend, Brevo, etc.). The choice of Email API is left to the candidate.

1. Send an invite email on sign up and invite with a generated link.
2. Send a password update alert email.
3. Send a login alert event email.

