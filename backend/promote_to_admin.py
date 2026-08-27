"""
One-off script to promote an existing user to 'admin' role.
Use this because the public /api/auth/register endpoint always
creates 'customer' accounts by design (security choice).

Usage:
    python promote_to_admin.py <username>
"""

import sys
from app import app, db, User

if len(sys.argv) != 2:
    print("Usage: python promote_to_admin.py <username>")
    sys.exit(1)

username = sys.argv[1]

with app.app_context():
    user = User.query.filter_by(username=username).first()

    if not user:
        print(f"No user found with username '{username}'")
        sys.exit(1)

    user.role = 'admin'
    db.session.commit()

    print(f"'{username}' is now an admin.")