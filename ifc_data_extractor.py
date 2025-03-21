"""
IFC Chatbot with Dynamic Code Generation
This script uses ifcopenshell and Google's Generative AI to analyze IFC files based on natural language queries.
It generates, validates, and executes Python code dynamically to answer user questions.
The generated code uses the pre-loaded ifc_file variable and ensures the function is called correctly.
"""

import ifcopenshell
import google.generativeai as genai
import traceback

# Configuration
GENAI_API_KEY = "AIzaSyBLuL_Nw20rrNOkKo07gNERvwfXV87Kz0Y"  # Replace with your Gemini API key
MODEL_NAME = "gemini-1.5-pro-latest"  # Use a supported model name
MAX_RETRIES = 3  # Maximum code correction attempts
RETRY_DELAY = 5  # Delay in seconds between retries for quota issues


query_helper1= " my file path is :- "
query_helper2 = " please include this in the example usage. Dont comment the example usage"

# Initialize Gemini model
genai.configure(api_key=GENAI_API_KEY)
model = genai.GenerativeModel(MODEL_NAME)

def generate_code(prompt: str) -> str:
    """Generate Python code using Gemini"""
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating code: {str(e)}"

def execute_code(code: str, ifc_file) -> str:
    """Execute the generated code in a safe environment"""
    try:
        # Create isolated namespace with allowed variables
        exec_namespace = {
            'ifc_file': ifc_file,
            'ifcopenshell': ifcopenshell,
            'result': None
        }
        
        # Execute the code
        exec(code, exec_namespace)
        return str(exec_namespace.get('result', 'No result returned'))
        
    except Exception as e:
        error_trace = traceback.format_exc()
        print(f"Execution failed with error:\n{error_trace}")
        return error_trace

def process_ifc_file(ifc_file_path, query):
    """Process the IFC file based on the user query"""
    try:
        # Load the IFC file
        ifc_file = ifcopenshell.open(ifc_file_path)
        
        # Generate Python code using Gemini
        prompt = f"""
        You are an IFC expert Python developer. Generate code to analyze an IFC file using ifcopenshell.
        Follow these strict rules:
        1. Only use ifcopenshell and standard libraries
        2. Use the pre-loaded 'ifc_file' variable (do not open the file again)
        3. Store results in a variable named 'result'
        4. Never modify the original IFC file
        5. Handle potential errors
        6. Return plain text without markdown or placeholders
        7. Ensure the code is complete and executable
        
        Query: {query}
        """
        
        # Generate and execute code
        for attempt in range(MAX_RETRIES + 1):
            try:
                # Generate code
                code = generate_code(prompt)
                if code.startswith("Error"):
                    print(f"Attempt {attempt + 1}: {code}")
                    continue
                
                # Remove markdown code blocks (python ... )
                code = code.replace("python", "").replace("", "").strip()
                
                # Ensure the code uses the pre-loaded 'ifc_file' variable
                if "ifcopenshell.open(" in code:
                    code = code.replace("ifcopenshell.open(", "# ifcopenshell.open(")
                
                # Ensure the code assigns the result to a variable
                if "result =" not in code:
                    code += "\nresult = 'No result returned'"
                
                print(f"\nGenerated Code (Attempt {attempt + 1}):\n{code}")
                
                # Execute the code
                result = execute_code(code, ifc_file)
                if "Error" not in result and "Traceback" not in result:
                    return result  # Return the final result
                else:
                    print(f"Attempt {attempt + 1}: Code execution failed.")
                
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                if attempt < MAX_RETRIES:
                    print(f"Retrying in {RETRY_DELAY} seconds...")
                    time.sleep(RETRY_DELAY)
                else:
                    return f"Failed after {MAX_RETRIES} attempts. Final error: {e}"
                    
    except Exception as e:
        print(f"Error processing IFC file: {e}")
        traceback.print_exc()
        return f"Error: {e}"

def main():
    """Main function to interact with the user"""
    # Process user input
    ifc_file_path = input("Enter IFC file path: ")
    query = input("Your query: ")
    query = query + query_helper1 + ifc_file_path + query_helper2
    print(query)
    print("\nProcessing...")
    result = process_ifc_file(ifc_file_path, query)
    print("\n" + "-"*50 + "\n" + str(result))

if __name__ == "__main__":
    main()