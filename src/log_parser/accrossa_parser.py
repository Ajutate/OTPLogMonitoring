import re

def parse_accrossa_log(file_path):
    results = {}
    with open(file_path, 'r') as file:
        for line in file:
            # Extract ORN from oobOrnRefNo or oobrefNo
            orn_match = re.search(r"oobOrnRefNo[-=](\d+)", line)
            if not orn_match:
                orn_match = re.search(r"oobrefNo[-=](\d+)", line)
            if orn_match:
                orn = orn_match.group(1)
                # Check for success condition
                print ("parse_accossa_log | line: " + line)
                if "00BResponse(responseCode-00" in line and "responseMsg-SUCCESS" in line:
                    print ("parse_accossa_log | Inside success condition")
                    status = "Success"
                else:
                    print ("parse_accossa_log | Inside fail condition")
                    status = "Fail"
                # Extract timestamp (first part of line)
                timestamp = line.split()[0] + " " + line.split()[1]
                results[orn] = {"status": status, "timestamp": timestamp}
    return results

def extract_timestamp(log_line):
    # Assuming the timestamp is the first part of the log line
    return log_line.split()[0]

def extract_status(log_line):
    # Assuming the status is indicated by "Success" or "Fail" in the log line
    if "Success" in log_line:
        return "Success"
    elif "Fail" in log_line:
        return "Fail"
    return "Unknown"