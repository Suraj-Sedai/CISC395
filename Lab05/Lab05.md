# Lab 5: AI Agents - Terminal-Based AI Operations
## CISC 395 - Applied Generative AI and LLM Applications

**Due:** [Date specified on Blackboard]

**Submission:** Upload to Blackboard — `Lab05_YourName.md` + generated files (see checklist)

---

## Prerequisites

**Complete before the lab begins.**

### Set Up Your Workspace and Download Lab Files

Open VS Code, then open the `CISC395/` folder (`File > Open Folder`). Open the integrated terminal (`` Ctrl+Shift+` `` on Windows, `` Cmd+Shift+` `` on Mac). Run:

```bash
mkdir Lab05
cd Lab05

# Download (curl is built-in on Mac and Windows 10/11)
curl -o Lab05.zip "https://raw.githubusercontent.com/tisage/CISC395/refs/heads/main/Lab05/Lab05.zip"

# Unzip (Mac / Linux)
unzip Lab05.zip

# Unzip (Windows)
tar -xf Lab05.zip

cd ..
```

Verify structure from the workspace root:

```bash
tree Lab05        # Mac/Linux
tree /F Lab05     # Windows
```

Expected:
```
Lab05/
├── data/
│   └── student_grades.csv
├── code/
│   ├── calculator.py
│   └── buggy_sort.py
├── messy/
│   └── [10 poorly-named files]
└── papers/
    └── [research paper PDF]
```

---

## Overview

| Exercise | Topic | Deliverable |
|----------|-------|-------------|
| 1 | Workspace Setup and Context File | `GEMINI.md` + answers in this file |
| 2 | AI-Powered Paper Reading | `papers/paper_summary.md` + answers in this file |
| 3 | Grade Data Analysis | `data/grade_report.md` + answers in this file |
| 4 | Digital Organization Challenge | reorganized `messy/` + answers in this file |
| Reflection | | answers in this file |

**No coding required.** All exercises use terminal AI sessions.

**How to enter a session:**
```bash
gemini       # Gemini CLI
copilot      # GitHub Copilot CLI
```

---

## Exercise 1: Workspace Setup and Context File (20 points)

### Part A: Enter Your First Session

Navigate into `Lab05/` and start a session:

```bash
cd Lab05
gemini
```

Approve the folder trust prompt when it appears.

**Screenshot:** Take a screenshot of the session start (`screenshot_01.png`).

---

### Part B: Create Your GEMINI.md

Inside the session, ask AI to draft a `GEMINI.md` context file for this project and save it:

**The prompt you used:**
```
 > explain me Lab05 Folder

 > write in something like
   """The folder has
   a CSV with student grades, two Python files, and a messy/ folder.

```

After saving, verify it loaded:
```
> /memory show
```

**`/memory show` output (first 3–5 lines is enough):**
```

# Lab 05 Project Context

This folder is part of **Lab 05: AI Agents - Terminal-Based AI Operations** for CISC 395. 
                                  
[Paste just enough to confirm the context file was loaded]

```

> `GEMINI.md` will be submitted as a separate file — do not paste its full content here.

---

### Part C: Test Your Context

With `GEMINI.md` loaded, ask AI about `code/buggy_sort.py` — without describing it yourself:

```
> Look at code/buggy_sort.py and explain what it does. Is there a bug?
```

**AI's response:**
```
 The file code/buggy_sort.py contains several functions that implement common algorithms like bubble sort, binary search, counting occurrences, and removing duplicates.


  The code contains several intentional bugs as listed below:


  1. `bubble_sort` Bug
   * What it does: It sorts an array by repeatedly swapping adjacent elements if they are in the wrong order.
   * The Bug: The inner loop for j in range(0, n - i): is incorrect. Because it accesses arr[j + 1], when j reaches n - i, it will try to access an index out of bounds (n - i + 1).
   * Fix: It should be range(0, n - i - 1).


  2. `binary_search` Bugs
   * What it does: It searches for a target value in a sorted array using a divide-and-conquer approach.
   * The Bug (Initial Boundary): right = len(arr) will cause an IndexError if the target is larger than all elements, as mid could become len(arr). It should be len(arr) - 1.
   * The Bug (Infinite Loop): left = mid will cause an infinite loop if the target is not found or is in the right half of the current range, as left never moves past the midpoint. It   
     should be left = mid + 1.


  3. `count_occurrences` Bug
   * What it does: Counts how many times a target appears in a list.
   * The Bug: range(len(arr) + 1) will cause an IndexError when i reaches len(arr).
   * Fix: It should be range(len(arr)).


  4. `remove_duplicates` Bug
   * What it does: Intended to return a new list with only unique elements from the original list.
   * The Bug: The condition if item not in lst: is logically flawed. It checks if the item is in the original list (which it always is), so it will never add anything to result.
   * Fix: It should be if item not in result:.

```

**Reflection:** Did AI correctly identify the bug without any hints? Did having `GEMINI.md` make a difference compared to asking cold? (2–3 sentences)

```
Yes AI correctly indentify the bug without any hints, having the GEMINI.md file helped to identify that there are some intentional bugs.
```

---

## Exercise 2: AI-Powered Paper Reading (30 points)

### Required Sections

Your `paper_summary.md` must contain all five sections:

| # | Section | What it should cover |
|---|---------|----------------------|
| 1 | **Introduction** | What the paper proposes and its key contribution |
| 2 | **Core Principles** | The key technical idea or methodology |
| 3 | **Impact and Influence** | Why this paper matters and how widely adopted |
| 4 | **Influence on Modern AI** | How the paper's ideas appear in today's systems |
| 5 | **Relevance to Your Major** | How this connects to your major/career — your own words |

### Write and Run Your Prompt

Write a prompt that reads the PDF, applies at least two techniques from Units 2–3, requires all five sections, and saves the result as `papers/paper_summary.md`.

**Your prompt:**
```
[Write your complete prompt here]

You are an AI research professor and technical writing mentor.

TASK:
Read the attached PDF research paper in papers/1706.03762v7.pdf and generate a structured markdown summary saved as:

papers/paper_summary.md

INSTRUCTIONS:
- Analyze the full paper carefully.
- Identify the main contribution, core methodology, and broader impact.
- Think step-by-step before writing.
- Use clear academic language.
- Do not copy text directly from the paper.

REQUIRED FORMAT (STRICT):

# Paper Summary

## 1. Introduction
Explain the research problem and key contribution.

## 2. Core Principles
Explain the main technical idea and how it works.

## 3. Impact and Influence
Describe why this paper matters and its adoption or influence.

## 4. Influence on Modern AI
Connect the paper’s ideas to modern AI systems or architectures.

## 5. Relevance to My Major (Computer Science – AI/ML Focus)
Write in first person. Explain how this paper connects to my AI/ML career path.

ADDITIONAL REQUIREMENTS:
- Use proper markdown formatting.
- Minimum 600 words.
- Ensure all five sections are included.
- Save the output as: papers/paper_summary.md

Techniques used: [e.g., "Role Prompting + Structured Output"]
```

> `papers/paper_summary.md` will be submitted as a separate file — do not paste its content here.

**Reflection:**

1. Which section did AI handle best? Which was weakest? Why? (2–3 sentences)

```
The CLI AI handels the folder paths and the file inside really well and understand all the folders which is really good.
```

2. Did you need to refine your prompt or ask follow-up questions? What worked and what did not? (2–3 sentences)

```
Yeah, refininf prompt or follow ups is really useful. Sometimes just follow ups question generated the things I wanted to.

[Your answer]
```

---

## Exercise 3: Grade Data Analysis (25 points)

### Part A: Explore the Data

Ask at least three different questions about `data/student_grades.csv`. For each, paste your prompt and the AI's response.

**Suggested questions (choose 3 or write your own):**
- What is the grade distribution (A/B/C/D/F)?
- Who are the top 3 students by total score?
- Which students are at risk (below 70%)?
- What is the class average, highest, and lowest score?

---

**Question 1 — Your prompt:**
```
[Paste your prompt]
Analyze the file data/student_grades.csv.

1. Calculate each student's total score and percentage.
2. Categorize each student into letter grades using:
   A = 90–100
   B = 80–89
   C = 70–79
   D = 60–69
   F = below 60
3. Show the overall grade distribution (count of A, B, C, D, F).
4. Present the result in a clear table.

```
**AI's response:**
```
I will analyze the data/student_grades.csv data. It seems the file already contains Total and Grade columns, but I will recalculate them based on your specific criteria (Total Score   
  and Percentage) and the provided grading scale (A=90-100, B=80-89, etc.), as the existing "Grade" column uses +/- modifiers which your request simplifies.


  Assumptions:
   * The Total column in the CSV seems to be a weighted average or percentage already, as the values are like 87.2, 96.1, etc.
   * However, looking at the raw scores (Labs ~100, Midterm ~100, Final ~100), if I sum them up, they would exceed 100.
   * Let's check the CSV header again: Lab1,Lab2,Lab3,Lab4,Midterm,Final.
   * If I simply sum them: 4 labs + Midterm + Final = 6 items. If each is out of 100, the total possible is 600.
   * The existing Total column in the CSV looks like a percentage (average of the 6 items? or weighted?).
       * Example S001: (95+88+92+85+78+82) / 6 = 520 / 6 = 86.66... The CSV says 87.2. Maybe weights are involved.
   * Decision: Since I don't have the syllabus weighting, I will assume the Total column in the CSV is the final percentage score to be used for grading. I will use that column to apply 
     your specific A/B/C/D/F buckets.


  Analysis of Student Grades

  Here is the breakdown based on the Total column provided in the file, applying your grading scale:



  ┌───────────┬────────────────┬─────────────┬──────────────┐
  │ StudentID │ Name           │ Total Score │ Letter Grade │
  ├───────────┼────────────────┼─────────────┼──────────────┤
  │ S001      │ Alice Chen     │ 87.2        │ B            │
  │ S002      │ Bob Johnson    │ 65.3        │ D            │
  │ S003      │ Carol Williams │ 96.1        │ A            │
  │ S004      │ David Lee      │ 80.2        │ B            │
  │ S005      │ Emma Davis     │ 55.8        │ F            │
  │ S006      │ Frank Martinez │ 90.0        │ A            │
  │ S007      │ Grace Kim      │ 77.3        │ C            │
  │ S008      │ Henry Brown    │ 87.5        │ B            │
  │ S009      │ Iris Taylor    │ 67.2        │ D            │
  │ S010      │ James Wilson   │ 97.1        │ A            │
  │ S011      │ Kate Anderson  │ 78.0        │ C            │
  │ S012      │ Liam Thomas    │ 56.2        │ F            │
  │ S013      │ Mia Jackson    │ 91.0        │ A            │
  │ S014      │ Noah White     │ 74.1        │ C            │
  │ S015      │ Olivia Harris  │ 96.5        │ A            │
  │ S016      │ Peter Clark    │ 66.3        │ D            │
  │ S017      │ Quinn Lewis    │ 86.5        │ B            │
  │ S018      │ Rachel Walker  │ 91.2        │ A            │
  │ S019      │ Sam Hall       │ 64.3        │ D            │
  │ S020      │ Tina Young     │ 84.2        │ B            │
  └───────────┴────────────────┴─────────────┴──────────────┘

  Overall Grade Distribution

  ┌──────────────────┬───────┐
  │ Grade            │ Count │
  ├──────────────────┼───────┤
  │ A (90-100)   │ 6     │
  │ B (80-89)    │ 5     │
  │ C (70-79)    │ 3     │
  │ D (60-69)    │ 4     │
  │ F (Below 60) │ 2     │
  └──────────────────┴───────┘



  Summary:
   * Class Size: 20 Students
   * Most Common Grade: A (6 students)
   * Pass Rate (D or better): 90% (18/20)
   * Fail Rate: 10% (2/20)

                                                                                                                                                                          ? for shortcuts 
──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
 auto-accept edits shift+tab to manual    
 ```

---

**Question 2 — Your prompt:**
```
Using data/student_grades.csv:

1. Compute the total score and percentage for each student.
2. Identify the top 3 students based on total score.
3. Display their names, total scores, and percentages.
4. Sort the results from highest to lowest.

```
**AI's response:**
```
I will analyze the data/student_grades.csv data to find the top 3 students.


  Assumptions & Calculation:
   * Total Score: The CSV already has a Total column which appears to be a calculated percentage (e.g., 87.2, 96.1). I will treat this as the definitive "Total Score" for ranking
     purposes.
   * Percentage: Since the Total column is already normalized (out of 100), the "Total Score" and "Percentage" are effectively the same value here.

  Top 3 Students

  Based on the Total column in data/student_grades.csv:


   1. James Wilson (S010)
       * Total Score: 97.1
       * Percentage: 97.1%


   2. Olivia Harris (S015)
       * Total Score: 96.5
       * Percentage: 96.5%

   3. Carol Williams (S003)
       * Total Score: 96.1
       * Percentage: 96.1%


  Honorable Mention:
   * Rachel Walker (S018) follows closely with 91.2%.
```

---

**Question 3 — Your prompt:**
```
Analyze data/student_grades.csv and answer the following:

1. Calculate the class average percentage.
2. Identify the highest and lowest scoring students.
3. List any students scoring below 70% and mark them as "At Risk".
4. Present the results clearly with appropriate formatting.
```
**AI's response:**
```
I will analyze the data/student_grades.csv file to calculate class statistics, identify high and low performers, and flag students at risk.


  1. Class Average Percentage
  Based on the Total column for all 20 students:
   * Sum of Scores: 1589.5
   * Class Average: 79.48%

  2. Highest and Lowest Scoring Students



  ┌───────────────────┬──────────────┬────────────┬─────────────┐
  │ Rank              │ Name         │ Student ID │ Total Score │
  ├───────────────────┼──────────────┼────────────┼─────────────┤
  │ Highest Score │ James Wilson │ S010       │ 97.1%   │
  │ Lowest Score  │ Emma Davis   │ S005       │ 55.8%   │
  └───────────────────┴──────────────┴────────────┴─────────────┘



  3. Students "At Risk" (Scoring Below 70%)
  The following 6 students are currently scoring below the 70% threshold:



  ┌────────────┬─────────────┬─────────────┬─────────────┐
  │ Student ID │ Name        │ Total Score │ Status      │
  ├────────────┼─────────────┼─────────────┼─────────────┤
  │ S002       │ Bob Johnson │ 65.3%       │ At Risk │
  │ S005       │ Emma Davis  │ 55.8%       │ At Risk │
  │ S009       │ Iris Taylor │ 67.2%       │ At Risk │
  │ S012       │ Liam Thomas │ 56.2%       │ At Risk │
  │ S016       │ Peter Clark │ 66.3%       │ At Risk │
  │ S019       │ Sam Hall    │ 64.3%       │ At Risk │
  └────────────┴─────────────┴─────────────┴─────────────┘



  4. Summary of Findings
   * The class is performing well overall with an average of nearly 80%.
   * 30% of the class (6 out of 20) is currently in the "At Risk" category, primarily due to low Midterm and Final scores compared to their Lab performance.
   * The top three students (James Wilson, Olivia Harris, Carol Williams) are all performing at an exceptional level (96%+).

  
```

---

### Part B: Generate a Grade Report

Ask AI to synthesize findings into `data/grade_report.md` (class stats, top performers, students needing support, one recommendation).

**Your prompt:**
```
Using the analysis of data/student_grades.csv, generate a professional markdown report saved as:

data/grade_report.md

The report should include the following sections:

# Grade Report

## 1. Class Statistics
- Total number of students
- Class average percentage
- Highest score (student name and percentage)
- Lowest score (student name and percentage)
- Grade distribution (A/B/C/D/F)

## 2. Top Performers
- List the top 3 students with their total scores and percentages

## 3. Students Needing Support
- List students scoring below 70%
- Clearly label them as "At Risk"

## 4. Recommendation
- Provide one clear, actionable recommendation to improve overall class performance

Format the report professionally using proper markdown headings, bullet points, and clean formatting.
Do not include code — only the final markdown content.
```

**Verify the file was created** (paste one line of terminal output):
```
[e.g.,   dir data   →   student_grades.csv   grade_report.md]
```

> `data/grade_report.md` will be submitted as a separate file — do not paste its content here.

---

## Exercise 4: Digital Organization Challenge (15 points)

### Part A: Show the Current State

Run `dir messy` (Windows) or `ls messy` (Mac/Linux) and paste the output:

```
[Paste terminal output showing all 10 files]

    Directory: D:\Projects\CISC395\Lab05\messy


Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
-a----         2/23/2026   5:16 PM             68 20241103_assignment_submission_DONE.txt
-a----         2/23/2026   5:16 PM             36 asdfghjkl.csv
-a----         2/23/2026   5:16 PM            100 Copy of notes week2(1).txt
-a----         2/23/2026   5:16 PM             58 file_backup_old2.txt
-a----         2/23/2026   5:16 PM             94 hw1 FINAL(2) v3.txt
-a----         2/23/2026   5:16 PM             83 NEW new version script REVISED.txt
-a----         2/23/2026   5:16 PM             94 report draft REAL one.docx.txt
-a----         2/23/2026   5:16 PM             58 temp.py
-a----         2/23/2026   5:16 PM             94 Untitled Document (3).txt
-a----         2/23/2026   5:16 PM             26 untitled1.py

```

---

### Part B: Ask AI to Propose an Organization Plan

Ask AI to analyze `messy/`, propose a folder structure as a tree diagram, assign each file to a subfolder with a reason, and suggest better names — **without moving anything yet**.

**Your prompt:**
```
Analyze the following directory listing from:

D:\Projects\CISC395\Lab05\messy

Your task:

1. Propose a clean, professional folder structure for organizing this directory.
2. Show the proposed structure as a tree diagram.
3. Assign each existing file to a specific subfolder.
4. Suggest a clearer, standardized filename for each file.
5. Briefly explain the reason for each placement and rename decision.
6. Do NOT move or modify anything — this is only a proposed plan.

The goal is to improve clarity, maintainability, and professional project organization.
Format the response clearly with headings and a tree diagram.

```

**AI's proposed plan:**
```
1. Proposed Folder Structure
  A clean, category-based structure is proposed to separate formal submissions, raw data, working scripts, and archived materials.


   1 messy/
   2 ├── assignments/         # Formal lab and homework submissions
   3 ├── data/                # Datasets and CSV files
   4 ├── notes/               # Study notes and project ideation
   5 ├── reports/             # Progress tracking and presentation scripts
   6 ├── scripts/             # Python code and development tests
   7 └── archive/             # Superseded or redundant files

  2. File Assignment and Renaming Plan



  ┌───────────────────────────────────────────┬──────────────────────────────────┬──────────────────┐
  │ Current Filename                          │ Proposed Standardized Filename   │ Target Subfolder │
  ├───────────────────────────────────────────┼──────────────────────────────────┼──────────────────┤
  │ 20241103_assignment_submission_DONE.txt │ lab03_submission_20241103.txt  │ assignments/   │
  │ hw1 FINAL(2) v3.txt                     │ hw01_llm_introduction.txt      │ assignments/   │
  │ asdfghjkl.csv                           │ sample_student_scores.csv      │ data/          │
  │ Copy of notes week2(1).txt              │ week02_notes_prompt_eng.txt    │ notes/         │
  │ Untitled Document (3).txt               │ final_project_ideas.txt        │ notes/         │
  │ NEW new version script REVISED.txt      │ week04_presentation_script.txt │ reports/       │
  │ report draft REAL one.docx.txt          │ week03_progress_report.txt     │ reports/       │
  │ temp.py                                 │ test_hello_world.py            │ scripts/       │
  │ untitled1.py                            │ test_simple_math.py            │ scripts/       │
  │ file_backup_old2.txt                    │ superseded_backup_2024.txt     │ archive/       │

```

---

### Part C: Evaluate and Implement

**Your evaluation:** Do you agree with the plan? What would you change? (2–3 sentences)

```
I am agree with the plan, all the file is well organized in the specific folder and the naming is really good and accordingly.
```

Ask AI to execute the plan. Show the result:

```bash
tree messy        # Mac/Linux
tree /F messy     # Windows
```

**`tree messy` output after reorganization:**
```
D:\PROJECTS\CISC395\LAB05\MESSY
├───archive
│       superseded_backup_2024.txt
│       
├───assignments
│       hw01_llm_introduction.txt
│       lab03_submission_20241103.txt
│       
├───data
│       sample_student_scores.csv
│       
├───notes
│       final_project_ideas.txt
│       week02_notes_prompt_eng.txt
│       
├───reports
│       week03_progress_report.txt
│       week04_presentation_script.txt
│       
└───scripts
        test_hello_world.py
        test_simple_math.py
```

---

## Reflection (10 points)

**1. Session vs. Single Command**

This lab used session-based interaction where AI built up context across multiple messages. How did that change the quality of results compared to asking one-off questions? Give a specific example from your session. (3–4 sentences)

```
Session-based interaction improved the results because the AI remembered previous steps and built on them. For example, after analyzing the grade data, it used the same results to create the final grade report without recalculating everything. This made the output more accurate and consistent. With one-off questions, I would have had to repeat information each time.

```

**2. Permissions**

Describe one moment where AI asked your permission before taking an action. What did it want to do, and did you review the content before approving? (2–3 sentences)

```
When I asked the AI to organize the messy folder according to the proposed plan, it asked for permission before making any changes. It wanted to confirm before moving and renaming the files. I reviewed the suggested structure and file names first, then approved the plan before proceeding.
```

**3. One Real Use Case**

Name one task from your actual student or professional life that you will use terminal AI for after this lab. Be specific: what folder, what prompt, what output. (2–3 sentences)

```
I will use terminal AI to organize my D:\Projects\ML_Experiments\ folder, where I store different machine learning model versions and datasets. I would prompt it: “Analyze this directory, group models, datasets, and notebooks into a clean research structure, suggest standardized names, and generate a reorganization plan.” The expected output would be a tree diagram, renamed file suggestions, and a step-by-step reorganization plan I can approve before applying.
```

---

## Submission Checklist

**Upload all of the following to Blackboard:**

- [ ] `Lab05_YourName.md` — this file, fully filled in
- [ ] `GEMINI.md` — your context file (from Exercise 1B)
- [ ] `papers/paper_summary.md` — AI-generated paper summary (from Exercise 2)
- [ ] `data/grade_report.md` — AI-generated grade report (from Exercise 3B)
- [ ] `screenshot_01.png` — session start screenshot (from Exercise 1A)

> The reorganized `messy/` folder is verified by the `tree` output pasted in Exercise 4C — no separate upload needed.

---

## Grading Rubric

| Component | Points | Criteria |
|-----------|--------|----------|
| **Exercise 1** | **20** | |
| Screenshot (session start) | 5 | Screenshot shows successful session with folder authorization |
| Prompt + `/memory show` | 8 | Prompt is complete; `/memory show` confirms context loaded |
| Code context test | 7 | AI response pasted; reflection shows understanding of why context helps |
| **Exercise 2** | **30** | |
| Prompt design (2+ techniques) | 10 | Techniques named and correctly applied |
| `paper_summary.md` (submitted file) | 15 | All 5 sections present and substantive; Section 5 in student's own words |
| Reflection | 5 | Honest evaluation of AI output quality |
| **Exercise 3** | **25** | |
| 3 prompts + AI responses | 15 | Questions are specific; responses are accurate and informative |
| `grade_report.md` (submitted file) | 10 | Report includes stats, insights, and a recommendation |
| **Exercise 4** | **15** | |
| Before state shown | 3 | All 10 files visible in terminal output |
| Organization prompt + AI plan | 8 | Plan is logical; student evaluates it critically |
| Tree output after reorganization | 4 | Files moved and renamed; folder structure visible |
| **Reflection** | **10** | |
| Session context reflection | 4 | Specific example cited |
| Permissions moment | 3 | Concrete example from the session |
| Future use case | 3 | Realistic and specific |
| **Total** | **100** | |

---

## Common Commands Reference

**Navigation**

| Task | Windows | Mac / Linux |
|------|---------|-------------|
| Show current path | `cd` | `pwd` |
| Go into a folder | `cd Lab05` | `cd Lab05` |
| Go up one level | `cd ..` | `cd ..` |
| List files | `dir` | `ls` |
| List a subfolder | `dir data` | `ls data` |
| Show folder tree | `tree /F` | `tree` |

**Gemini CLI**

| Command | What it does |
|---------|--------------|
| `gemini` | Enter an interactive session |
| `/memory show` | Display loaded GEMINI.md context |
| `/memory refresh` | Reload GEMINI.md after editing |
| `/compress` | Compress long conversation |
| `/quit` | Exit the session |

**GitHub Copilot CLI**

| Command | What it does |
|---------|--------------|
| `copilot` | Enter an interactive session |
| `/compact` | Compress long conversation |
| `/quit` | Exit the session |

---

**Estimated time:** 90 minutes in class, with optional finishing at home

**End of Lab 5**
