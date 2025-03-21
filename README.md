# IFC_Chatbot

# IFC Chatbot with Dynamic Code Generation Documentation

## Overview

This script is designed to analyze IFC (Industry Foundation Classes) files using natural language queries. It leverages Google's Generative AI (Gemini) to dynamically generate, validate, and execute Python code based on user input. The generated code uses the `ifcopenshell` library to interact with IFC files and ensures that the pre-loaded `ifc_file` variable is used correctly.

## Key Features

- **Dynamic Code Generation**: Uses Google's Generative AI to generate Python code based on natural language queries.
- **IFC File Analysis**: Analyzes IFC files using the `ifcopenshell` library.
- **Safe Execution**: Executes generated code in a controlled environment to prevent unauthorized actions.
- **Error Handling**: Includes robust error handling and retry mechanisms for code generation and execution.

## Prerequisites

- Python 3.x
- `ifcopenshell` library
- Google Generative AI API key

## Installation

1. **Install Python**: Ensure Python 3.x is installed on your system.
2. **Install Required Libraries**:
   ```bash
   pip install ifcopenshell google-generativeai
   ```
