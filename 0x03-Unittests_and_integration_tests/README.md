
# 📦 0x03 - Unittests and Integration Tests

This directory contains unit and integration tests for the `utils.access_nested_map` function, as part of the **ALX Backend Python** curriculum. The goal is to ensure correctness, robustness, and maintainability of utility functions through parameterized and structured testing.

---

## 🧪 Contents

- **`test_utils.py`**  
  Implements unit tests for the `access_nested_map` function using `unittest` and `parameterized`.

---

### 🔍 What’s Tested

#### `access_nested_map(nested_map, path)`

This function retrieves a value from a nested dictionary using a sequence of keys.

#### ✅ Unit Tests

- **TestAccessNestedMap**
  - Uses `@parameterized.expand` to test multiple input scenarios
  - Verifies correct value retrieval from nested dictionaries
  - Ensures concise, readable test logic (≤ 2 lines per test)

---

### 🛠️ Setup

1. **Clone the repository** (if not already):

   ```bash
   git clone https://github.com/your-username/alx-backend-python.git
   cd alx-backend-python/0x03-Unittests_and_integration_tests
   ```

2. **Create and activate a virtual environment**:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

   Or manually:

   ```bash
   pip install parameterized
   ```

---

### 🚀 Running Tests

```bash
python3 -m unittest test_utils.TestAccessNestedMap
```

Or run all tests in the file:

```bash
python3 -m unittest test_utils
```
