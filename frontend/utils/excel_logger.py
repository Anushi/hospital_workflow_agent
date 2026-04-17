import pandas as pd
import os
from datetime import datetime

# Path where logs will be stored
LOG_FILE = "data/hospital_logs.xlsx"

def log_to_excel(result):
    # Ensure data directory exists
    os.makedirs("data", exist_ok=True)
    
    # Flatten the incoming JSON result
    new_entry = {
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Ambulance ID": result.get("ambulance_id"),
        "Risk Priority": result["triage"].get("priority"),
        "Admission Level": result["admission"].get("suggested_admission_level"),
        "Assigned Bed": result["resource"].get("bed"),
        "Teams Notified": ", ".join(result["resource"].get("teams", [])),
        "Clinical Note": result["admission"].get("note")
    }
    
    df_new = pd.DataFrame([new_entry])

    try:
        if not os.path.isfile(LOG_FILE):
            # Create new file
            df_new.to_excel(LOG_FILE, index=False, engine='openpyxl')
        else:
            # Append to existing file
            with pd.ExcelWriter(LOG_FILE, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
                # Load existing to find the next empty row
                start_row = writer.book['Sheet1'].max_row
                df_new.to_excel(writer, index=False, header=False, startrow=start_row)
        return True
    except Exception as e:
        print(f"Excel Logging Error: {e}")
        return False