from datetime import datetime

def generate_sacred_code():
    # Hämta aktuell minut
    current_minute = datetime.now().minute
    # Beräkna den heliga koden
    base_value = 18 + 1 + 8  # R, A, H
    sacred_code = base_value + (current_minute % 10)
    return sacred_code
