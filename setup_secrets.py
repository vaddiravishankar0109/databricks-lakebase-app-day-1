"""
One-time setup script: creates the Databricks secret scope and stores the
Massive API key. Run this locally (with the Databricks CLI configured) or
from a notebook - never commit the resulting secret value anywhere.

Usage:
    python setup_secrets.py
"""
from databricks.sdk import WorkspaceClient
from databricks.sdk.service import workspace
from databricks.sdk.errors import ResourceAlreadyExists
import getpass

w = WorkspaceClient()

# Handle 'massive' scope - delete and recreate if exists
try:
    w.secrets.create_scope(scope="massive")
    print("Created scope 'massive'")
except ResourceAlreadyExists:
    print("Scope 'massive' already exists, deleting and recreating...")
    w.secrets.delete_scope(scope="massive")
    w.secrets.create_scope(scope="massive")
    print("Recreated scope 'massive'")

w.secrets.put_secret(
    scope="massive",
    key="api-key",
    string_value=getpass.getpass("Paste your Massive API key: ")
)

# Handle 'database' scope - delete and recreate if exists
try:
    w.secrets.create_scope(scope="database")
    print("Created scope 'database'")
except ResourceAlreadyExists:
    print("Scope 'database' already exists, deleting and recreating...")
    w.secrets.delete_scope(scope="database")
    w.secrets.create_scope(scope="database")
    print("Recreated scope 'database'")

w.secrets.put_secret(
    scope="database",
    key="lakebase-url",
    string_value=getpass.getpass("Paste your Lakebase URL: ")
)


w.secrets.put_acl(
    scope="database",
    principal="users",
    permission=workspace.AclPermission.READ,
)

w.secrets.put_acl(
    scope="massive",
    principal="users",
    permission=workspace.AclPermission.READ,
)
