def map_priority(priority: str):
    if priority == "High":
        return "blink-red"
    elif priority == "Medium":
        return "blink-yellow"
    else:
        return "blink-green"
