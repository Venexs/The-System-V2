from sympy import im
import ujson
from datetime import datetime, timedelta
import os
import random
from PIL import Image, ImageTk
import math
import time
import subprocess


import thesystem
import sfx
import thesystem.system

def get_weekly_night_market_data():
    """
    Get weekly night market data with automatic weekly management.
    
    This function handles the complete weekly data lifecycle:
    - Checks if it's a new week (Monday-based)
    - Creates new data if it's a new week
    - Returns existing data if it's the same week
    - Stores data in Player Data directory as JSON
    
    Weekly Reset Logic:
    - New week = Monday (weekday 0)
    - Week key format: "YYYY-MM-DD" (Monday's date)
    - Data structure includes rank items (S, B, C, D) with rarity info
    - Items are filtered by rarity (Common, Rare, Epic, Legendary)
    
    Returns:
        dict: Weekly night market data with structure:
        {
            "week_key": "YYYY-MM-DD",           # Monday's date as week identifier
            "created_date": "YYYY-MM-DD HH:MM:SS", # When this week's data was created
            "week_start": "YYYY-MM-DD",         # Monday's date
            "last_updated": "YYYY-MM-DD HH:MM:SS", # Last time data was accessed
            "rank_items": {
                "S": {"item_name": {"rarity": "Common/Rare/Epic/Legendary", "data": {...}}},
                "B": {...},
                "C": {...},
                "D": {...}
            }
        }
    """
    # File path for storing weekly data in Player Data directory
    file_path = "Files/Player Data/Night_Market_Weekly.json"
    
    # Calculate current week's Monday date for week identification
    # Current weekday (0=Monday, 6=Sunday)
    today = datetime.now()
    weekday = today.weekday()

    # Calculate how many days since last Sunday
    days_since_sunday = (weekday + 1) % 7
    sunday = today - timedelta(days=days_since_sunday)
    sunday = sunday.replace(hour=0, minute=0, second=0, microsecond=0)

    current_week_key = sunday.strftime("%Y-%m-%d")
    
    # Check if weekly data file exists
    if os.path.exists(file_path):
        try:
            # Load existing weekly data
            with open(file_path, 'r') as f:
                raw = f.read().strip()
                if not raw:  # empty file
                    raise ValueError("Empty file")
                stored_data = ujson.loads(raw)
            
            stored_week_key = stored_data.get("week_key")
            
            if stored_week_key == current_week_key:
                # Same week - return existing data and update timestamp
                stored_data["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                with open(file_path, 'w') as f:
                    ujson.dump(stored_data, f, indent=4)
                return stored_data
            else:
                # New week - create fresh data
                return _create_new_weekly_data(current_week_key, sunday)

        except Exception as e:
            print(f"Error loading night market data: {e} — resetting file.")
            return _create_new_weekly_data(current_week_key, sunday)
    else:
        # File doesn't exist - create new data
        return _create_new_weekly_data(current_week_key, sunday)

def _select_items_by_rarity(candidates, rarity_config):
    """
    Select items based on percentage-based rarity system.
    Ensures each rank gets exactly 1 item by falling back to Common if needed.
    
    Args:
        candidates (dict): All available items for a rank
        rarity_config (dict): How many items to select per rarity
    
    Returns:
        dict: Selected items based on rarity
    """
    selected_items = {}
    
    # Group candidates by rarity
    rarity_groups = {"Common": [], "Rare": [], "Epic": [], "Legendary": []}
    
    for item_name, item_info in candidates.items():
        rarity = item_info["rarity"]
        if rarity in rarity_groups:
            rarity_groups[rarity].append((item_name, item_info))
    
    # Rarity percentages (total = 100%)
    rarity_percentages = {
        "Common": 50,    # 50% chance
        "Rare": 30,      # 30% chance
        "Epic": 15,      # 15% chance
        "Legendary": 5   # 5% chance
    }
    
    # Generate random number for rarity selection
    rand_value = random.randint(1, 100)
    
    # Determine which rarity to select based on percentages
    cumulative_percentage = 0
    selected_rarity = "Common"  # Default fallback
    
    for rarity, percentage in rarity_percentages.items():
        cumulative_percentage += percentage
        if rand_value <= cumulative_percentage:
            selected_rarity = rarity
            break
    
    # Try to select 1 item from the chosen rarity
    available_items = rarity_groups.get(selected_rarity, [])
    
    if available_items:
        # Select 1 item from the chosen rarity
        selected = random.sample(available_items, 1)
        
        # Add selected item to result
        for item_name, item_info in selected:
            selected_items[item_name] = item_info
    else:
        # Fallback to Common if chosen rarity has no items
        common_items = rarity_groups.get("Common", [])
        if common_items:
            selected = random.sample(common_items, 1)
            for item_name, item_info in selected:
                selected_items[item_name] = item_info
        else:
            # If even Common is empty, take any available item
            all_items = []
            for items in rarity_groups.values():
                all_items.extend(items)
            
            if all_items:
                selected = random.sample(all_items, 1)
                for item_name, item_info in selected:
                    selected_items[item_name] = item_info
    
    return selected_items

# Legacy function for backward compatibility
def _create_new_weekly_data(week_key, monday_date):
    """
    Internal function to create new weekly night market data.
    
    Args:
        week_key (str): Week identifier (Monday's date)
        monday_date (datetime): Monday's datetime object
    
    Returns:
        dict: New weekly data with rank items and metadata
    """
    # Load inventory data to get rank items
    try:
        with open("Files/Data/Inventory_List.json", 'r') as f:
            inventory_data = ujson.load(f)
    except Exception as e:
        print(f"Error loading inventory data: {e}")
        inventory_data = {}
    
    # Initialize rank items structure
    rank_items = {"S": {}, "B": {}, "C": {}, "D": {}}
    
    # Rarity-based selection configuration - 1 item per rank with flexible rarity
    rarity_config = {
        "S": {"Common": 0, "Rare": 0, "Epic": 0, "Legendary": 1},  # S-rank: 1 Legendary item
        "B": {"Common": 0, "Rare": 0, "Epic": 1, "Legendary": 0},  # B-rank: 1 Epic item
        "C": {"Common": 0, "Rare": 1, "Epic": 0, "Legendary": 0},  # C-rank: 1 Rare item
        "D": {"Common": 1, "Rare": 0, "Epic": 0, "Legendary": 0}   # D-rank: 1 Common item
    }
    
    # Process each rank separately
    for rank in ["S", "B", "C", "D"]:
        # Collect all items for this rank
        rank_candidates = {}
        for item_name, item_data in inventory_data.items():
            if item_data and len(item_data) > 0:
                item = item_data[0]
                item_rank = item.get("rank")
                
                if item_rank == rank:
                    rarity = item.get("rarity", "Common")
                    if item_name not in rank_candidates:
                        rank_candidates[item_name] = {
                            "rarity": rarity,
                            "data": item
                        }
        
        # Select items based on percentage-based rarity system
        selected_items = _select_items_by_rarity(rank_candidates, rarity_config[rank])
        
        # Apply 10% discount to selected items
        for sel_name, sel_item in selected_items.items():
            if "Value" in sel_item["data"]:
                original_val = sel_item["data"]["Value"]
                discounted_val = math.floor(original_val * 0.75)  # 25% off
                sel_item["data"]["Value"] = discounted_val
                sel_item["data"]["bought"] = False
        
        rank_items[rank] = selected_items
    
    # Create comprehensive weekly data structure
    weekly_data = {
        "week_key": week_key,
        "created_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "week_start": monday_date.strftime("%Y-%m-%d"),
        "rank_items": rank_items,
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # Save to Player Data directory
    try:
        with open("Files/Player Data/Night_Market_Weekly.json", 'w') as f:
            ujson.dump(weekly_data, f, indent=4)
    except Exception as e:
        print(f"Error saving night market data: {e}")
    
    return weekly_data

def buy_item(item_name: str, price: int, window):
    """
    Attempt to buy an item by name and price.

    Steps:
    - Check if player has enough coins in Status.json
    - Deduct coins if possible
    - Add the item (from Inventory_List.json) into Inventory.json
    - Mark the item as bought in Night_Market_Weekly.json
    - Save all changes

    Args:
        item_name (str): The item to purchase
        price (int): The cost of the item

    Returns:
        dict: {"success": True/False, "message": str}
    """

    threading.Thread(target=sfx.button(), daemon=True).start()

    status_file = "Files/Player Data/Status.json"
    inventory_list_file = "Files/Data/Inventory_List.json"
    player_inventory_file = "Files/Player Data/Inventory.json"
    night_market_file = "Files/Player Data/Night_Market_Weekly.json"

    # Load status data
    if not os.path.exists(status_file):
        return {"success": False, "message": "Status.json not found"}
    with open(status_file, 'r') as f:
        status_data = ujson.load(f)

    player_status = status_data["status"][0]  # first entry holds stats
    coins = player_status.get("coins", 0)

    # Check coin balance
    if coins < price:
        thesystem.system.message_open("Insufficient Funds")
        return {"success": False, "message": "Insufficient Funds"}

    # Load inventory list (shop items)
    if not os.path.exists(inventory_list_file):
        return {"success": False, "message": "Inventory_List.json not found"}
    with open(inventory_list_file, 'r') as f:
        inventory_list = ujson.load(f)

    if item_name not in inventory_list:
        return {"success": False, "message": f"Item '{item_name}' not found in inventory list"}

    # Deduct coins
    player_status["coins"] = coins - price

    # Save updated status
    with open(status_file, 'w') as f:
        ujson.dump(status_data, f, indent=4)

    # Load player inventory (owned items)
    if os.path.exists(player_inventory_file):
        with open(player_inventory_file, 'r') as f:
            player_inventory = ujson.load(f)
    else:
        player_inventory = {}

    # Add item into player inventory
    item_data = inventory_list[item_name][0]  # first (and only) dict entry
    if item_name not in player_inventory:
        player_inventory[item_name] = [item_data]
    else:
        # If item already exists, increase qty
        player_inventory[item_name][0]["qty"] += 1

    # Save updated player inventory
    with open(player_inventory_file, 'w') as f:
        ujson.dump(player_inventory, f, indent=4)

    # --- Update Night_Market_Weekly.json ---
    if os.path.exists(night_market_file):
        with open(night_market_file, 'r') as f:
            night_market = ujson.load(f)

        found = False
        for rank, items in night_market.get("rank_items", {}).items():
            if item_name in items:
                items[item_name]["data"]["bought"] = True
                found = True
                break

        if found:
            # Save updated night market data
            with open(night_market_file, 'w') as f:
                ujson.dump(night_market, f, indent=4)

    thesystem.system.message_open("Purchase Confirmed")
    window.quit()
    subprocess.Popen(['python', 'Anime Version/Night Market/gui.py'])
    return {"success": True, "message": f"Bought {item_name} for {price} coins"}

def get_item_image(name):
    try:
        # Construct the absolute path to the Images folder
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        if name.split()[0] == 'Coin' and name.split()[1] == 'Bag':
            file_loc = os.path.join(script_dir, "Images")
            files = os.path.join(file_loc, "Coin Pouch Big.png")

        elif name.split()[-1] == 'Key':
            file_loc = os.path.join(script_dir, "Images")
            files = os.path.join(file_loc, "Instance Keys Big.png")

        elif name=="INT. Based Points"or name=="INTav":
            file_loc = os.path.join(script_dir, "Images")
            files = os.path.join(file_loc, "AVINT" + '.png')

        elif name=="STR. Based Points" or name=="STRav":
            file_loc = os.path.join(script_dir, "Images")
            files = os.path.join(file_loc, "AVSTR" + '.png')

        elif name.split()[0]=="Coins:":
            file_loc = os.path.join(script_dir, "Images")
            files = os.path.join(file_loc, "Coin" + '.png')

        elif name.split()[0]=="Experience":
            file_loc = os.path.join(script_dir, "Images")
            files = os.path.join(file_loc, "XP" + '.png')

        elif name=="LVLADD":
            file_loc = os.path.join(script_dir, "Images")
            files = os.path.join(file_loc, "Level Add" + '.png')

        elif name=="":
            file_loc = os.path.join(script_dir, "Images")
            files = os.path.join(file_loc, "Unknown" + '.png')

        else:
            file_loc = os.path.join(script_dir, "Images")
            files = os.path.join(file_loc, name + ' Big.png')

        if not os.path.exists(files):
            files = os.path.join(file_loc, "Unknown.png")

        # Open and resize the image
        image = Image.open(files)

        # Crop to 680x680 (centered)
        width, height = image.size
        left = 0
        top = (height - 680) // 2  # Crop from center
        right = 680
        bottom = top + 680
        image = image.crop((left, top, right, bottom))

        image = image.resize((80, 80), Image.Resampling.LANCZOS)  # High-quality resize
        return ImageTk.PhotoImage(image)

    except:
        return None  # Handle errors properly


# Main execution block moved into the function
if __name__ == "__main__":
    # Get current weekly data (handles all weekly logic automatically)
    weekly_data = get_weekly_night_market_data()
    
    # Display weekly metadata
    print(f"Week Key: {weekly_data['week_key']}")
    print(f"Created: {weekly_data['created_date']}")
    print(f"Week Start: {weekly_data['week_start']}")
    print(f"Last Updated: {weekly_data['last_updated']}")
    
    # Display rank items summary with rarity breakdown
    rank_items = weekly_data['rank_items']
    print(rank_items)
    for rank in ["S", "B", "C", "D"]:
        print(f"\n=== {rank}-Rank Items ===")
        rank_data = rank_items[rank]
        print(f"Total {rank}-rank items: {len(rank_data)}")
        
        # Count items by rarity
        rarity_counts = {"Common": 0, "Rare": 0, "Epic": 0, "Legendary": 0}
        for item_info in rank_data.values():
            rarity = item_info["rarity"]
            rarity_counts[rarity] = rarity_counts.get(rarity, 0) + 1
        
        print(f"Rarity breakdown: {rarity_counts}")
        
        # Show examples
        count = 0
        for item_name, item_info in rank_data.items():
            if count < 3:  # Show first 3 examples
                rarity = item_info["rarity"]
                value = item_info["data"].get("Value", 0)
                print(f"  - {item_name} ({rarity}, Value: {value})")
                count += 1
            else:
                break 