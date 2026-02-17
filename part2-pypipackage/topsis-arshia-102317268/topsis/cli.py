import argparse
import pandas as pd
import numpy as np
import sys

def main():

    parser = argparse.ArgumentParser(
        description="TOPSIS Multi-Criteria Decision Making Tool"
    )

    parser.add_argument("input_file", help="Input data file (.csv or .xlsx)")
    parser.add_argument("weights", help="Comma-separated weights")
    parser.add_argument("impacts", help="Comma-separated impacts (+ or -)")
    parser.add_argument("output_file", help="Output result file (.csv or .xlsx)")

    args = parser.parse_args()

    input_file = args.input_file
    weights = args.weights
    impacts = args.impacts
    output_file = args.output_file

    # ---------- FILE READING ----------
    try:
        if input_file.endswith(".csv"):
            df = pd.read_csv(input_file)
        elif input_file.endswith(".xlsx"):
            df = pd.read_excel(input_file)
        else:
            print("Error: Only CSV or XLSX files are supported.")
            sys.exit(1)
    except FileNotFoundError:
        print("Error: File not found.")
        sys.exit(1)

    # ---------- CLEAN DATA ----------
    df = df.dropna(axis=1, how='all')
    df.columns = df.columns.str.strip()
    df = df.loc[:, (df.columns != '') & (~df.columns.str.contains('^Unnamed'))]

    # ---------- VALIDATIONS ----------
    if df.shape[1] < 3:
        print("Error: Input file must contain at least 3 columns.")
        sys.exit(1)

    criteria_data = df.iloc[:, 1:]

    if criteria_data.apply(pd.to_numeric, errors='coerce').isnull().values.any():
        print("Error: Non-numeric values found in criteria columns.")
        sys.exit(1)

    # ---------- SPLIT INPUTS ----------
    weights_list = [w.strip() for w in weights.split(',')]
    impacts_list = [i.strip() for i in impacts.split(',')]

    criteria_count = df.shape[1] - 1

    if not (len(weights_list) == len(impacts_list) == criteria_count):
        print("Error: Number of weights, impacts and criteria columns must be the same.")
        sys.exit(1)

    for impact in impacts_list:
        if impact not in ['+', '-']:
            print("Error: Impacts must be either '+' or '-'.")
            sys.exit(1)

    try:
        weights_list = [float(w) for w in weights_list]
    except ValueError:
        print("Error: Weights must be numeric.")
        sys.exit(1)

    # ---------- TOPSIS CALCULATION ----------

    matrix = criteria_data.astype(float).values

    # Step 1: Normalize
    norm_matrix = matrix / np.sqrt((matrix ** 2).sum(axis=0))

    # Step 2: Multiply Weights
    weighted_matrix = norm_matrix * weights_list

    # Step 3: Ideal Best & Worst
    ideal_best = []
    ideal_worst = []

    for i in range(criteria_count):
        if impacts_list[i] == '+':
            ideal_best.append(weighted_matrix[:, i].max())
            ideal_worst.append(weighted_matrix[:, i].min())
        else:
            ideal_best.append(weighted_matrix[:, i].min())
            ideal_worst.append(weighted_matrix[:, i].max())

    ideal_best = np.array(ideal_best)
    ideal_worst = np.array(ideal_worst)

    # Step 4: Distance Calculation
    dist_best = np.sqrt(((weighted_matrix - ideal_best) ** 2).sum(axis=1))
    dist_worst = np.sqrt(((weighted_matrix - ideal_worst) ** 2).sum(axis=1))

    # Step 5: Score
    scores = dist_worst / (dist_best + dist_worst)

    # Step 6: Rank
    ranks = scores.argsort()[::-1] + 1

    # ---------- OUTPUT ----------
    df['Topsis Score'] = scores
    df['Rank'] = ranks

    try:
        if output_file.endswith(".csv"):
            df.to_csv(output_file, index=False)
        elif output_file.endswith(".xlsx"):
            df.to_excel(output_file, index=False)
        else:
            print("Error: Output file must be CSV or XLSX.")
            sys.exit(1)
    except Exception as e:
        print("Error saving file:", e)
        sys.exit(1)

    print("TOPSIS calculation completed successfully!")
    print("Results saved to:", output_file)


if __name__ == "__main__":
    main()