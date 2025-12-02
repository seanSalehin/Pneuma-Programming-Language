=======================================
     PNEUMA PROGRAMMING LANGUAGE
          by Sean Salehin
=======================================

ABOUT PNEUMA:
------------------------------------------------
Pneuma is a JIT-compiled programming language designed for clarity, speed, and ease of use. The language features a clean syntax inspired by modern paradigms, making it ideal for both learning and practical development. Pneuma's entry point is the main function, and it supports a wide range of programming constructs including functions, loops, conditionals, and file imports.

FEATURES:
------------------------------------------------
• Functions with typed arguments, return values, function calls, and parameters
• Comparison operations and boolean logic
• Loops (while, scan/for), break, and continue
• Import/load files using .pn extension
• String and variable handling with type annotations
• JIT-style execution for optimal performance
• printf with formatting
• Prefix and postfix operators
• Support for negative numbers
• do/while loops

INSTALLATION & USAGE:
------------------------------------------------
1. Create a new folder for your project (e.g., Pneuma).
2. Open the folder in your IDE or your code editor.
3. Install Python 3.7+ and Anaconda (or Miniconda) if not already installed.
4. Open your terminal (or Anaconda Prompt) inside the project folder.
5. Create and activate a dedicated Conda environment:
     conda create --name Pneuma python=3.12
     conda install llvmlite
     conda activate Pneuma
6. Clone the Repository: git clone https://github.com/seanSalehin/Pneuma-Programming-Language.git
7. Place all your .pn files in the Test folder.
8. Edit main.pn to write your program.
9. To run, execute (from the root folder): python main.py

SYNTAX EXAMPLES:
--------------------------------------------
Check Tutorials.txt in the Test folder for guided lessons and examples to learn Pneuma's syntax.

IMPORTING FILES:
------------------------------------------------
All additional files must be in the Test folder and have the .pn extension.
Example: load "filename.pn";

VERSION:
--------------------------------------------
This is Pneuma version 2.8.1
============================================