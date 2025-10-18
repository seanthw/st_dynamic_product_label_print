import sys
import os

def update_manifest_version(version):
    manifest_path = '__manifest__.py'
    if not os.path.exists(manifest_path):
        print(f"Error: {manifest_path} not found.")
        sys.exit(1)

    new_lines = []
    version_updated = False
    with open(manifest_path, 'r', encoding='utf-8') as f:
        for line in f:
            if "'version'" in line:
                # This assumes the version is on its own line.
                # The indentation and comma are hardcoded to match the existing style.
                new_lines.append(f"    'version': '{version}',\n")
                version_updated = True
            else:
                new_lines.append(line)

    if not version_updated:
        # If 'version' key was not found, we'll insert it after the 'name' key.
        final_lines = []
        for line in new_lines:
            final_lines.append(line)
            if "'name'" in line:
                final_lines.append(f"    'version': '{version}',\n")
        new_lines = final_lines

    with open(manifest_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

    print(f"Successfully updated __manifest__.py to version {version}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python update_manifest_version.py <new_version>")
        sys.exit(1)
    
    new_version = sys.argv[1]
    update_manifest_version(new_version)