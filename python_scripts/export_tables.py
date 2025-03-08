import csv
import re
import random
# def latex_table_to_csv(latex_code, csv_filename):
#     """
#     Converts a LaTeX table with single backslashes to a CSV file, handling potential formatting issues.

#     :param latex_code: String containing the LaTeX table.
#     :param csv_filename: Output CSV filename.
#     """
#     # Preprocess the LaTeX code to clean up non-standard escape sequences
#     latex_code = latex_code.replace("\x08", "")  # Remove problematic escape sequences
    
#     # Extract the content of the tabular environment
#     match = re.search(r"\\begin\{tabular\}.*?\\hline(.*?)\\end\{tabular\}", latex_code, re.S)
#     if not match:
#         raise ValueError("No valid tabular environment found in the LaTeX code. "
#                          "Ensure the table uses \\begin{tabular} and \\end{tabular}.")
    
#     tabular_content = match.group(1)
    
#     # Split rows using single backslashes for row separators
#     rows = []
#     for line in tabular_content.split(r"\\"):
#         line = line.strip()
#         if line and not line.startswith(r"\hline"):  # Skip empty lines and \hline
#             # Replace & (column separator) with commas and clean up LaTeX formatting
#             cleaned_line = re.sub(r"\\[a-zA-Z]+|[\{\}\$\-]", "", line)
#             row = [col.strip() for col in cleaned_line.split("&")]
#             rows.append(row)
    
#     # Write to CSV
#     with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
#         writer = csv.writer(file)
#         writer.writerows(rows)
    
#     print(f"Table converted and saved to '{csv_filename}'.")

def latex_table_to_csv(latex_code, csv_filename, randomize_floats=False, float_range=(0, 100)):
    """
    Converts a LaTeX table with single backslashes to a CSV file, with an option to randomize float values.

    :param latex_code: String containing the LaTeX table.
    :param csv_filename: Output CSV filename.
    :param randomize_floats: If True, replaces float values with random numbers.
    :param float_range: Tuple specifying the range of random float values.
    """
    # Clean up the LaTeX input to remove unwanted characters
    latex_code = latex_code.replace("\x08", "").strip()  # Remove backspace escape sequences

    # Correct regex to capture tabular content
    match = re.search(r"\\begin\{tabular\}.*?\\hline(.*?)\\end\{tabular\}", latex_code, re.S)
    if not match:
        raise ValueError("No valid tabular environment found in the LaTeX code.")
    
    tabular_content = match.group(1)
    
    # Split rows using single backslashes (escaped in regex as `\\\\`)
    rows = []
    last_solver = ""  # Variable to store the last non-empty solver name
    
    for line in tabular_content.split(r"\\"):
        line = line.strip()
        if line and not line.startswith(r"\hline"):  # Skip empty lines and \hline
            # Replace & with commas, remove LaTeX formatting
            cleaned_line = re.sub(r"\\[a-zA-Z]+|[\{\}\$]", "", line)
            row = [col.strip() for col in cleaned_line.split("&")]

            # Check if the first column (Solver) is empty
            if row[0] == "":
                row[0] = last_solver  # Fill missing Solver with last known value
            else:
                last_solver = row[0]  # Update last_solver to the new Solver name
            
            # Randomize float values if the option is enabled
            if randomize_floats:
                row = [
                    str(round(random.uniform(*float_range), 3)) if re.match(r"^\d+(\.\d+)?$", col) else col
                    for col in row
                ]
            rows.append(row)
    
    # Write rows to CSV
    with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(rows)
    
    print(f"Table converted and saved to '{csv_filename}'.")


# def latex_table_to_csv(latex_code, csv_filename, randomize_floats=False, float_range=(0, 100)):
#     """
#     Converts a LaTeX table with single backslashes to a CSV file, with an option to randomize float values.

#     :param latex_code: String containing the LaTeX table.
#     :param csv_filename: Output CSV filename.
#     :param randomize_floats: If True, replaces float values with random numbers.
#     :param float_range: Tuple specifying the range of random float values.
#     """
#     # Clean up the LaTeX input to remove unwanted characters
#     latex_code = latex_code.replace("\x08", "").strip()  # Remove backspace escape sequences

#     # Correct regex to capture tabular content
#     match = re.search(r"\\begin\{tabular\}.*?\\hline(.*?)\\end\{tabular\}", latex_code, re.S)
#     if not match:
#         raise ValueError("No valid tabular environment found in the LaTeX code.")
    
#     tabular_content = match.group(1)
    
#     # Split rows using single backslashes (escaped in regex as `\\\\`)
#     rows = []
#     for line in tabular_content.split(r"\\"):
#         line = line.strip()
#         if line and not line.startswith(r"\hline"):  # Skip empty lines and \hline
#             # Replace & with commas, remove LaTeX formatting
#             cleaned_line = re.sub(r"\\[a-zA-Z]+|[\{\}\$]", "", line)
#             row = [col.strip() for col in cleaned_line.split("&")]
            
#             # Randomize float values if the option is enabled
#             if randomize_floats:
#                 row = [
#                     str(round(random.uniform(*float_range), 3)) if re.match(r"^\d+(\.\d+)?$", col) else col
#                     for col in row
#                 ]
#             rows.append(row)
    
#     # Write rows to CSV
#     with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
#         writer = csv.writer(file)
#         writer.writerows(rows)
    
#     print(f"Table converted and saved to '{csv_filename}'.")


def latex_table_to_csv_v2(latex_code, csv_filename, randomize_floats=False, float_range=(0, 100)):
    """
    Converts a LaTeX table with single backslashes to a CSV file, with an option to randomize float values.
    Specifically for LaTeX tables like the one provided (with p-column width specifiers).

    :param latex_code: String containing the LaTeX table.
    :param csv_filename: Output CSV filename.
    :param randomize_floats: If True, replaces float values with random numbers.
    :param float_range: Tuple specifying the range of random float values.
    """
    # Clean up the LaTeX input to remove unwanted characters
    latex_code = latex_code.replace("\x08", "").strip()  # Remove backspace escape sequences

    # Correct regex to capture tabular content
    match = re.search(r"\\begin\{tabular\}.*?\\hline(.*?)\\end\{tabular\}", latex_code, re.S)
    if not match:
        raise ValueError("No valid tabular environment found in the LaTeX code.")
    
    tabular_content = match.group(1)
    
    # Split rows using single backslashes (escaped in regex as `\\\\`)
    rows = []
    for line in tabular_content.split(r"\\"):
        line = line.strip()
        if line and not line.startswith(r"\hline"):  # Skip empty lines and \hline
            # Replace & with commas, remove LaTeX formatting
            cleaned_line = re.sub(r"\\[a-zA-Z]+|[\{\}\$]", "", line)
            row = [col.strip() for col in cleaned_line.split("&")]
            
            # Randomize float values if the option is enabled
            if randomize_floats:
                row = [
                    str(round(random.uniform(*float_range), 3)) if re.match(r"^\d+(\.\d+)?$", col) else col
                    for col in row
                ]
            rows.append(row)
    
    # Write rows to CSV
    with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(rows)
    
    print(f"Table converted and saved to '{csv_filename}'.")




def latex_to_csv_v3(latex_string, csv_filename, headers, randomize_floats=False, float_range=(0, 100)):
    """
    Converts a LaTeX string table into a CSV file, removes \hline, and optionally randomizes float values.

    :param latex_string: String containing the LaTeX table data.
    :param csv_filename: Output CSV filename.
    :param randomize_floats: If True, replaces float values with random numbers.
    :param float_range: Tuple specifying the range of random float values.
    """
    # Remove \hline and split by lines (\\)
    latex_string = latex_string.replace("\\hline", "")
    rows = latex_string.strip().split("\\\\")
    
    # Process each row
    processed_rows = []
    for row in rows:
        row_data = [col.strip() for col in row.split("&")]
        
        # If randomization is enabled, randomize float values
        if randomize_floats:
            row_data = [
                str(round(random.uniform(*float_range), 3)) if re.match(r"^\d+(\.\d+)?$", col) else col
                for col in row_data
            ]
        
        processed_rows.append(row_data)
    
    # Write to CSV
    with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(headers)  # Write header
        writer.writerows(processed_rows)  # Write data rows

    print(f"Table converted and saved to '{csv_filename}'.")

headers_int = ["Solver", "Turbulence Model", "pressure (kPa)", "Heat Flux (MW/($m^2$))"]
# Table header as a constant
headers_sep = [
    "Solver", "Turbulence Model", "x$_{sep}$ (m)", "p$_{peak}$ (kPa)", "p$_{peak,loc}$ (m)", 
    "q$_{peak}$ (MW/($m^2$))", "q$_{peak,loc}$ (m)"
]

# Example usage
# Example usage
# latex_code = r'''
# \begin{table}[ht]
#     \resizebox{\columnwidth}{!}{%
#     \begin{tabular}{llll}
#     \hline
#     \textbf{Solver} & \textbf{Turbulence Model} & \textbf{pressure (kPa)} & \textbf{heat flux (MW/($m^2$))} \\
#     \hline
#     \hline
#     STAR-CCM+ & k-$\omega$ SST & 44.89 & 0.971 \\
#     \hline
#     Eilmer & k-$\omega$ 2006 & 44.16 & 0.95 \\
#     \hline
#     Ansys Fluent (Aselsan) & SA & 43.73 & 0.624 \\
#     & SA 2-T model & 43.93 & 0.621 \\
#     & k-$\omega$ SST & 43.82 & 0.958 \\
#     & k-$\omega$ SST 2-T model & 44.25 & 0.98 \\
#     \hline
#     SU2 & k-$\omega$ SST & 42.33 & 0.73 \\
#     \hline
#     OVERFLOW & k-$\omega$ SST & 44.39 & 0.696 \\
#     \hline
#     VULCAN & SA-noft2 & 43.71 & 0.631 \\
#     & SA-noft2 2013 QCR-V & 43.88 & 0.756 \\
#     & k-$\omega$ SST & 44.05 & 0.959 \\
#     & k-$\omega$ SST-KL & 44.19 & 0.939 \\
#     & k-$\omega$ SST-V & 44.35 & 0.919 \\
#     & k-$\omega$ SST-V no 2/3 rho*k & 43.81 & 0.93 \\
#     \hline
#     Cadence Fidelity & SSC-EARSM & 44.25 & 0.919 \\
#     & k-$\omega$ SST a1=0.355 & 44.38 & 1.075 \\
#     \hline
#     \end{tabular} 
#     }
#     \caption{Integrated wall quantities for run 4 . Values are scaled by $\int$dx.}
#     \label{tab:res_comparison_integrated_run4}
# \end{table}
# '''
# latex_table_to_csv(latex_code, "run4_integrated_values.csv", 
#                 randomize_floats=False, float_range=(0.1, 1e3))

latex_code_run4_int = r'''
    STAR-CCM+ & k-$\omega$ SST & 44.89 & 0.971 \\
    \hline
    Eilmer & k-$\omega$ 2006 & 44.16 & 0.95 \\
    \hline
    Ansys Fluent (Aselsan) & SA & 43.73 & 0.624 \\
    & SA 2-T model & 43.93 & 0.621 \\
    & k-$\omega$ SST & 43.82 & 0.958 \\
    & k-$\omega$ SST 2-T model & 44.25 & 0.98 \\
    \hline
    SU2 & k-$\omega$ SST & 42.33 & 0.73 \\
    \hline
    OVERFLOW & k-$\omega$ SST & 44.39 & 0.696 \\
    \hline
    VULCAN & SA-noft2 & 43.71 & 0.631 \\
    & SA-noft2 2013 QCR-V & 43.88 & 0.756 \\
    & k-$\omega$ SST & 44.05 & 0.959 \\
    & k-$\omega$ SST-KL & 44.19 & 0.939 \\
    & k-$\omega$ SST-V & 44.35 & 0.919 \\
    & k-$\omega$ SST-V no 2/3 rho*k & 43.81 & 0.93 \\
    \hline
    Cadence Fidelity & SSC-EARSM & 44.25 & 0.919 \\
    & k-$\omega$ SST a1=0.355 & 44.38 & 1.075
'''


latex_to_csv_v3(latex_code_run4_int, "run4_integrated_values.csv", headers_int, 
                randomize_floats=False, float_range=(0.1, 1e3))



latex_code_run4_sep = r'''
    STAR-CCM+ & k-$\omega$ SST & 2.571 & 150.38 & 2.695 & 3.722 & 2.694\\
\hline
Eilmer & k-$\omega$ 2006 & 2.531 & 161.82 & 2.707 & 4.185 & 2.706\\
\hline
Ansys Fluent (Aselsan) & SA & 2.638 & 103.67 & 2.676 & 1.41 & 2.702\\
 & SA 2-T model & 2.636 & 103.77 & 2.677 & 1.392 & 2.708 \\
 & k-$\omega$ SST & 2.509 & 162.8 & 2.719 & 3.836 & 2.718 \\
 & k-$\omega$ SST 2-T model & 2.489 & 163.05 & 2.729 & 3.809 & 2.729 \\
\hline
SU2 & k-$\omega$ SST & 2.639 & 93.62 & 2.685 & 1.743 & 2.678\\
\hline
OVERFLOW & k-$\omega$ SST & 2.415 & 175.32 & 2.753 & 2.534 & 2.742\\
\hline
VULCAN & SA-noft2 & 2.639 & 103.87 & 2.678 & 1.42 & 2.698\\
 & SA-noft2 2013 QCR-V & 2.549 & 145.22 & 2.701 & 2.44 & 2.681 \\
 & k-$\omega$ SST & 2.472 & 173.18 & 2.737 & 4.072 & 2.737 \\
 & k-$\omega$ SST-KL & 2.457 & 171.13 & 2.745 & 3.869 & 2.744 \\
 & k-$\omega$ SST-V & 2.441 & 169.78 & 2.753 & 3.679 & 2.753 \\
 & k-$\omega$ SST-V no 2/3 rho*k & 2.519 & 161.78 & 2.713 & 3.631 & 2.713 \\
\hline
Cadence Fidelity & SSC-EARSM & 2.614 & 109.1 & 2.672 & 3.364 & 2.671\\
 & k-$\omega$ SST a1=0.355 & 2.563 & 127.7 & 2.705 & 3.888 & 2.7
'''
latex_to_csv_v3(latex_code_run4_sep, "run4_separation_peaks.csv", headers_sep, 
                randomize_floats=False, float_range=(0.1, 1e3))



latex_code_run6_int = r'''
    Eilmer & k-$\omega$ 2006 & 50.51 & 1.304 \\
\hline
Ansys Fluent (Aselsan) & k-$\omega$ SST & 50.07 & 1.317 \\
\hline
Cadence Fidelity & SSC-EARSM & 50.81 & 1.227 \\
 & k-$\omega$ SST a1=0.355 & 50.92 & 1.456
'''


latex_to_csv_v3(latex_code_run6_int, "run6_integrated_values.csv", headers_int, 
                randomize_floats=False, float_range=(0.1, 1e3))

latex_code_run6_sep = r'''
    Eilmer & k-$\omega$ 2006 & 2.539 & 219.08 & 2.7 & 6.885 & 2.699\\
\hline
Ansys Fluent (Aselsan) & k-$\omega$ SST & 2.51 & 225.57 & 2.713 & 6.33 & 2.713\\
\hline
Cadence Fidelity & SSC-EARSM & 2.623 & 138.09 & 2.687 & 4.011 & 2.665\\
 & k-$\omega$ SST a$_1$=0.355 & 2.565 & 168.94 & 2.701 & 5.858 & 2.697
'''
latex_to_csv_v3(latex_code_run6_sep, "run6_separation_peaks.csv", headers_sep, 
                randomize_floats=False, float_range=(0.1, 1e3))
