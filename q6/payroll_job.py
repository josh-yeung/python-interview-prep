import json
from collections import defaultdict

# Company Constants
HOURLY_RATE = 15.00
OVERTIME_MULTIPLIER = 1.5
OVERTIME_THRESHOLD_HOURS = 40.0

def load_timesheets(filepath):
    with open(filepath, "r") as file:
      return json.load(file) 
    
def calculate_time(start, finish):
    startHour, startMin  = start.split(":")
    finishHour, finishMin = finish.split(":")
    startTime = float(startHour) + (float(startMin) / 60)
    finishTime = float(finishHour) + (float(finishMin) / 60)
    return finishTime - startTime


def time_parse(shifts):
    hours = defaultdict(lambda: {"name": "", "hoursWorked": 0, "missingPunches": 0})
    for shift in shifts:
        if hours[shift["emp_id"]]["name"] != shift["name"]:
            hours[shift["emp_id"]]["name"] = shift["name"]
        if not shift["in"] or not shift["out"]:
            hours[shift["emp_id"]]["missingPunches"] += 1
        else:
            hours[shift["emp_id"]]["hoursWorked"] += calculate_time(shift["in"], shift["out"])
    return hours


def run_payroll():
    shifts = load_timesheets("timesheets.json")
    sheet = time_parse(shifts)
    output = {}
    for key, value in sheet.items():
        totalHours = value["hoursWorked"]
        if totalHours > 40:
            regularPay = round(40 * HOURLY_RATE, 2)
            overtimePay = round((totalHours - 40) * HOURLY_RATE * OVERTIME_MULTIPLIER, 2)
            totalPay = regularPay + overtimePay
        else: 
            regularPay = round(totalHours * HOURLY_RATE, 2)
            overtimePay = 0.0
            totalPay = regularPay
        item = {"name": value["name"], "total_hours": totalHours, 
                "regular_pay": regularPay, "overtime_pay": overtimePay, "total_pay": totalPay, "missing_punches": value["missingPunches"]}
        output[key] = item
    return output

def write_json(output):
    with open("payroll_report.json", "w") as file:
        json.dump(output, file, indent=2)


if __name__ == "__main__":
    output = run_payroll()
    write_json(output)