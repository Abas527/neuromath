
# NeuroMath

**Usage**

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
git clone https://github.com/Abas527/neuromath.git
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

---
### Functions

## Built-in Functions

### Basic Operations

| Function | Description |
|----------|-------------|
| `print(value)` | Print output to console |
| `typeof(value)` | Get type of value |
| `shape(matrix)` | Get matrix dimensions |
| `det(matrix)` | Calculate matrix determinant |
| `trans(matrix)` | Transpose matrix |
| `inv(matrix)` | Calculate matrix inverse |

###  Matrix Operations

| Function | Description |
|----------|-------------|
| `identity(n)` | Create n×n identity matrix |
| `zeroes(rows, cols)` | Create matrix filled with zeros |
| `dot(v1, v2)` | Dot product of vectors |
| `cross(v1, v2)` | Cross product of vectors |
| `norm(v)` | Vector norm/magnitude |
| `unit(v)` | Convert to unit vector |

###  Linear Algebra Functions

| Function | Description |
|----------|-------------|
| `eigenval(matrix)` | Calculate eigenvalues |
| `eigenvec(matrix)` | Calculate eigenvectors |
| `solve_linear(A, b)` | Solve linear system Ax = b |

### Visualization

| Function | Description |
|----------|-------------|
| `plot(f(x), x, start, end)` | Create 2D function plot |
| `plot_surface(f(x,y), x, y, x_start, x_end, y_start, y_end)` | Create 3D surface plot |

---

## Math Functions

### 📐 Trigonometric Functions

| Function | Description |
|----------|-------------|
| `sin(x)` | Sine of angle x |
| `cos(x)` | Cosine of angle x |
| `tan(x)` | Tangent of angle x |
| `arcsin(x)` | Inverse sine (arcsine) |
| `arccos(x)` | Inverse cosine (arccosine) |
| `arctan(x)` | Inverse tangent (arctangent) |

### Exponential & Logarithmic Functions

| Function | Description |
|----------|-------------|
| `exp(x)` | Exponential (e^x) |
| `log(x)` or `ln(x)` | Natural logarithm |
| `sqrt(x)` | Square root |
| `abs(x)` | Absolute value |
| `pow(x, y)` | Power (x^y) |

---

## Symbolic Functions

### Calculus & Algebra

| Function | Description |
|----------|-------------|
| `integrate(f(x), x)` | Perform symbolic integration |
| `diff(f(x), x)` | Perform symbolic differentiation |
| `limit(f(x), x, point)` | Calculate limit at a point |
| `solve(equation, variable)` | Solve algebraic equations |
| `summation(expr, (var, start, end))` | Compute series summation |
| `simplify(expr)` | Simplify mathematical expressions |
| `factor(expr)` | Factor algebraic expressions |

---

## Quick Examples

```mathscript
// Matrix operations
A = identity(3)
B = zeroes(2, 3)
det_A = det(A)

// Calculus
f(x) = x^2 + 3x + 2
derivative = diff(f(x), x)
integral = integrate(f(x), x)

// Visualization
plot(sin(x), x, 0, 2π)
```

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

