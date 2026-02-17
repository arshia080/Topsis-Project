## TOPSIS Decision Making System

---

## About This Project

This project implements **TOPSIS (Technique for Order Preference by Similarity to Ideal Solution)** in three ways:

1. **Command Line Program (CLI)**
2. **Python Package on PyPI**
3. **Web Application using Streamlit**

TOPSIS is used to **rank options based on multiple criteria**.  
Higher score = better option.

---

## Folder Structure
Topsis-Project/

├─ part1-cli/

├─ part2-package/

├─ part3-webservice/

└─ README.md

---

# Part 1 – CLI Program

### Run Command

`python topsis.py InputFile Weights Impacts OutputFile`

### Example

python topsis.py data.csv "1,1,1,1" "+,+,+,+" result.csv

### Checks Performed

- File must exist  
- Minimum 3 columns  
- First column = names  
- Other columns must be numbers  
- Criteria count = Weights count = Imapcts count 
- Impacts must be `+` or `-`  

---

**CLI Output File Example** 

<img width="777" height="266" alt="Screenshot 2026-02-03 213242" src="https://github.com/user-attachments/assets/f7341560-4881-45f6-8a00-83a7c5d2f102" />

---

# Part 2 – Python Package (PyPI)

### Package Name
topsis-arshia-102317268

### Install
`pip install topsis-arshia-102317268`

### Run Example
`topsis data.xlsx "1,1,1,1" "+,+,+,+" result.csv`

---

## PyPI Screenshots

**PyPI Page**  
<img width="1669" height="1051" alt="image" src="https://github.com/user-attachments/assets/cd34792f-802d-4fea-9e72-6113a8faec05" />

---

# Part 3 – Web Application (Streamlit)

### Live Link
https://topsis-project-arshia.streamlit.app/

### Features

- Upload CSV or Excel file  
- Enter weights and impacts  
- Enter email  
- Result sent to email  
- No file saved on server  
- Dark theme UI  

---

## Web App Screenshots
**Home Page**  
<img width="1919" height="1141" alt="image" src="https://github.com/user-attachments/assets/c9e72825-224c-448b-a1b2-1a5c1fcfc798" />

**Form Submission**
<img width="1919" height="1139" alt="image" src="https://github.com/user-attachments/assets/184f4415-e3dc-421e-bcab-48068b13ef5a" />

**Email Result**  
<img width="1427" height="627" alt="image" src="https://github.com/user-attachments/assets/275b47ec-6161-412b-bb38-c53367f988a4" />

---

# How TOPSIS Works (Simple)

1. Normalize values  
2. Apply weights  
3. Find best and worst values  
4. Measure distance  
5. Calculate score  
6. Rank options  

---

# Technologies Used

- Python  
- Pandas  
- NumPy  
- Streamlit  
- GitHub  
- PyPI  

---

# Run Web App Locally

`pip install streamlit pandas numpy openpyxl`

`streamlit run app.py`

---

# Security

Email credentials are stored using **environment variables / Streamlit secrets**, not in the code.

---

# Author

**Arshia**
