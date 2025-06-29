---
# Data Analysis Agent

An intelligent, CLI-based multi-functional **data analysis assistant** powered by LLMs, `LangChain`, and `pandas`. It helps users explore datasets using **natural language queries**, generate **code**, produce **visualizations**, and even suggest exploratory questions.

---

## Features

- **LLM-Driven Query Understanding** (via `ChatGroq`)
- **Smart Pandas Code Generation**
- **Seaborn/Matplotlib Visualization Generator**
- **Conversational Agent** using LangChain's ReAct framework
- **Auto-Summarization** of complex analysis
- **Natural Language Suggestions** for what to explore next

---

## Folder Structure

```

.
├── data_analysis_agent.py  # Main script with CLI + all tools
├── requirements.txt        # Required packages
├── output/                 # Stores plots as .png files

````

##  Workflow Breakdown

### Step 1: Load Dataset

* The agent prompts for a `.csv` or `.json` file path.
* It auto-detects encoding and loads the dataset into memory.
* Schema is extracted (column names, types, and shape).

### Step 2: Accept Natural Language Queries

* Examples:

  * "Show me the top 10 rows"
  * "Find the correlation between age and income"
  * "Visualize missing data"
  * "Plot distribution of all numeric features"

### Step 3: Classify the Query

* LLM classifies the query as:

  * **Simple**: direct queries (head, describe)
  * **Complex**: analytical queries (grouping, insights)

### Step 4: Generate Code or Plot

* Based on complexity:

  * **Pandas code** is generated and executed.
  * Or, **matplotlib/seaborn** visualization code is generated and rendered.

### Step 5: Return Results

* The result is printed in the terminal.
* For visual queries, plots are saved in the `output/` folder and auto-opened.

---

## Tools Overview

| Tool Name             | Purpose                                         |
| --------------------- | ----------------------------------------------- |
| `smart_analysis_tool` | Generates and executes pandas analysis code     |
| `visualization_tool`  | Generates and executes matplotlib/seaborn plots |
| `suggestion_tool`     | Suggests next analysis questions to explore     |

---

## 📎 Example Queries

* `What is the average salary by department?`
* `Describe the dataset`
* `Plot a histogram of all numeric columns`
* `Show me rows where age > 40`
* `suggestions` → (gets 5–6 LLM-generated analysis ideas)

---

## Notes

* Avoid unsafe commands like `os.system`, `exec`, etc. They’re blocked by default.
* This is **interactive CLI software** — run the script and ask questions in real time.

