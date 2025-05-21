import re

def parse_e2fa_log(file_path):
    results = {}
    status_map = {
        "00": "Success",
        "02": "Bad Password value.",
        "03": "Password has Expired.",
        "04": "Password is now blocked.",
        "05": "Password value not passed/MessageHash validation failed/LinkData was empty!.",
        "06": "DB Error",
        "07": "Link data encryption failed/Internal Error",
        "08": "No Password in system",
    }
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for i, line in enumerate(lines):
            # Step 1: Find line with OrnReferenceNumber and TxnID
            orn_match = re.search(r"OrnReferenceNumber: (\d+)", line)
            txnid_match = re.search(r"TxnID: ([\w-]+)", line)
            if orn_match and txnid_match:
                orn = orn_match.group(1)
                txnid = txnid_match.group(1)
                # Step 2: Find next line with StatusCode for this txnid
                for j in range(i+1, min(i+10, len(lines))):
                    if txnid in lines[j] and "StatusCode" in lines[j]:
                        status_match = re.search(r"StatusCode:([\w]+)", lines[j])
                        code = status_match.group(1) if status_match else None
                        status = status_map.get(code, "Failed")
                        # Extract timestamp in format YYYY-MM-DD HH:MM:SS if present
                        timestamp_match = re.search(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})", lines[j])
                        timestamp = timestamp_match.group(1) if timestamp_match else "Unknown"
                        results[orn] = {"status": status, "timestamp": timestamp}
                        break
    return results

def extract_transaction_id(line):
    # Logic to extract transaction ID from the log line
    pass

def extract_status(line):
    # Logic to extract success/fail status from the log line
    pass

def extract_timestamp(line):
    # Logic to extract timestamp from the log line
    pass