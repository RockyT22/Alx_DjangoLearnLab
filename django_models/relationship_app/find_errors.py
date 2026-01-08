import re

with open("views.py", "r", encoding="utf-8") as f:
    lines = f.readlines()
    
print("Searching for incorrect permission_required syntax...")
print("=" * 60)

for i, line in enumerate(lines, 1):
    line = line.strip()
    # Look for the wrong pattern
    if "@permission_required(login_url" in line and "relationship_app" in line:
        print(f"Line {i}: {line}")
        print("  ^ This syntax is WRONG!")
        
        # Try to extract the permission name
        match = re.search(r'relationship_app\.(\w+)', line)
        if match:
            perm_name = match.group(1)
            print(f"  Should be: @permission_required('relationship_app.{perm_name}', login_url='/login/')")
        print()
        
print("=" * 60)
print("Done!")
