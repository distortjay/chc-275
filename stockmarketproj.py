import re
import sys
from statistics import mean


    data = {}
    try:
        with open(path, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        raise
    except Exception as e:
        raise

    for lineno, raw in enumerate(lines, start=1):
        line = raw.strip()
        if not line:
            continue
        parts = re.split(r'[,\s]+', line)
        if len(parts) < 2:
            raise ValueError(f"{path}:{lineno}: missing data")
        ticker = parts[0].upper()
        nums = parts[1:]
        if len(nums) != 20:
            raise ValueError(f"{path}:{lineno}: expected 20 data points for {ticker}, got {len(nums)}")
        try:
            values = [float(x) for x in nums]
        except ValueError:
            raise ValueError(f"{path}:{lineno}: non-numeric value encountered for {ticker}")
        data[ticker] = values
    return data

def write_report(path, averages1, averages2):
    try:
        with open(path, 'w') as f:
            f.write("Stock  Avg_Days1-20  Avg_Days21-40\n")
            f.write("---------------------------------\n")
            tickers = sorted(set(averages1.keys()) | set(averages2.keys()))
            for t in tickers:
                a1 = averages1.get(t)
                a2 = averages2.get(t)
                a1s = f"{a1:.2f}" if a1 is not None else "N/A"
                a2s = f"{a2:.2f}" if a2 is not None else "N/A"
                f.write(f"{t:5}   {a1s:11}   {a2s:12}\n")
            f.write("\nTickers with higher Avg Days21-40 than Avg Days1-20:\n")
            higher = [t for t in tickers if (averages1.get(t) is not None and averages2.get(t) is not None and averages2[t] > averages1[t])]
            if higher:
                for t in higher:
                    f.write(f"- {t}\n")
            else:
                f.write("None\n")
    except Exception:
        raise

def main():
    file1 = "Day1_20.txt"
    file2 = "Day21_40.txt"
    out = "report.txt"

    try:
        data1 = parse_20day_file(file1)
    except FileNotFoundError:
        print(f"Error: {file1} not found.", file=sys.stderr)
        return
    except ValueError as ve:
        print(f"Error parsing {file1}: {ve}", file=sys.stderr)
        return
    except Exception as e:
        print(f"Unexpected error reading {file1}: {e}", file=sys.stderr)
        return
    else:
    
        pass

    try:
        data2 = parse_20day_file(file2)
    except FileNotFoundError:
        print(f"Error: {file2} not found.", file=sys.stderr)
        return
    except ValueError as ve:
        print(f"Error parsing {file2}: {ve}", file=sys.stderr)
        return
    except Exception as e:
        print(f"Unexpected error reading {file2}: {e}", file=sys.stderr)
        return
    else:
        # success reading file2
        pass

    # compute averages
    averages1 = {t: mean(vals) for t, vals in data1.items()}
    averages2 = {t: mean(vals) for t, vals in data2.items()}

    # write report with try-except-else
    try:
        write_report(out, averages1, averages2)
    except Exception as e:
        print(f"Failed to write {out}: {e}", file=sys.stderr)
        return
    else:
        print(f"Report generated: {out}")

if __name__ == "__main__":
    main()