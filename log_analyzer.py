import re
import sys
import csv

def analyze_log(file_path, export_csv=False):
    # Regex pattern matches both "Failed password" and "Failed password for invalid user"
    pattern = re.compile(r"Failed password for (invalid user )?(\w+) from ([\d\.]+)")

    results = []

    try:
        with open(file_path, "r") as f:
            for line in f:
                match = pattern.search(line)
                if match:
                    user = match.group(2)
                    ip = match.group(3)
                    results.append((user, ip))

        if results:
            print(f"Found {len(results)} failed login attempts:\n")
            for user, ip in results:
                print(f"User: {user}\tIP: {ip}")

            if export_csv:
                with open("failed_logins.csv", "w", newline="") as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(["User", "IP Address"])
                    writer.writerows(results)
                print("\nResults exported to failed_logins.csv")
        else:
            print("No failed login attempts found.")

    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python log_analyzer.py <logfile> [--csv]")
        sys.exit(1)

    logfile = sys.argv[1]
    export_csv = "--csv" in sys.argv
    analyze_log(logfile, export_csv)

