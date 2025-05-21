import re

def parse_axiom_log(file_path):
    results = {}
    with open(file_path, 'r') as file:
        for line in file:
            # Find ornId in the line
            orn_match = re.search(r"ornId[=:-](\d+)", line)
            if orn_match and "/axiomhttprec/pushlistener?" in line:
                print(f"parse_axiom_log | line: {line}")
                print("parse_axiom_log | Inside success condition")
                orn = orn_match.group(1)
                timestamp = line.split()[0] + " " + line.split()[1]
                status = "Success"
                results[orn] = {"status": status, "timestamp": timestamp}
    return results

def extract_otp_send_info(orn_number, logs):
    relevant_logs = [log for log in logs if orn_number in log['line']]
    return relevant_logs