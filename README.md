```markdown
**NeuroMath**

## Usage

### 1️⃣ CLI Mode

Start the CLI interpreter:

```bash
neuromath
```

**Example:**

```
x = 5
f(x) = 3*x^2 + 5*x
diff(f(x), x)
```

**Output:**

```
6*x + 5
```

### 2️⃣ GUI Mode (Notebook Style)

Launch Streamlit interface:

```bash
neuromath-gui
```

This opens a browser-based notebook interface for interactive symbolic computation.

---

## Language Syntax

### Variable Assignment
```
x = 10
y = x + 5
```

### Function Definition
```
f(x) = x^2 + 3*x
```

### Function Call
```
f(2)
```

### Differentiation
```
diff(f(x), x)
```

### Built-in Constants
- `pi`
- `e`

---

## 📘 Example Program

```
y = 3
z = y + 4
print(z)

f(x) = x^2 + 3*x
print(diff(f(x), x))
```

---

## 🏗️ Project Structure

```
neuromath/
│
├── lexer/
├── parser/
├── interpreter/
|-──semantic/
├── main.py
├── gui.py
└── app.py
```

---

## ⚙️ Requirements

- Python >= 3.9
- sympy >= 1.12
- numpy >= 1.26
- streamlit

---

## 🛠 Development Setup

1. **Clone repository:**

```bash
git clone https://github.com/yourusername/neuromath.git
cd neuromath
```

2. **Create virtual environment:**

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. **Install in editable mode:**

```bash
pip install -e .[dev]
```

4. **Run tests:**

```bash
pytest
```

5. **Build package:**

```bash
python -m build
```

6. **Upload to PyPI:**

```bash
twine upload dist/*
```

---

##  Testing

NeuroMath includes unit tests for:

- Lexer
- Parser
- Interpreter
- Function evaluation
- Differentiation

**Run:**

```bash
pytest
```

---

## 🔮 Roadmap

- Integration support
- Matrix operations
- Simplification engine
- LaTeX output
- Jupyter kernel support
- Neural-symbolic extensions

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repo
2. Create a feature branch
3. Submit a pull request

---

## 📄 License

MIT License

---

## 👨‍💻 Author

Anil Khatiwada
```
