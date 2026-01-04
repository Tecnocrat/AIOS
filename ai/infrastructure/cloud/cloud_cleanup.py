#!/usr/bin/env python3
"""
AIOS Cloud Cleanup Agent v1.0
AINLP.context[ACTIVE] - Cloud Substrate Sterilization Tool
AINLP.bridge[FIRESTORE] - Logging candidate projects

Genesis Protocol: Apoptosis of deprecated cloud projects
to prepare canonical environment for GCloud organ integration.

Usage:
    python cloud_cleanup.py scan     # Phase 1: Inventory to Firestore
    python cloud_cleanup.py purge    # Phase 2: Delete APPROVED projects
    python cloud_cleanup.py status   # Check current state
"""

import argparse
import sys
from datetime import datetime
from typing import List, Dict, Any

try:
    from google.cloud import resourcemanager_v3
    from google.cloud import firestore
    from google.api_core import exceptions as gcp_exceptions
except ImportError:
    print("❌ Missing dependencies. Run:")
    print("   pip install google-cloud-resource-manager google-cloud-firestore")
    sys.exit(1)

# AINLP.membrane: Import temporal substrate translation
try:
    from aios_schema.temporal import to_iso_string
except ImportError:
    # Fallback if aios-schema not installed
    def to_iso_string(value):
        """Fallback temporal translation."""
        if value is None:
            return None
        if hasattr(value, 'ToDatetime'):
            return value.ToDatetime().isoformat() + "Z"
        if hasattr(value, 'isoformat'):
            return value.isoformat() + "Z"
        return str(value)


# =============================================================================
# AIOS Protected Genome (NEVER DELETE)
# =============================================================================

PROTECTED_PROJECTS = [
    "gen-lang-client-0072186287",  # Gemini API (AIOS Brain)
    "aios-28728220",               # Firebase (AIOS Memory)
    "sys-28728220",                # System level protection
    "aios-win",                    # If exists as project
]

FIRESTORE_PROJECT = "aios-28728220"
COLLECTION_NAME = "cleanup_candidates"


# =============================================================================
# Scanner Phase (Dendritic Analysis)
# =============================================================================

def scan_projects() -> List[Dict[str, Any]]:
    """
    AINLP.dendritic: Scan all accessible GCP projects.
    Returns list of project metadata.
    """
    print("🔍 AIOS Genesis Protocol - Scanning cloud substrate...")
    print(f"   Protected genome: {PROTECTED_PROJECTS}")

    rm_client = resourcemanager_v3.ProjectsClient()
    request = resourcemanager_v3.SearchProjectsRequest()

    projects = []
    try:
        for project in rm_client.search_projects(request=request):
            # AINLP.membrane[TEMPORAL]: Use unified substrate translation
            project_data = {
                "project_id": project.project_id,
                "display_name": project.display_name,
                "state": str(project.state).rsplit(".", maxsplit=1)[-1],  # Extract enum name
                "create_time": to_iso_string(project.create_time),
                "is_protected": project.project_id in PROTECTED_PROJECTS,
            }
            projects.append(project_data)

            status = "🛡️ PROTECTED" if project_data["is_protected"] else "⚠️ CANDIDATE"
            print(f"   {status}: {project.project_id} ({project.display_name})")

    except gcp_exceptions.PermissionDenied as e:
        print(f"❌ Permission denied: {e}")
        print("   Run: gcloud auth application-default login")
        raise

    print(f"\n📊 Found {len(projects)} projects total")
    return projects


def log_to_firestore(projects: List[Dict[str, Any]]) -> int:
    """
    AINLP.tachyonic: Persist inventory to Firestore for human review.
    """
    print(f"\n📝 Logging to Firestore: {FIRESTORE_PROJECT}/{COLLECTION_NAME}")

    db = firestore.Client(project=FIRESTORE_PROJECT)
    collection = db.collection(COLLECTION_NAME)

    batch = db.batch()
    count = 0

    for project in projects:
        project_id = project["project_id"]

        # Determine initial status
        if project["is_protected"]:
            status = "PROTECTED"
        elif project["state"] == "DELETE_REQUESTED":
            status = "ALREADY_DELETING"
        else:
            status = "PENDING_REVIEW"

        doc_ref = collection.document(project_id)
        batch.set(doc_ref, {
            "project_id": project_id,
            "display_name": project["display_name"],
            "state": project["state"],
            "create_time": project["create_time"],
            "status": status,
            "scan_timestamp": firestore.SERVER_TIMESTAMP,
            "scanned_by": "AIOS Genesis Protocol v1.0",
        })
        count += 1

    batch.commit()
    print(f"✅ Logged {count} projects to Firestore")
    print("\n👉 Next steps:")
    print(f"   1. Open: https://console.firebase.google.com/project/{FIRESTORE_PROJECT}/firestore")
    print(f"   2. Navigate to collection: {COLLECTION_NAME}")
    print("   3. Change 'status' to 'APPROVED' for projects to delete")
    print("   4. Run: python cloud_cleanup.py purge")

    return count


# =============================================================================
# Purge Phase (Apoptosis)
# =============================================================================

def get_approved_projects() -> List[Dict[str, Any]]:
    """
    AINLP.logic: Fetch projects marked APPROVED in Firestore.
    """
    db = firestore.Client(project=FIRESTORE_PROJECT)
    collection = db.collection(COLLECTION_NAME)

    # Query for approved projects
    approved = collection.where("status", "==", "APPROVED").stream()

    projects = []
    for doc in approved:
        data = doc.to_dict()
        # Double-check protection (defense in depth)
        if data["project_id"] not in PROTECTED_PROJECTS:
            projects.append(data)
        else:
            print(f"⚠️ BLOCKED: {data['project_id']} is in protected genome!")

    return projects


def delete_project(project_id: str) -> bool:
    """
    AINLP.apoptosis: Delete a single GCP project.
    """
    rm_client = resourcemanager_v3.ProjectsClient()

    try:
        # GCP project names are in format: projects/{project_id}
        name = f"projects/{project_id}"
        operation = rm_client.delete_project(name=name)

        # Wait for operation to complete
        print(f"   ⏳ Deletion initiated for {project_id}...")
        operation.result()  # Blocks until complete

        return True

    except gcp_exceptions.NotFound:
        print(f"   ⚠️ Project {project_id} not found (already deleted?)")
        return True

    except gcp_exceptions.PermissionDenied:
        print(f"   ❌ Permission denied for {project_id}")
        return False

    except gcp_exceptions.GoogleAPICallError as e:
        print(f"   ❌ Error deleting {project_id}: {e}")
        return False


def update_firestore_status(project_id: str, status: str) -> None:
    """Update project status in Firestore."""
    db = firestore.Client(project=FIRESTORE_PROJECT)
    doc_ref = db.collection(COLLECTION_NAME).document(project_id)
    doc_ref.update({
        "status": status,
        "updated_at": firestore.SERVER_TIMESTAMP,
    })


def purge_approved() -> Dict[str, int]:
    """
    AINLP.apoptosis: Execute deletion of all APPROVED projects.
    """
    print("\n☠️ AIOS Genesis Protocol - Purge Phase")
    print("   Fetching APPROVED projects from Firestore...")

    approved = get_approved_projects()

    if not approved:
        print("   ✅ No projects approved for deletion.")
        return {"deleted": 0, "failed": 0}

    print(f"   Found {len(approved)} projects approved for deletion:")
    for p in approved:
        print(f"      - {p['project_id']} ({p['display_name']})")

    # Confirmation prompt
    print("\n⚠️ WARNING: This action is IRREVERSIBLE!")
    confirm = input("   Type 'CONFIRM APOPTOSIS' to proceed: ")

    if confirm != "CONFIRM APOPTOSIS":
        print("   ❌ Aborted. No projects deleted.")
        return {"deleted": 0, "failed": 0}

    # Execute deletions
    deleted = 0
    failed = 0

    for project in approved:
        project_id = project["project_id"]
        print(f"\n🗑️ Deleting: {project_id}")

        if delete_project(project_id):
            update_firestore_status(project_id, "DELETED")
            deleted += 1
            print(f"   ✅ Deleted: {project_id}")
        else:
            update_firestore_status(project_id, "DELETION_FAILED")
            failed += 1

    print(f"\n📊 Purge complete: {deleted} deleted, {failed} failed")
    return {"deleted": deleted, "failed": failed}


# =============================================================================
# Status Check
# =============================================================================

def check_status() -> None:
    """
    AINLP.status: Display current cleanup state from Firestore.
    """
    print("\n📊 AIOS Genesis Protocol - Status Report")

    db = firestore.Client(project=FIRESTORE_PROJECT)
    collection = db.collection(COLLECTION_NAME)

    # Count by status
    status_counts = {}
    for doc in collection.stream():
        data = doc.to_dict()
        status = data.get("status", "UNKNOWN")
        status_counts[status] = status_counts.get(status, 0) + 1

    if not status_counts:
        print("   No projects in inventory. Run: python cloud_cleanup.py scan")
        return

    print("\n   Status breakdown:")
    for status, count in sorted(status_counts.items()):
        emoji = {
            "PROTECTED": "🛡️",
            "PENDING_REVIEW": "⏳",
            "APPROVED": "✅",
            "DELETED": "☠️",
            "DELETION_FAILED": "❌",
            "ALREADY_DELETING": "⏳",
        }.get(status, "❓")
        print(f"      {emoji} {status}: {count}")

    total = sum(status_counts.values())
    print(f"\n   Total: {total} projects tracked")


# =============================================================================
# CLI Entry Point
# =============================================================================

def main():
    """CLI entry point for AIOS Cloud Cleanup Agent."""
    parser = argparse.ArgumentParser(
        description="AIOS Genesis Protocol - Cloud Cleanup Agent",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cloud_cleanup.py scan    # Inventory all projects to Firestore
  python cloud_cleanup.py status  # Check current state
  python cloud_cleanup.py purge   # Delete APPROVED projects

Safety:
  Protected projects are NEVER deleted:
    - gen-lang-client-0072186287 (Gemini API)
    - aios-28728220 (Firebase)
    - sys-28728220 (System)
        """
    )

    parser.add_argument(
        "command",
        choices=["scan", "purge", "status"],
        help="Command to execute"
    )

    args = parser.parse_args()

    print("=" * 60)
    print("AIOS Genesis Protocol v1.0 - Cloud Substrate Sterilization")
    print("=" * 60)
    print(f"Timestamp: {datetime.utcnow().isoformat()}Z")
    print(f"Firestore: {FIRESTORE_PROJECT}/{COLLECTION_NAME}")

    if args.command == "scan":
        projects = scan_projects()
        log_to_firestore(projects)

    elif args.command == "purge":
        purge_approved()

    elif args.command == "status":
        check_status()


if __name__ == "__main__":
    main()
