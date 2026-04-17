ICU_BEDS = 2

def allocate_icu(priority):
    global ICU_BEDS
    if priority == "High" and ICU_BEDS > 0:
        ICU_BEDS -= 1
        return True, ICU_BEDS
    return False, ICU_BEDS
