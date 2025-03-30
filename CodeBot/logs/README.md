# CodeBot Project (AI-Oriented Documentation)

## **Overview**
CodeBot is an AI-driven tool designed to automate code analysis, mutation, and optimization. It uses genetic algorithms and external AI engines to iteratively improve its own codebase.

---

## **Core Features**
1. **Genetic Algorithms**:
   - Handles population generation, mutation, crossover, and selection.
   - Evaluates code quality using fitness functions.

2. **AI Integration**:
   - Leverages external AI tools for advanced code analysis and mutation guidance.

3. **Self-Improvement**:
   - Iteratively rewrites its own codebase to improve functionality and performance.

4. **Logging and Debugging**:
   - Maintains detailed runtime logs for debugging and performance monitoring.

5. **Human-AI Collaboration**:
   - Provides a chatbot interface for natural language interaction.
   - Interacts with human users to receive feedback and refine its processes.

---

## **Folder Structure**
The `CodeBot` folder is organized as follows:
```
c:\dev\CodeBot\
├── codebot_core.py
├── core\
│   ├── ai_engine.py
│   ├── self_improvement.py
│   ├── analyze_structure.py
├── genetic\
│   ├── genetic_algorithm.py
│   ├── genetic_iteration.py
│   ├── genetic_optimizer.py
│   ├── genetic_structure.py
│   ├── genetic_population.py
├── modules\
│   ├── file_manager.py
│   ├── text_injector.py
│   ├── ui_interface.py
├── storage\
│   ├── folder_dev_structure.json
│   ├── folder_codebot_structure.json
├── tests\
│   ├── test_codebot_core.py
│   ├── test_pipeline.py
├── requirements.txt
├── pytest.ini
├── README.md
```

---

## **How to Run**
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run CodeBot:
   ```bash
   python codebot_core.py
   ```
3. Run Genetic Algorithm:
   ```bash
   python genetic/genetic_algorithm.py
   ```

---

## **Recent Changes**

### **1. Relocation of `codebot_core.py`**
- `codebot_core.py` has been moved to the main `CodeBot` folder for better accessibility and to act as the primary entry point for the project.

### **2. Removal of `utils.py`**
- The `utils.py` file has been removed to streamline the project structure.
- Functions previously in `utils.py` have been relocated:
  - `get_valid_file_path` is now in `genetic_optimizer.py`.

### **3. Refactored `get_valid_file_path`**
- **Location**: `genetic/genetic_optimizer.py`
- **Purpose**: Validates file paths provided by the user.
- **Usage**:
  - Used in `codebot_core.py` for file injection commands.
  - Used in `self_improvement.py` for analyzing code files.

```python
def get_valid_file_path(prompt="Enter file path: "):
    """
    Prompts the user for a file path and validates its existence.
    """
    while True:
        file_path = input(prompt).strip()
        if os.path.exists(file_path):
            return file_path
        print("Invalid file path. Please try again.")
```

### **4. Expanded `sanitize_input`**
- **Location**: `genetic/genetic_optimizer.py`
- **Purpose**: Sanitizes user input for various contexts (`general`, `code`, `file_path`, `html`, `json`).
- **Enhancements**:
  - Added JSON validation logic.
  - Improved error handling for invalid inputs.

---

## **Key Modules and Their Roles**

### **1. Main Entry Point**
- **`codebot_core.py`**:
  - Acts as the main entry point for the project.
  - Implements the `Chatbot` class for natural language interaction.
  - Routes commands through the `exchange_layer` function to appropriate modules.

### **2. Core**
- **`ai_engine.py`**:
  - Integrates with Hugging Face Transformers for AI-driven code analysis.
  - Provides functions like `explain_python_code` and `suggest_code_improvements`.

- **`self_improvement.py`**:
  - Implements logic for CodeBot's self-improvement using genetic algorithms.
  - Uses `get_valid_file_path` for file-based operations.

### **3. Genetic**
- **`genetic_optimizer.py`**:
  - Contains core utilities like `sanitize_input` and `get_valid_file_path`.
  - Implements genetic optimization logic for improving code quality.

- **`genetic_algorithm.py`**:
  - Handles population generation, mutation, crossover, and selection.

- **`genetic_iteration.py`**:
  - Manages iterative processes for genetic algorithms.

### **4. Modules**
- **`file_manager.py`**:
  - Provides utilities for file operations like setup and cleanup.

- **`text_injector.py`**:
  - Handles text injection into files at specified positions.

- **`ui_interface.py`**:
  - Implements a graphical user interface for interacting with CodeBot.

---

## **Command Reference**

### **Chatbot Commands**
1. **Explain Python Code**:
   - Command: `explain python <code_snippet>`
   - Example:
     ```bash
     explain python def add(a, b): return a + b
     ```

2. **Validate JSON**:
   - Command: `validate json <json_string>`
   - Example:
     ```bash
     validate json {"key": "value"}
     ```

3. **Run Genetic Algorithm**:
   - Command: `run genetic algorithm`

4. **Inject Text**:
   - Command: `inject text`
   - Prompts for file path, text, and injection mode (`append`, `overwrite`, `insert`).

5. **Setup Project Structure**:
   - Command: `setup project`

---

## **Future Goals**

1. **Enhanced Genetic Algorithms**:
   - Improve fitness functions to evaluate code quality more comprehensively.
   - Add support for multi-objective optimization.

2. **AI Integration**:
   - Integrate with external AI engines for advanced code analysis and optimization.

3. **Scalability**:
   - Optimize CodeBot to handle larger codebases and more complex workflows.

4. **Documentation**:
   - Expand this README with detailed explanations of each module and function.

---

## **Contact**
For further assistance, please interact with the CodeBot system or consult the runtime logs.
