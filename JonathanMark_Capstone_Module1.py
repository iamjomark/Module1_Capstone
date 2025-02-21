# Password and Launch Code
PASSWORD = "H@ndler1"  # Password required for removing and strike
LAUNCH_CODE = "86" # required for strike

# Initial BLUFOR collection (Blue Force / friendly units)
blufor = [
    {"callsign": "SPEARHEAD", "firepower_provided": 70.2, "stock": 1},
    {"callsign": "NORDLICHT", "firepower_provided": 80.4, "stock": 1},
    {"callsign": "MIRAKEL", "firepower_provided": 15, "stock": 7},
    {"callsign": "NIGHTHAWK", "firepower_provided": 45.1, "stock": 3},
    {"callsign": "ESEMKA", "firepower_provided": 2, "stock": 15}
]

# Initial OPFOR collection (Opposition Force / enemy targets)
opfor = [
    {"name": "GERONIMO", "priority": 1, "coor": "43S 338007 3782327", "firepower_needed": 35},
    {"name": "SOS-1", "priority": 2, "coor": "dzkmrefnw6d3wrf", "firepower_needed": 0},
    {"name": "BHDOWN", "priority": 1, "coor": "t025xm6ng7qbfn7g", "firepower_needed": 42},
    {"name": "SOS-2", "priority": 2, "coor": "dj15mpmfgp8z", "firepower_needed": 0},
    {"name": "BLOOP", "priority": 3, "coor": "1z0gs", "firepower_needed": 0},
    {"name": "NUREMBERG", "priority": 3, "coor": "u0zc76vk2ud233ue", "firepower_needed": 0},
    {"name": "BIELEFELD", "priority": 2, "coor": "u1npfnjb3hbzj3zz", "firepower_needed": 14.2}
]

# Lists to save and store removed BLUFOR and OPFOR units for re-adding option
removed_blufor = []
removed_opfor = []

# Functions

# Input function with error handling (try, except). a 3 attempt limit for tries, and valid choices
def get_int_input(prompt, valid_options=None):
    attempts = 0
    while attempts < 3: # attempt will increase for every try until a max of 3
        try:
            value = int(input(prompt))
            if valid_options and value not in valid_options:
                print(f"Invalid choice. Choose from {valid_options}. Attempt {attempts + 1}/3.")
            else:
                return value
        except ValueError:
            print(f"Invalid input. Please enter an integer. Attempt {attempts + 1}/3.")
        attempts += 1
    
    print("Too many invalid inputs. Exiting.")
    exit()# after 3 tries, the app will stop

def get_float_input(prompt):
    attempts = 0
    while attempts < 3: # same like above
        try:
            return float(input(prompt))
        except ValueError:
            print(f"Invalid input. Please enter a number. Attempt {attempts + 1}/3.")
        attempts += 1
    
    print("Too many invalid inputs. Exiting.")
    exit()# same like above

# BLUFOR Functions

# Display BLUFOR units based on filter and sort
def display_blufor(): 
    # Filtering
    print("\nBLUFOR Units:")
    print("\nFilter by:")
    print("1. All")
    print("2. Available (stock >0)")
    print("3. Firepower provided >= value")
    filter_choice = get_int_input("Choose filter option (1-3): ", valid_options={1, 2, 3})
    
    # Display based on filter
    filtered = blufor.copy()
    # filter based on availability (stock > 0)
    if filter_choice == 2:
        filtered = [unit for unit in filtered if unit['stock'] > 0] # list comprehension to make code compact
    # filter based on minimum firepower
    elif filter_choice == 3:
        min_fp = get_float_input("Enter minimum firepower: ")
        filtered = [unit for unit in filtered if unit['firepower_provided'] >= min_fp]
    
    # Sorting
    print("\nSort by:")
    print("1. Sort by stock")
    print("2. Sort by firepower")
    print("3. Sort by availability")
    sort_choice = get_int_input("Choose sorting option (1-3): ", valid_options={1, 2, 3})
    
    # Display based on stock
    if sort_choice == 1: 
        filtered.sort(key=lambda unit: unit['stock'], reverse=True)
    # based on firepower_provided
    elif sort_choice == 2:
        filtered.sort(key=lambda unit: unit['firepower_provided'], reverse=True)
    # based on availability (stock > 0)
    elif sort_choice == 3:
        filtered.sort(key=lambda unit: unit['stock'] > 0, reverse=True)
    
    # Display in a tidy manner
    print("\n{:<5} {:<15} {:<15} {:<10}".format("No.", "Callsign", "Firepower", "Stock"))
    for index, unit in enumerate(filtered, 1):
        print("{:<5} {:<15} {:<15.1f} {:<10}".format(
            index, 
            unit['callsign'], 
            unit['firepower_provided'], 
            unit['stock']
        ))
    return filtered  
    # Return filtered list for further actions on other menus and functions

# Adding new and re-adding / recover removed BLUFOR units
def add_blufor():
    print("\nAdd BLUFOR Unit:")
    print("1. Add new unit")
    print("2. Recover removed unit")
    choice = get_int_input("Choose option: ", valid_options={1, 2})
    
    # Add new units
    if choice == 1:
        callsign = input("Enter callsign: ").strip().upper() # making sure no spaces left/right + CAPS
        if any(unit['callsign'] == callsign for unit in blufor): # making sure no duplicates
            print("Callsign already exists. Update stock on Update Menu")
            return
        firepower = get_float_input("Enter firepower provided: ")
        stock = get_int_input("Enter stock: ")
        blufor.append({
            "callsign": callsign,
            "firepower_provided": firepower,
            "stock": stock
        })
        print("BLUFOR unit added successfully!")
        display_blufor()

    # Re-add / recover removed unit
    elif choice == 2:
        if not removed_blufor: # check for removed units
            print("No removed BLUFOR units to re-add.")
            return
        print("Removed BLUFOR Units:")
        for index, unit in enumerate(removed_blufor): 
        # putting numbers (enumerate) for index so user can choose
        # not forgetting + 1 and - 1 since index starts from 0 instead of 1 
            print(f"{index+1}. {unit['callsign']} (Firepower: {unit['firepower_provided']}, Stock: {unit['stock']})")
        unit_index = get_int_input("Select unit to re-add: ") - 1
        if 0 <= unit_index < len(removed_blufor):
            unit = removed_blufor[unit_index]
            blufor.append(unit)
            removed_blufor.pop(unit_index)
            print(f"Re-added {unit['callsign']} successfully.")
            display_blufor()
        else:
            print("Invalid selection.")


# Update BLUFOR unit stock
def update_blufor():
    filtered_units = display_blufor()  # Get filtered list with index from the display menu
    if not filtered_units: # check if no available units
        print("No BLUFOR units to update.")
        return
    choice = get_int_input("Enter unit number to update: ")
    if 1 <= choice <= len(filtered_units):
        unit = filtered_units[choice - 1]
        new_stock = get_int_input("Enter new stock value: ") 
        if new_stock < 0: # can't be less than 0
            print("Stock value cannot be negative. Please enter a valid number.")
            return 
        unit['stock'] = new_stock
        print(f"Updated {unit['callsign']} stock to {new_stock}.")
        display_blufor()
    else:
        print("Invalid index.")

# Remove BLUFOR unit
def remove_blufor():
    filtered_units = display_blufor()  # Get filtered list with indices
    if not filtered_units:
        print("No BLUFOR units to remove.")
        return
    choice = get_int_input("Enter unit number to remove: ")
    if 1 <= choice <= len(filtered_units):
        unit_to_remove = filtered_units[choice - 1]

        # Password check
        attempts = 0
        while attempts < 3:
            password_attempt = input("Enter password to confirm removal: ")
            if password_attempt == PASSWORD:
                break
            attempts += 1
            print(f"Incorrect password. Attempt {attempts}/3.")
        else:
            print("Too many failed attempts. Exiting.")
            exit()
        
        # Reconfirm 
        confirm = input(f"Confirm removal of {unit_to_remove['callsign']} (yes/no): ").strip().lower()
        if confirm != 'yes':
            print("Removal canceled.")
            return
        blufor.remove(unit_to_remove)  # Remove from original list
        removed_blufor.append(unit_to_remove)  # Store in removed list
        print(f"Removed {unit_to_remove['callsign']}")
        display_blufor()
    else:
        print("Invalid index.")

# OPFOR Functions
# most annotations are the same as BLUFOR

# Display OPFOR targets based on filter then sort
def display_opfor():
    print("\nOPFOR Targets:")
    # Filter options
    print("\nFilter by:")
    print("1. All")
    print("2. Firepower needed")
    print("3. Priority")
    filter_choice = get_int_input("Choose filter option (1-3): ", valid_options={1, 2, 3}) # valid options to choose 
    
    # Filtering
    filtered = opfor.copy()
    # based on firepower_needed
    if filter_choice == 2:
        min_fp = get_float_input("Enter minimum firepower: ")
        filtered = [target for target in filtered if target['firepower_needed'] >= min_fp]
    # based on priority
    elif filter_choice == 3:
        priority_level = get_int_input("Enter priority level (1-3): ", valid_options={1, 2, 3})
        filtered = [target for target in filtered if target['priority'] == priority_level]

    # Sort options
    print("\nSort by:")
    print("1. Sort by priority")
    print("2. Sort by firepower needed")
    print("3. Sort by coordinates")
    sort_choice = get_int_input("Choose sorting option (1-3): ", valid_options={1, 2, 3})

    # Sorting
    # Based on priority
    if sort_choice == 1:
        filtered.sort(key=lambda target: target['priority'])
    # based on firepower_needed
    elif sort_choice == 2:
        filtered.sort(key=lambda target: target['firepower_needed'], reverse=True)
    # based on coordinates
    elif sort_choice == 3:
        filtered.sort(key=lambda target: target['coor'])
    
    # Display in a tidy manner
    print("\n{:<5} {:<15} {:<10} {:<20} {:<15}".format("No.", "Name", "Priority", "Coordinates", "Firepower Needed"))
    for idx, target in enumerate(filtered, 1):
        print("{:<5} {:<15} {:<10} {:<20} {:<15.1f}".format(
            idx,
            target['name'],
            target['priority'],
            target['coor'],
            target['firepower_needed']
        ))
    return filtered  # Return filtered list for further actions

# Add new and re-adding removed OPFOR targets
def add_opfor():
    print("\nAdd OPFOR Target:")
    print("1. Add new target")
    print("2. Re-add removed target")
    choice = get_int_input("Choose option: ", valid_options={1, 2})
    
    # Adding new targets
    if choice == 1:
        name = input("Enter target name: ").strip().upper()
        if any(target['name'] == name for target in opfor): # check for duplicates
            print("Target name already exists.")
            return
        priority = get_int_input("Enter priority: ")
        coor = input("Enter coordinates: ")
        firepower = get_float_input("Enter firepower needed: ")
        opfor.append({
            "name": name,
            "priority": priority,
            "coor": coor,
            "firepower_needed": firepower
        })
        print("OPFOR target added successfully!")
        display_opfor()

    # Re-adding removed targets
    elif choice == 2:
        if not removed_opfor: # check for any removed target
            print("No removed OPFOR targets to re-add.") 
            return
        print("Removed OPFOR Targets:")
        for index, target in enumerate(removed_opfor):
            print(f"{index+1}. {target['name']} (Priority: {target['priority']}, Firepower Needed: {target['firepower_needed']})")
        target_index = get_int_input("Select target to re-add: ") - 1
        if 0 <= target_index < len(removed_opfor):
            target = removed_opfor[target_index]
            opfor.append(target) # readding target
            removed_opfor.pop(target_index)
            print(f"Re-added {target['name']} successfully.")
            display_opfor()
        else:
            print("Invalid selection.")

# Remove targets
def remove_opfor():
    filtered_targets = display_opfor()  # Get filtered list with indices
    if not filtered_targets:
        print("No OPFOR targets to remove.")
        return
    choice = get_int_input("Enter target number to remove: ")
    if 1 <= choice <= len(filtered_targets):
        target_to_remove = filtered_targets[choice - 1]

        # Password check
        attempts = 0
        while attempts < 3:
            password_attempt = input("Enter password to confirm removal: ")
            if password_attempt == PASSWORD:
                break
            attempts += 1
            print(f"Incorrect password. Attempt {attempts}/3.")
        else:
            print("Too many failed attempts. Exiting.")
            exit()
        
        confirm = input(f"Confirm removal of {target_to_remove['name']} (yes/no): ").lower()
        if confirm != 'yes':
            print("Removal canceled.")
            return
        opfor.remove(target_to_remove)
        removed_opfor.append(target_to_remove)
        print(f"Removed {target_to_remove['name']}")
        display_opfor()
    else:
        print("Invalid index.")

# Strike Function
def commence_strike():
    print("\n!!! STRIKE MISSION !!!")
    if not opfor: # check for available targets
        print("No available targets!")
        return
        
    print("\nAvailable Targets:")
    for index, target in enumerate(opfor):
        print(f"{index+1}. {target['name']} (Priority: {target['priority']}, Required Firepower: {target['firepower_needed']})")
    # again like BLUFOR, starting the options from 1 instead of default 0

    target_choice = get_int_input("Select target: ") - 1
    if not (0 <= target_choice < len(opfor)):
        print("Invalid target selection!")
        return

    available_units = [unit for unit in blufor if unit['stock'] > 0]
    if not available_units:
        print("No available units for strike!")
        return
        
    print("\nAvailable Strike Units:")
    for index, unit in enumerate(available_units):
        print(f"{index+1}. {unit['callsign']} (Firepower: {unit['firepower_provided']}, Available: {unit['stock']})")
    
    unit_choice = get_int_input("Select strike unit: ") - 1
    if not (0 <= unit_choice < len(available_units)):
        print("Invalid unit selection!")
        return

    # Authorization
    print("\n=== STRIKE AUTHORIZATION ===")
    # Password check with 3 tries
    attempts_pw = 0
    while attempts_pw < 3:
        password_attempt = input("Enter security password: ")
        if password_attempt == PASSWORD:
            break
        attempts_pw += 1
        print(f"Password verification failed! Attempt {attempts_pw}/3.")
    else:
        print("Too many failed attempts. Exiting.")
        return
    # Launch code check with 3 tries
    attempts_code = 0
    while attempts_code < 3:
        code = input("Enter launch code: ")
        if code == LAUNCH_CODE:
            break
        attempts_code += 1
        print(f"Launch code invalid! Attempt {attempts_code}/3.")
    else:
        print("Too many failed attempts. Exiting.")
        return

    # Execution
    selected_unit = available_units[unit_choice]
    selected_target = opfor[target_choice]
    
    print(f"\nLaunching {selected_unit['callsign']} against {selected_target['name']}...")
    
    #Success
    if selected_unit['firepower_provided'] > selected_target['firepower_needed']:
        opfor.pop(target_choice) # removing the target
        selected_unit['stock'] -= 1 # update unit stock
        print("Mission success! Target eliminated.")
    # Fail
    else:
        selected_unit['stock'] -= 1 # update unit stock
        print("Mission failed! Insufficient firepower.")

# Menu Systems
def blufor_menu():
    while True:
        print("\n=== BLUFOR COMMAND ===")
        print("1. List Units")
        print("2. Add Unit")
        print("3. Update Unit Stock")
        print("4. Remove Unit")
        print("5. Return to Main")
        choice = get_int_input("Select option: ", valid_options={1, 2, 3, 4, 5})
        
        if choice == 1:
            display_blufor()
        elif choice == 2:
            add_blufor()
        elif choice == 3:
            update_blufor()
        elif choice == 4:
            remove_blufor()
        elif choice == 5:
            break
        else:
            print("Invalid option! Please choose 1-5.")

def opfor_menu():
    while True:
        print("\n=== OPFOR MENU ===")
        print("1. Display targets")
        print("2. Add target")
        print("3. Remove target")
        print("4. Back")
        choice = get_int_input("Select option: ", valid_options={1, 2, 3, 4})
        if choice == 1:
            display_opfor()
        elif choice == 2:
            add_opfor()
        elif choice == 3:
            remove_opfor()
        elif choice == 4:
            break
        else:
            print("Invalid choice")

# Main Program
def main():
    attempts = 0
    while attempts < 3:
        password_attempt = input("Enter password: ")
        if password_attempt == PASSWORD:
            break
        attempts += 1
        print(f"Access Denied. Attempt {attempts}/3.")
    else:
        print("Too many failed attempts. Exiting.")
        return
    
    print("\nWelcome, Special Staff to the Minister of Defense")
    while True:
        print("\nMain Menu")
        print("1. BLUFOR Menu")
        print("2. OPFOR Menu")
        print("3. Strike")
        print("4. Exit")
        choice = get_int_input("Select option: ", valid_options={1, 2, 3, 4})
        if choice == 1:
            blufor_menu()
        elif choice == 2:
            opfor_menu()
        elif choice == 3:
            commence_strike()
        elif choice == 4:
            print("Free Lunch currently unavailable due to: ")
            print("Budget Efficiency")
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()