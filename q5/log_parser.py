import json
from collections import defaultdict


def parser(input_filepath):
    logs = []
    with open(input_filepath, "r") as file:
        content = file.read()
        content = content.split("\n")
        index = -1
        for item in content:
            line = item.strip()
            line = line.split("|")
            if len(line) == 1:
                continue
            item = line[0].strip().split()
            logs.append({"info": item[0], "date": item[1]})
            index += 1
            for i in range(1, len(line)):
                item = line[i].strip().split()
                key = item[0][:-1]
                val = item[1]
                logs[index][key] = val
    return logs
                    

def parse_logs_and_generate_report(input_filepath, output_filepath):
    print(f"Reading logs from {input_filepath}...")
    logs = parser(input_filepath)
    output = defaultdict(float)
    for log in logs:
        if log["status"] == "success" and log["action"] == "purchase":
            amount = float(log.get("amount", 0))
            output[log["user_id"]] += amount
    with open(output_filepath, "w") as file:
        json.dump(output, file, indent=4) 

    print(f"Report successfully saved to {output_filepath}")

if __name__ == "__main__":
    parse_logs_and_generate_report("server.log", "spend_report.json")