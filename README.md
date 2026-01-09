# Postman Exporter

A Python tool to export and merge Postman collections and environments from multiple workspaces using the Postman API.

## Motivation

Does your team use the free version of Postman? We do too. With the limit of 3 users per team, sharing and backing up collections became a frequent manual chore. 

The biggest frustration is that **Postman doesn't provide a native "Export All" button**. You are forced to manually export each collection one by one. When you have dozens of collections across multiple workspaces, this is extremely tedious and prone to human error.

I built this tool to solve exactly that problem. It automates the entire process, allowing you to regularly backup **all** your collections and environments from multiple workspaces in seconds, without needing to upgrade to the paid plan just for better data portability.

## Features

- ✅ Export collections from multiple workspaces and merge them into a single file
- ✅ Export all environments to separate JSON files
- ✅ Automatic handling of collection UIDs for proper access
- ✅ Configurable via environment variables
- ✅ Detailed export statistics and error handling
- ✅ Timeout protection for API calls

## Prerequisites

- Python 3.7 or higher
- Postman API Key with appropriate permissions

## Installation

1. Clone or download this repository

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file from the template:
```bash
cp .env.example .env
```

4. Edit `.env` and add your Postman API Key:
```env
POSTMAN_API_KEY=your_actual_api_key_here
```

## Getting Your Postman API Key

1. Go to [Postman Web](https://web.postman.co/)
2. Click on your profile icon → **Settings**
3. Navigate to **API Keys** section
4. Click **Generate API Key**
5. Give it a name (e.g., "Export Script")
6. **Important**: Make sure to select these permissions:
   - ✅ Read collections
   - ✅ Read workspaces
   - ✅ Read environments
7. Copy the generated API key and paste it in your `.env` file

## Configuration

Edit the `.env` file to customize your export settings:

```env
# Required: Your Postman API Key
POSTMAN_API_KEY=your_postman_api_key_here

# Optional: Export directories (defaults shown)
EXPORT_DIR=exports
COLLECTION_OUTPUT_FILE=merged_collection.json
ENVIRONMENT_OUTPUT_DIR=environments

# Optional: Target workspaces (comma-separated)
TARGET_WORKSPACES=Servco DTE,CM,OSS

# Optional: API timeout in seconds
REQUEST_TIMEOUT=30
```

## Usage

### Export Collections

Export and merge collections from specified workspaces:

```bash
python export_collections.py
```

This will:
1. Fetch all workspaces from your Postman account
2. Filter to only the workspaces specified in `TARGET_WORKSPACES`
3. Download all collections from those workspaces
4. Merge them into a single collection file
5. Save to `exports/merged_collection.json`

**Output structure:**
```
Linknet/
├── Servco DTE/
│   ├── Collection 1
│   └── Collection 2
├── CM/
│   └── Collection 3
└── OSS/
    ├── Collection 4
    └── Collection 5
```

### Export Environments

Export all environments to separate JSON files:

```bash
python export_environments.py
```

This will:
1. Fetch all environments from your Postman account
2. Download each environment
3. Save each to a separate JSON file in `exports/environments/`

## Output

After running the scripts, you'll find:

```
postman-exporter/
├── exports/
│   ├── merged_collection.json          # All collections merged
│   └── environments/                    # Individual environment files
│       ├── PROD.json
│       ├── DEV.json
│       └── UAT.json
```

## Troubleshooting

### Error: "POSTMAN_API_KEY is not set"

Make sure you have:
1. Created a `.env` file in the same directory as the scripts
2. Added your API key: `POSTMAN_API_KEY=your_key_here`
3. No spaces around the `=` sign

### Error: 404 - instanceNotFoundError

This means the API key doesn't have permission to access certain collections. Make sure:
1. Your API key has the correct permissions (Read collections, Read workspaces)
2. You have access to the workspaces/collections you're trying to export
3. The collections haven't been deleted or moved

### Collections showing as "Failed"

Some collections may fail if:
- They belong to other users and you don't have access
- They've been deleted
- Your API key doesn't have sufficient permissions

The script will continue and export all accessible collections.

## Security Notes

⚠️ **Important**: 
- Never commit your `.env` file to version control
- The `.gitignore` file is configured to exclude sensitive files
- Keep your API key secure and rotate it regularly
- Exported files may contain sensitive data - handle with care

## API Rate Limits

Postman API has rate limits:
- Free tier: 60 requests per minute
- Paid tier: Higher limits

The script includes timeout protection and will show rate limit information in headers.

## License

MIT License - Feel free to use and modify as needed.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues or questions:
1. Check the Troubleshooting section above
2. Review [Postman API Documentation](https://www.postman.com/postman/workspace/postman-public-workspace/documentation/12959542-c8142d51-e97c-46b6-bd77-52bb66712c9a)
3. Open an issue in this repository
