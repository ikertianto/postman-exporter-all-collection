"""
Export all Postman environments
"""
import requests
import json
import os
from typing import List, Dict
from dotenv import load_dotenv
import config

# Load environment variables from .env file
load_dotenv()


def list_environments() -> List[Dict]:
    """List all environments from Postman API"""
    url = f"{config.POSTMAN_API_BASE}/environments"
    try:
        response = requests.get(url, headers=config.get_headers(), timeout=config.REQUEST_TIMEOUT)
        if response.status_code != 200:
            raise Exception(f"❌ Failed to list environments:\n{response.status_code} - {response.text}")
        return response.json()["environments"]
    except Exception as e:
        print(f"❌ Error listing environments: {e}")
        return []


def export_environments() -> None:
    """Export each environment to a separate JSON file"""
    envs = list_environments()
    
    if not envs:
        print("⚠️ No environments found")
        return
    
    # Create output directory
    output_dir = os.path.join(config.EXPORT_DIR, config.ENVIRONMENT_OUTPUT_DIR)
    os.makedirs(output_dir, exist_ok=True)
    
    stats = {"total": len(envs), "success": 0, "failed": 0}

    for env in envs:
        env_name = env["name"]
        env_uid = env["uid"]
        print(f"📥 Exporting: {env_name}")

        url = f"{config.POSTMAN_API_BASE}/environments/{env_uid}"
        try:
            response = requests.get(url, headers=config.get_headers(), timeout=config.REQUEST_TIMEOUT)

            if response.status_code == 200:
                data = response.json()["environment"]
                filename = f"{env_name}.json".replace(" ", "_")
                path = os.path.join(output_dir, filename)
                
                with open(path, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2)
                
                print(f"   ✅ Saved: {path}")
                stats["success"] += 1
            else:
                print(f"   ❌ Failed to fetch: {env_name}")
                print(f"      Status: {response.status_code}")
                print(f"      Body: {response.text}")
                stats["failed"] += 1
        except Exception as e:
            print(f"   ❌ Error: {env_name} - {e}")
            stats["failed"] += 1
    
    # Print statistics
    print(f"\n{'='*50}")
    print(f"📊 Export Statistics:")
    print(f"   Total environments: {stats['total']}")
    print(f"   ✅ Successful: {stats['success']}")
    print(f"   ❌ Failed: {stats['failed']}")
    print(f"{'='*50}")


if __name__ == "__main__":
    print("🔄 Exporting all environments...\n")
    export_environments()
    print("\n✅ Done.")
