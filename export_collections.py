"""
Export and merge Postman collections from multiple workspaces
"""
import requests
import json
import os
from typing import List, Dict, Optional
from dotenv import load_dotenv
import config

# Load environment variables from .env file
load_dotenv()


def get_all_workspaces() -> List[Dict]:
    """Fetch all workspaces from Postman API"""
    url = f"{config.POSTMAN_API_BASE}/workspaces"
    try:
        response = requests.get(url, headers=config.get_headers(), timeout=config.REQUEST_TIMEOUT)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch workspaces: {response.status_code} - {response.text}")
        return response.json().get("workspaces", [])
    except requests.exceptions.Timeout:
        print("❌ Timeout while fetching workspaces")
        return []
    except Exception as e:
        print(f"❌ Error fetching workspaces: {e}")
        return []


def filter_target_workspaces(all_workspaces: List[Dict]) -> Dict[str, str]:
    """Filter workspaces to only include target workspaces"""
    workspace_map = {}
    for ws in all_workspaces:
        if ws["name"] in config.TARGET_WORKSPACES:
            workspace_map[ws["name"]] = ws["id"]
    
    print(f"\n✅ Found {len(workspace_map)} target workspaces:")
    for name, ws_id in workspace_map.items():
        print(f"   - {name}: {ws_id}")
    
    return workspace_map


def get_collections(workspace_id: str) -> List[Dict]:
    """Get all collections from a workspace"""
    url = f"{config.POSTMAN_API_BASE}/workspaces/{workspace_id}"
    try:
        response = requests.get(url, headers=config.get_headers(), timeout=config.REQUEST_TIMEOUT)
        if response.status_code != 200:
            raise Exception(f"Status {response.status_code}: {response.text}")
        return response.json()["workspace"]["collections"]
    except requests.exceptions.Timeout:
        raise Exception("Request timeout")


def fetch_collection_data(collection_uid: str, collection_name: str) -> Optional[Dict]:
    """Fetch detailed collection data using UID"""
    url = f"{config.POSTMAN_API_BASE}/collections/{collection_uid}"
    try:
        response = requests.get(url, headers=config.get_headers(), timeout=config.REQUEST_TIMEOUT)
        if response.status_code != 200:
            print(f"   ❌ Failed: {collection_name} (Status {response.status_code})")
            return None
        return response.json()["collection"]
    except requests.exceptions.Timeout:
        print(f"   ⏱️ Timeout: {collection_name}")
        return None
    except Exception as e:
        print(f"   ❌ Error: {collection_name} - {e}")
        return None


def merge_selected_workspaces() -> Optional[Dict]:
    """Main function to merge collections from selected workspaces"""
    # Step 1: Get all workspaces
    print("🔍 Fetching all workspaces...")
    all_workspaces = get_all_workspaces()
    
    if not all_workspaces:
        print("❌ No workspaces found or failed to fetch workspaces")
        return None
    
    # Step 2: Filter to target workspaces
    workspace_map = filter_target_workspaces(all_workspaces)
    
    if not workspace_map:
        print(f"❌ None of the target workspaces found: {config.TARGET_WORKSPACES}")
        return None
    
    # Step 3: Export collections from each workspace
    linknet_children = []
    stats = {"total": 0, "success": 0, "failed": 0}

    for folder_name in config.TARGET_WORKSPACES:
        if folder_name not in workspace_map:
            print(f"\n⚠️ Workspace '{folder_name}' not found, skipping...")
            continue
        
        ws_id = workspace_map[folder_name]
        print(f"\n📦 Processing workspace: {folder_name}")
        
        try:
            collections = get_collections(ws_id)
            print(f"   Found {len(collections)} collections")
        except Exception as e:
            print(f"   ❌ Failed to get collections: {e}")
            continue

        subfolder_items = []

        for collection in collections:
            cname = collection["name"]
            cuid = collection.get("uid", collection["id"])  # Use UID if available, fallback to ID
            stats["total"] += 1
            
            print(f"   📥 Downloading: {cname}")
            collection_data = fetch_collection_data(cuid, cname)
            
            if collection_data:
                items = collection_data.get("item", [])
                if items:
                    subfolder_items.append({
                        "name": cname,
                        "item": items
                    })
                    stats["success"] += 1
                    print(f"      ✅ Success")
                else:
                    print(f"      ⚠️ Empty collection")
                    stats["failed"] += 1
            else:
                stats["failed"] += 1
        
        if subfolder_items:
            linknet_children.append({
                "name": folder_name,
                "item": subfolder_items
            })

    # Print statistics
    print(f"\n{'='*50}")
    print(f"📊 Export Statistics:")
    print(f"   Total collections: {stats['total']}")
    print(f"   ✅ Successful: {stats['success']}")
    print(f"   ❌ Failed: {stats['failed']}")
    print(f"{'='*50}")

    return {
        "info": {
            "name": config.ROOT_FOLDER_NAME,
            "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
        },
        "item": [
            {
                "name": config.ROOT_FOLDER_NAME,
                "item": linknet_children
            }
        ]
    }


def save_collection(data: Optional[Dict]) -> None:
    """Save merged collection to JSON file"""
    if not data:
        print("❌ No data to save")
        return
    
    # Create export directory if it doesn't exist
    os.makedirs(config.EXPORT_DIR, exist_ok=True)
    
    output_path = os.path.join(config.EXPORT_DIR, config.COLLECTION_OUTPUT_FILE)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"\n✅ Merged collection saved to: {output_path}")


if __name__ == "__main__":
    print("🔄 Starting Postman collection export...\n")
    merged = merge_selected_workspaces()
    save_collection(merged)
