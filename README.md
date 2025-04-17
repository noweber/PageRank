# PageRank Algorithm in Python

This repository contains a Python implementation of the **PageRank** algorithm, used to rank web pages based on their structural importance within a corpus of hyperlinks. It provides both:
- A **sampling-based approximation** using a random surfer model
- An **iterative solution** that refines ranks until convergence

The implementation is fully self-contained and operates on a directory of `.html` files as a simulated web corpus.

---

## ⚙️ Technologies Used

- **Python 3**
- Built-in libraries: `os`, `sys`, `re`, `random`
- No external dependencies

---

## 🧠 How It Works

### Input
The input is a directory containing `.html` files. Each file may contain `<a href="...">` links to other files in the corpus.

### Output
The script prints the estimated PageRank of each page using:
1. **Sampling Method** — Based on the random surfer model with a specified number of steps
2. **Iterative Method** — Based on repeated application of the PageRank formula until convergence

---

## 🔁 Methods Implemented

### `crawl(directory)`
Parses `.html` files and builds a mapping of pages to the links they contain.

### `transition_model(corpus, page, damping_factor)`
Constructs a probability distribution over the next page based on the damping factor.

### `sample_pagerank(corpus, damping_factor, n)`
Estimates PageRank via sampling with `n` iterations starting from a random page.

### `iterate_pagerank(corpus, damping_factor)`
Computes PageRank by repeatedly updating values until they converge below a fixed threshold.

---

## 🚀 How to Run

Make sure you have a directory of `.html` files ready. Then run:

```bash
python pagerank.py path/to/corpus
