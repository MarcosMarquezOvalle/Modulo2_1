from __future__ import annotations

import crud
import database


def main():
    # 1. Initialize the database schema
    database.init_db()
    print("Database initialized successfully.\n")

    # 2. CREATE - Add new entries
    print("--- Creating Users ---")
    session = database.get_session()
    user1_id = crud.create_user(session, "Alice Smith", "alice@example.com")
    user2_id = crud.create_user(session, "Bob Jones", "bob@example.com")
    print(f"Added Alice with ID: {user1_id}")
    print(f"Added Bob with ID: {user2_id}\n")

    # 3. READ - Display current state
    print("--- Current Database Records ---")
    users = crud.list_users(session)
    for user in users:
        print(f"[{user.id}] Name: {user.name} | Email: {user.email}")
    print()

    # 4. UPDATE - Modify an entry
    print("--- Updating Alice's Email ---")
    if crud.update_user(session, user1_id.id, email="alice.smith@newdomain.com"):
        print("Update successful!")
    print()

    # 5. DELETE - Remove an entry
    print("--- Deleting Bob's Record ---")
    if crud.delete_user(session, user2_id.id):
        print("Deletion successful!\n")

    # 6. READ - Verify final state
    print("--- Final Database Records ---")
    remaining_users = crud.list_users(session)
    for user in remaining_users:
        print(f"[{user.id}] Name: {user.name} | Email: {user.email}")


if __name__ == "__main__":
    main()
