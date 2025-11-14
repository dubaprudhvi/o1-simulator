from utils.imports import *

def read_config(app: str, config_file=CONFIG_PATH):
    config_path = Path(config_file)
    if not config_path.exists():
        return {}
    
    try:
        with open(config_file, 'r') as f:
            config_data = json.load(f)
        return config_data.get(app, {})
    except (json.JSONDecodeError, IOError) as e:
        print(f"Warning: Could not read config file: {e}")
        return {}

def update_config(config, app, config_file=CONFIG_PATH):
    config_data = {}
    config_path = Path(config_file)
    
    if config_path.exists():
        try:
            with open(config_file, 'r') as f:
                config_data = json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Could not read config file: {e}")
            config_data = {}
    
    config_data[app] = config
    
    try:
        with open(config_file, 'w') as f:
            json.dump(config_data, f, indent=4)
    except IOError as e:
        print(f"Error: Could not write to config file: {e}")

def view_config(app: str):
    config = read_config(app)
    
    print("\n" + "-"*12)
    print(f"{app} CONFIGURATION")
    print("-"*12)
    
    if not config:
        print(f"No {app} configuration found.")
    else:
        for key, value in config.items():
            print(f"{key:15}: {value}")
    
    print("-"*12)
    input("\nPress Enter to continue...")

def edit_config(app: str):
    current_config = read_config(app)
    
    print("\n" + "-"*12)
    print(f"EDIT {app} CONFIGURATION")
    print("-"*12)
    
    if not current_config:
        print(f"No existing {app} configuration found.")
        input("Press Enter to continue...")
        return
    
    updated_config = current_config.copy()
    
    existing_keys = list(current_config.keys())
    
    print("Edit existing keys (press Enter to keep current value):")
    for key in existing_keys:
        current_value = current_config.get(key, '')
        new_value = input(f"{key:15} [Current: {current_value}]: ").strip()
        if new_value:
            updated_config[key] = new_value
    
    update_config(updated_config, app)
    print(f"\n✓ {app} configuration updated successfully!")
    
    changes_made = False
    for key in existing_keys:
        old_value = current_config.get(key, '')
        new_value = updated_config.get(key, '')
        if old_value != new_value:
            print(f"  Changed: {key} = {old_value} → {new_value}")
            changes_made = True
    
    if not changes_made:
        print("  No changes were made.")
    
    input("\nPress Enter to continue...")