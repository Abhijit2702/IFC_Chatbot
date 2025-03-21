# import ifcopenshell
# import google.generativeai as genai
# import traceback  # Added missing import
# import time

# # Initialize with valid API key
# genai.configure(api_key="AIzaSyCPtJbenBsU08rfQ0zqi3STX6nH1bwtfGw")

# # Verify available models
# try:
#     print("Available models:")
#     valid_models = [
#         m.name for m in genai.list_models() 
#         if 'generateContent' in m.supported_generation_methods
#     ]
#     print("\n".join(valid_models))
    
#     # Use verified model name
#     model = genai.GenerativeModel('gemini-pro')  # Correct public model name

# except Exception as config_error:
#     print(f"Configuration error: {config_error}")
#     exit()

# def process_ifc_file(ifc_file_path, query):
#     try:
#         ifc_file = ifcopenshell.open(ifc_file_path)
        
       
            
#         # For other queries
#         prompt = f"""Create Python code using ifcopenshell to:
#         - Take 'ifc_file' as input
#         - Answer: {query}
#         - Return direct numerical result"""
        
#         try:
#             response = model.generate_content(prompt)
#             code = response.text
            
#             # Clean generated code
#             code = code.replace("ifcopenshell.open(", "# ").replace("ifc_file_path", "# ")
#             print("Generated code:\n", code)
            
#             # Execute in isolated namespace
#             exec_globals = {}
#             exec(code, exec_globals)
#             result = exec_globals['get_answer'](ifc_file)
#             print("Result:", result)
            
#         except genai.Error as api_error:
#             print(f"API Error: {api_error}")
#             print("Falling back to direct IFC processing...")
#             # Add simple fallback processing here

#     except Exception as e:
#         print(f"Error: {str(e)}")
#         traceback.print_exc()

# def main():
#     try:
#         process_ifc_file(
#             input("Enter IFC file path: "),
#             input("Your query: ")
#         )
#     except Exception as e:
#         print(f"Application error: {e}")
#         traceback.print_exc()

# if __name__ == "__main__":
#     main()


#-------------------------------------------------------
# """
# IFC Chatbot with Auto-Correction
# This script uses ifcopenshell and Google's Generative AI to analyze IFC files based on natural language queries.
# It automatically generates, executes, and iteratively improves Python code to answer user questions.
# """

# import ifcopenshell
# import google.generativeai as genai
# import traceback
# import time

# # Configuration
# GENAI_API_KEY = "AIzaSyCPtJbenBsU08rfQ0zqi3STX6nH1bwtfGw"  # Replace with your Gemini API key
# MODEL_NAME = "gemini-1.5-pro-latest"  # Use a supported model name
# MAX_RETRIES = 10  # Maximum code correction attempts
# RETRY_DELAY = 5  # Delay in seconds between retries for quota issues

# # Initialize Gemini model
# genai.configure(api_key=GENAI_API_KEY)

# def get_supported_models():
#     """List all supported models for generateContent"""
#     try:
#         print("Available models:")
#         valid_models = [
#             m.name for m in genai.list_models() 
#             if 'generateContent' in m.supported_generation_methods
#         ]
#         print("\n".join(valid_models))
#         return valid_models
#     except Exception as e:
#         print(f"Error listing models: {e}")
#         return []

# def process_ifc_file(ifc_file_path, query):
#     """Process the IFC file based on the user query"""
#     try:
#         # Load the IFC file
#         ifc_file = ifcopenshell.open(ifc_file_path)
        
#         # Generate Python code using Gemini
#         prompt = f"""
#         You are an IFC expert Python developer. Generate code to analyze an IFC file using ifcopenshell.
#         Follow these rules:
#         1. Only use ifcopenshell and standard libraries
#         2. Store results in a 'result' variable
#         3. Never modify the original IFC file
#         4. Handle potential errors
#         5. Return plain text without markdown
        
#         Query: {query}
#         """
        
#         # Initialize the model
#         model = genai.GenerativeModel(MODEL_NAME)
        
#         # Generate and execute code
#         for attempt in range(MAX_RETRIES + 1):
#             try:
#                 response = model.generate_content(prompt)
#                 code = response.text
                
#                 # Clean generated code
#                 code = code.replace("ifcopenshell.open(", "# ").replace("ifc_file_path", "# ")
#                 print(f"\nGenerated Code (Attempt {attempt + 1}):\n{code}")
                
#                 # Execute in isolated namespace
#                 exec_namespace = {
#                     'ifc_file': ifc_file,
#                     'ifcopenshell': ifcopenshell,
#                     'result': None
#                 }
#                 exec(code, exec_namespace)
                
#                 # Return the result
#                 result = exec_namespace.get('result', 'No result returned')
#                 print(f"Result: {result}")
#                 return result
                
#             except Exception as e:
#                 print(f"Attempt {attempt + 1} failed: {e}")
#                 if attempt < MAX_RETRIES:
#                     print(f"Retrying in {RETRY_DELAY} seconds...")
#                     time.sleep(RETRY_DELAY)
#                 else:
#                     print("Max retries reached. Exiting.")
#                     return f"Failed after {MAX_RETRIES} attempts. Final error: {e}"
                    
#     except Exception as e:
#         print(f"Error processing IFC file: {e}")
#         traceback.print_exc()
#         return f"Error: {e}"

# def main():
#     """Main function to interact with the user"""
#     # List supported models
#     supported_models = get_supported_models()
#     if not supported_models:
#         print("No supported models found. Exiting.")
#         return
    
#     # Process user input
#     ifc_file_path = input("Enter IFC file path: ")
#     query = input("Your query: ")
    
#     print("\nProcessing...")
#     result = process_ifc_file(ifc_file_path, query)
#     print("\n" + "-"*50 + "\n" + str(result))

# if __name__ == "__main__":
#     main()
#----------------------------------------------------------

# """
# IFC Chatbot with Dynamic Code Generation
# This script uses ifcopenshell and Google's Generative AI to analyze IFC files based on natural language queries.
# It generates, validates, and executes Python code dynamically to answer user questions.
# """

# import ifcopenshell
# import google.generativeai as genai
# import traceback
# import re

# # Configuration
# GENAI_API_KEY = "AIzaSyCPtJbenBsU08rfQ0zqi3STX6nH1bwtfGw"  # Replace with your Gemini API key
# MODEL_NAME = "gemini-1.5-pro-latest"  # Use a supported model name
# MAX_RETRIES = 3  # Maximum code correction attempts
# RETRY_DELAY = 5  # Delay in seconds between retries for quota issues

# # Initialize Gemini model
# genai.configure(api_key=GENAI_API_KEY)
# model = genai.GenerativeModel(MODEL_NAME)

# def validate_code(code: str) -> bool:
#     """Validate the generated code for syntax errors and unsafe patterns"""
#     # Check for invalid placeholders
#     if "#" in code or "..." in code:
#         return False
    
#     # Check for unsafe patterns
#     unsafe_patterns = [
#         r"os\.system", r"subprocess", r"__import__", r"open\(",
#         r"delete", r"write", r"shutil", r"rmdir", r"remove"
#     ]
#     if any(re.search(pattern, code) for pattern in unsafe_patterns):
#         return False
    
#     return True

# def fix_generated_code(code: str) -> str:
#     """Fix common issues in the generated code"""
#     # Remove markdown code blocks (```python ... ```)
#     code = re.sub(r"```python|```", "", code).strip()
    
#     # Ensure the code assigns the result to a variable
#     if "result =" not in code:
#         code += "\nresult = 'No result returned'"
    
#     return code

# def execute_code(code: str, ifc_file) -> str:
#     """Execute the generated code in a safe environment"""
#     try:
#         # Create isolated namespace with allowed variables
#         exec_namespace = {
#             'ifc_file': ifc_file,
#             'ifcopenshell': ifcopenshell,
#             'result': None
#         }
        
#         exec(code, exec_namespace)
#         return str(exec_namespace.get('result', 'No result returned'))
        
#     except Exception as e:
#         error_trace = traceback.format_exc()
#         print(f"Execution failed: {error_trace}")
#         return error_trace

# def generate_code(prompt: str) -> str:
#     """Generate Python code using Gemini"""
#     try:
#         response = model.generate_content(prompt)
#         return response.text
#     except Exception as e:
#         return f"Error generating code: {str(e)}"

# def process_ifc_file(ifc_file_path, query):
#     """Process the IFC file based on the user query"""
#     try:
#         # Load the IFC file
#         ifc_file = ifcopenshell.open(ifc_file_path)
        
#         # Generate Python code using Gemini
#         prompt = f"""
#         You are an IFC expert Python developer. Generate code to analyze an IFC file using ifcopenshell.
#         Follow these rules:
#         1. Only use ifcopenshell and standard libraries
#         2. Store results in a 'result' variable
#         3. Never modify the original IFC file
#         4. Handle potential errors
#         5. Return plain text without markdown
        
#         Query: {query}
#         """
        
#         # Generate and execute code
#         for attempt in range(MAX_RETRIES + 1):
#             try:
#                 code = generate_code(prompt)
#                 if code.startswith("Error"):
#                     print(f"Attempt {attempt + 1}: {code}")
#                     continue
                
#                 # Fix common issues in the generated code
#                 code = fix_generated_code(code)
#                 print(f"print {code}")
#                 # Validate the code
#                 if not validate_code(code):
#                     print(f"Attempt {attempt + 1}: Invalid code generated.")
#                     continue
                
#                 print(f"\nGenerated Code (Attempt {attempt + 1}):\n{code}")
                
#                 # Execute the code
#                 result = execute_code(code, ifc_file)
#                 if "Error" not in result and "Traceback" not in result:
#                     print(f"Result: {result}")
#                     return result
                
#             except Exception as e:
#                 print(f"Attempt {attempt + 1} failed: {e}")
#                 if attempt < MAX_RETRIES:
#                     print(f"Retrying in {RETRY_DELAY} seconds...")
#                     time.sleep(RETRY_DELAY)
#                 else:
#                     print("Max retries reached. Exiting.")
#                     return f"Failed after {MAX_RETRIES} attempts. Final error: {e}"
                    
#     except Exception as e:
#         print(f"Error processing IFC file: {e}")
#         traceback.print_exc()
#         return f"Error: {e}"

# def main():
#     """Main function to interact with the user"""
#     # Process user input
#     ifc_file_path = input("Enter IFC file path: ")
#     query = input("Your query: ")
    
#     print("\nProcessing...")
#     result = process_ifc_file(ifc_file_path, query)
#     print("\n" + "-"*50 + "\n" + str(result))

# if __name__ == "__main__":
#     main()

#---------------------------------------------------
# """
# IFC Chatbot with Dynamic Code Generation and Error Display
# This script uses ifcopenshell and Google's Generative AI to analyze IFC files based on natural language queries.
# It generates, validates, and executes Python code dynamically to answer user questions.
# If the code fails, it displays the error before marking it as invalid.
# """

# import ifcopenshell
# import google.generativeai as genai
# import traceback
# import re

# # Configuration
# GENAI_API_KEY = "AIzaSyCPtJbenBsU08rfQ0zqi3STX6nH1bwtfGw"  # Replace with your Gemini API key
# MODEL_NAME = "gemini-1.5-pro-latest"  # Use a supported model name
# MAX_RETRIES = 3  # Maximum code correction attempts
# RETRY_DELAY = 5  # Delay in seconds between retries for quota issues

# # Initialize Gemini model
# genai.configure(api_key=GENAI_API_KEY)
# model = genai.GenerativeModel(MODEL_NAME)

# def validate_code(code: str) -> bool:
#     """Validate the generated code for syntax errors and unsafe patterns"""
#     # Check for invalid placeholders
#     if "#" in code or "..." in code:
#         print("Invalid code: Placeholders detected.")
#         return False
    
#     # Check for unsafe patterns
#     unsafe_patterns = [
#         r"os\.system", r"subprocess", r"__import__", r"open\(",
#         r"delete", r"write", r"shutil", r"rmdir", r"remove"
#     ]
#     if any(re.search(pattern, code) for pattern in unsafe_patterns):
#         print("Invalid code: Unsafe patterns detected.")
#         return False
    
#     return True

# def fix_generated_code(code: str) -> str:
#     """Fix common issues in the generated code"""
#     # Remove markdown code blocks (```python ... ```)
#     code = re.sub(r"```python|```", "", code).strip()
    
#     # Ensure the code assigns the result to a variable
#     if "result =" not in code:
#         code += "\nresult = 'No result returned'"
    
#     return code

# def execute_code(code: str, ifc_file) -> str:
#     """Execute the generated code in a safe environment"""
#     try:
#         # Create isolated namespace with allowed variables
#         exec_namespace = {
#             'ifc_file': ifc_file,
#             'ifcopenshell': ifcopenshell,
#             'result': None
#         }
        
#         exec(code, exec_namespace)
#         return str(exec_namespace.get('result', 'No result returned'))
        
#     except Exception as e:
#         error_trace = traceback.format_exc()
#         print(f"Execution failed with error:\n{error_trace}")
#         return error_trace

# def generate_code(prompt: str) -> str:
#     """Generate Python code using Gemini"""
#     try:
#         response = model.generate_content(prompt)
#         return response.text
#     except Exception as e:
#         return f"Error generating code: {str(e)}"

# def process_ifc_file(ifc_file_path, query):
#     """Process the IFC file based on the user query"""
#     try:
#         # Load the IFC file
#         ifc_file = ifcopenshell.open(ifc_file_path)
        
#         # Generate Python code using Gemini
#         prompt = f"""
#         You are an IFC expert Python developer. Generate code to analyze an IFC file using ifcopenshell.
#         Follow these rules:
#         1. Only use ifcopenshell and standard libraries
#         2. Store results in a 'result' variable
#         3. Never modify the original IFC file
#         4. Handle potential errors
#         5. Return plain text without markdown
        
#         Query: {query}
#         """
        
#         # Generate and execute code
#         for attempt in range(MAX_RETRIES + 1):
#             try:
#                 code = generate_code(prompt)
#                 if code.startswith("Error"):
#                     print(f"Attempt {attempt + 1}: {code}")
#                     continue
                
#                 # Fix common issues in the generated code
#                 code = fix_generated_code(code)
                
#                 # Validate the code
#                 if not validate_code(code):
#                     print(f"Attempt {attempt + 1}: Invalid code generated.")
#                     continue
                
#                 print(f"\nGenerated Code (Attempt {attempt + 1}):\n{code}")
                
#                 # Execute the code
#                 result = execute_code(code, ifc_file)
#                 if "Error" not in result and "Traceback" not in result:
#                     print(f"Result: {result}")
#                     return result
#                 else:
#                     print(f"Attempt {attempt + 1}: Code execution failed.")
                
#             except Exception as e:
#                 print(f"Attempt {attempt + 1} failed: {e}")
#                 if attempt < MAX_RETRIES:
#                     print(f"Retrying in {RETRY_DELAY} seconds...")
#                     time.sleep(RETRY_DELAY)
#                 else:
#                     print("Max retries reached. Exiting.")
#                     return f"Failed after {MAX_RETRIES} attempts. Final error: {e}"
                    
#     except Exception as e:
#         print(f"Error processing IFC file: {e}")
#         traceback.print_exc()
#         return f"Error: {e}"

# def main():
#     """Main function to interact with the user"""
#     # Process user input
#     ifc_file_path = input("Enter IFC file path: ")
#     query = input("Your query: ")
    
#     print("\nProcessing...")
#     result = process_ifc_file(ifc_file_path, query)
#     print("\n" + "-"*50 + "\n" + str(result))

# if __name__ == "__main__":
#     main()

#---------------------------------------------------------

# """
# IFC Chatbot with Dynamic Code Generation
# This script uses ifcopenshell and Google's Generative AI to analyze IFC files based on natural language queries.
# It generates, validates, and executes Python code dynamically to answer user questions.
# The generated code is guaranteed to be valid and executable.
# """

# import ifcopenshell
# import google.generativeai as genai
# import traceback

# # Configuration
# GENAI_API_KEY = "AIzaSyCPtJbenBsU08rfQ0zqi3STX6nH1bwtfGw"  # Replace with your Gemini API key
# MODEL_NAME = "gemini-1.5-pro-latest"  # Use a supported model name
# MAX_RETRIES = 3  # Maximum code correction attempts
# RETRY_DELAY = 5  # Delay in seconds between retries for quota issues

# # Initialize Gemini model
# genai.configure(api_key=GENAI_API_KEY)
# model = genai.GenerativeModel(MODEL_NAME)

# def generate_code(prompt: str) -> str:
#     """Generate Python code using Gemini"""
#     try:
#         response = model.generate_content(prompt)
#         return response.text
#     except Exception as e:
#         return f"Error generating code: {str(e)}"

# def execute_code(code: str, ifc_file) -> str:
#     """Execute the generated code in a safe environment"""
#     try:
#         # Create isolated namespace with allowed variables
#         exec_namespace = {
#             'ifc_file': ifc_file,
#             'ifcopenshell': ifcopenshell,
#             'result': None
#         }
        
#         # Execute the code
#         exec(code, exec_namespace)
#         return str(exec_namespace.get('result', 'No result returned'))
        
#     except Exception as e:
#         error_trace = traceback.format_exc()
#         print(f"Execution failed with error:\n{error_trace}")
#         return error_trace

# def process_ifc_file(ifc_file_path, query):
#     """Process the IFC file based on the user query"""
#     try:
#         # Load the IFC file
#         ifc_file = ifcopenshell.open(ifc_file_path)
        
#         # Generate Python code using Gemini
#         prompt = f"""
#         You are an IFC expert Python developer. Generate code to analyze an IFC file using ifcopenshell.
#         Follow these strict rules:
#         1. Only use ifcopenshell and standard libraries
#         2. Store results in a variable named 'result'
#         3. Never modify the original IFC file
#         4. Handle potential errors
#         5. Return plain text without markdown or placeholders
#         6. Ensure the code is complete and executable
        
#         Query: {query}
#         """
        
#         # Generate and execute code
#         for attempt in range(MAX_RETRIES + 1):
#             try:
#                 # Generate code
#                 code = generate_code(prompt)
#                 if code.startswith("Error"):
#                     print(f"Attempt {attempt + 1}: {code}")
#                     continue
                
#                 # Remove markdown code blocks (```python ... ```)
#                 code = code.replace("```python", "").replace("```", "").strip()
                
#                 # Ensure the code assigns the result to a variable
#                 if "result =" not in code:
#                     code += "\nresult = 'No result returned'"
                
#                 print(f"\nGenerated Code (Attempt {attempt + 1}):\n{code}")
                
#                 # Execute the code
#                 result = execute_code(code, ifc_file)
#                 if "Error" not in result and "Traceback" not in result:
#                     return result  # Return the final result
#                 else:
#                     print(f"Attempt {attempt + 1}: Code execution failed.")
                
#             except Exception as e:
#                 print(f"Attempt {attempt + 1} failed: {e}")
#                 if attempt < MAX_RETRIES:
#                     print(f"Retrying in {RETRY_DELAY} seconds...")
#                     time.sleep(RETRY_DELAY)
#                 else:
#                     return f"Failed after {MAX_RETRIES} attempts. Final error: {e}"
                    
#     except Exception as e:
#         print(f"Error processing IFC file: {e}")
#         traceback.print_exc()
#         return f"Error: {e}"

# def main():
#     """Main function to interact with the user"""
#     # Process user input
#     ifc_file_path = input("Enter IFC file path: ")
#     query = input("Your query: ")
    
#     print("\nProcessing...")
#     result = process_ifc_file(ifc_file_path, query)
#     print("\n" + "-"*50 + "\n" + str(result))

# if __name__ == "__main__":
#     main()

#-----------------------------------------------------

# """
# IFC Chatbot with Dynamic Code Generation
# This script uses ifcopenshell and Google's Generative AI to analyze IFC files based on natural language queries.
# It generates, validates, and executes Python code dynamically to answer user questions.
# The generated code uses the pre-loaded `ifc_file` variable to avoid file path issues.
# """

# import ifcopenshell
# import google.generativeai as genai
# import traceback

# # Configuration
# GENAI_API_KEY = "AIzaSyCPtJbenBsU08rfQ0zqi3STX6nH1bwtfGw"  # Replace with your Gemini API key
# MODEL_NAME = "gemini-1.5-pro-latest"  # Use a supported model name
# MAX_RETRIES = 3  # Maximum code correction attempts
# RETRY_DELAY = 5  # Delay in seconds between retries for quota issues

# # Initialize Gemini model
# genai.configure(api_key=GENAI_API_KEY)
# model = genai.GenerativeModel(MODEL_NAME)

# def generate_code(prompt: str) -> str:
#     """Generate Python code using Gemini"""
#     try:
#         response = model.generate_content(prompt)
#         return response.text
#     except Exception as e:
#         return f"Error generating code: {str(e)}"

# def execute_code(code: str, ifc_file) -> str:
#     """Execute the generated code in a safe environment"""
#     try:
#         # Create isolated namespace with allowed variables
#         exec_namespace = {
#             'ifc_file': ifc_file,
#             'ifcopenshell': ifcopenshell,
#             'result': None
#         }
        
#         # Execute the code
#         exec(code, exec_namespace)
#         return str(exec_namespace.get('result', 'No result returned'))
        
#     except Exception as e:
#         error_trace = traceback.format_exc()
#         print(f"Execution failed with error:\n{error_trace}")
#         return error_trace

# def process_ifc_file(ifc_file_path, query):
#     """Process the IFC file based on the user query"""
#     try:
#         # Load the IFC file
#         ifc_file = ifcopenshell.open(ifc_file_path)
        
#         # Generate Python code using Gemini
#         prompt = f"""
#         You are an IFC expert Python developer. Generate code to analyze an IFC file using ifcopenshell.
#         Follow these strict rules:
#         1. Only use ifcopenshell and standard libraries
#         2. Use the pre-loaded 'ifc_file' variable (do not open the file again)
#         3. Store results in a variable named 'result'
#         4. Never modify the original IFC file
#         5. Handle potential errors
#         6. Return plain text without markdown or placeholders
#         7. Ensure the code is complete and executable
        
#         Query: {query}
#         """
        
#         # Generate and execute code
#         for attempt in range(MAX_RETRIES + 1):
#             try:
#                 # Generate code
#                 code = generate_code(prompt)
#                 if code.startswith("Error"):
#                     print(f"Attempt {attempt + 1}: {code}")
#                     continue
                
#                 # Remove markdown code blocks (```python ... ```)
#                 code = code.replace("```python", "").replace("```", "").strip()
                
#                 # Ensure the code uses the pre-loaded 'ifc_file' variable
#                 if "ifcopenshell.open(" in code:
#                     code = code.replace("ifcopenshell.open(", "# ifcopenshell.open(")
                
#                 # Ensure the code assigns the result to a variable
#                 if "result =" not in code:
#                     code += "\nresult = 'No result returned'"
                
#                 print(f"\nGenerated Code (Attempt {attempt + 1}):\n{code}")
                
#                 # Execute the code
#                 result = execute_code(code, ifc_file)
#                 if "Error" not in result and "Traceback" not in result:
#                     return result  # Return the final result
#                 else:
#                     print(f"Attempt {attempt + 1}: Code execution failed.")
                
#             except Exception as e:
#                 print(f"Attempt {attempt + 1} failed: {e}")
#                 if attempt < MAX_RETRIES:
#                     print(f"Retrying in {RETRY_DELAY} seconds...")
#                     time.sleep(RETRY_DELAY)
#                 else:
#                     return f"Failed after {MAX_RETRIES} attempts. Final error: {e}"
                    
#     except Exception as e:
#         print(f"Error processing IFC file: {e}")
#         traceback.print_exc()
#         return f"Error: {e}"

# def main():
#     """Main function to interact with the user"""
#     # Process user input
#     ifc_file_path = input("Enter IFC file path: ")
#     query = input("Your query: ")
    
#     print("\nProcessing...")
#     result = process_ifc_file(ifc_file_path, query)
#     print("\n" + "-"*50 + "\n" + str(result))

# if __name__ == "__main__":
#     main()

#------------------------------------------------------------

# """
# IFC Chatbot with Dynamic Code Generation
# This script uses ifcopenshell and Google's Generative AI to analyze IFC files based on natural language queries.
# It generates, validates, and executes Python code dynamically to answer user questions.
# The generated code uses the pre-loaded `ifc_file` variable and ensures the function is called correctly.
# """

# import ifcopenshell
# import google.generativeai as genai
# import traceback

# # Configuration
# GENAI_API_KEY = "AIzaSyCPtJbenBsU08rfQ0zqi3STX6nH1bwtfGw"  # Replace with your Gemini API key
# MODEL_NAME = "gemini-1.5-pro-latest"  # Use a supported model name
# MAX_RETRIES = 3  # Maximum code correction attempts
# RETRY_DELAY = 5  # Delay in seconds between retries for quota issues


# query_helper1= " my file path is :- "
# query_helper2 = " remove all the syntax errors.If needed make changes in helper queries or prompt but give the result"

# # Initialize Gemini model
# genai.configure(api_key=GENAI_API_KEY)
# model = genai.GenerativeModel(MODEL_NAME)

# def generate_code(prompt: str) -> str:
#     """Generate Python code using Gemini"""
#     try:
#         response = model.generate_content(prompt)
#         return response.text
#     except Exception as e:
#         return f"Error generating code: {str(e)}"

# def execute_code(code: str, ifc_file) -> str:
#     """Execute the generated code in a safe environment"""
#     try:
#         # Create isolated namespace with allowed variables
#         exec_namespace = {
#             'ifc_file': ifc_file,
#             'ifcopenshell': ifcopenshell,
#             'result': None
#         }
        
#         # Execute the code
#         exec(code, exec_namespace)
#         return str(exec_namespace.get('result', 'No result returned'))
        
#     except Exception as e:
#         error_trace = traceback.format_exc()
#         print(f"Execution failed with error:\n{error_trace}")
#         return error_trace

# def process_ifc_file(ifc_file_path, query):
#     """Process the IFC file based on the user query"""
#     try:
#         # Load the IFC file
#         ifc_file = ifcopenshell.open(ifc_file_path)
        
#         # Generate Python code using Gemini
#         prompt = f"""
#         You are an IFC expert Python developer. Generate code to analyze an IFC file using ifcopenshell.
#         Follow these strict rules:
#         1. Only use ifcopenshell and standard libraries
#         2. Use the pre-loaded 'ifc_file' variable (do not open the file again)
#         3. Store results in a variable named 'result'
#         4. Never modify the original IFC file
#         5. Handle potential errors
#         6. Return plain text without markdown or placeholders
#         7. Ensure the code is complete and executable
#         8. NEVER use ifcopenshell.open() - the file is already loaded as 'ifc_file'
#         9. Only analyze the provided 'ifc_file' variable
        
#         Query: {query}
#         """
        
#         # Generate and execute code
#         for attempt in range(MAX_RETRIES + 1):
#             try:
#                 # Generate code
#                 code = generate_code(prompt)
#                 if code.startswith("Error"):
#                     print(f"Attempt {attempt + 1}: {code}")
#                     continue
                
#                 # Remove markdown code blocks (```python ... ```)
#                 code = code.replace("```python", "").replace("```", "").strip()
                
#                 # Ensure the code uses the pre-loaded 'ifc_file' variable
#                 if "ifcopenshell.open(" in code:
#                     code = code.replace("ifcopenshell.open(", "# ifcopenshell.open(")
                
#                 # Ensure the code assigns the result to a variable
#                 if "result =" not in code:
#                     code += "\nresult = 'No result returned'"
                
#                 print(f"\nGenerated Code (Attempt {attempt + 1}):\n{code}")
                
#                 # Execute the code
#                 result = execute_code(code, ifc_file)
#                 if "Error" not in result and "Traceback" not in result:
#                     return result  # Return the final result
#                 else:
#                     print(f"Attempt {attempt + 1}: Code execution failed.")
                
#             except Exception as e:
#                 print(f"Attempt {attempt + 1} failed: {e}")
#                 if attempt < MAX_RETRIES:
#                     print(f"Retrying in {RETRY_DELAY} seconds...")
#                     time.sleep(RETRY_DELAY)
#                 else:
#                     return f"Failed after {MAX_RETRIES} attempts. Final error: {e}"
                    
#     except Exception as e:
#         print(f"Error processing IFC file: {e}")
#         traceback.print_exc()
#         return f"Error: {e}"

# def main():
#     """Main function to interact with the user"""
#     # Process user input
#     ifc_file_path = input("Enter IFC file path: ")
#     query = input("Your query: ")
#     query = query + query_helper1 + ifc_file_path + query_helper2
#     print(query)
#     print("\nProcessing...")
#     result = process_ifc_file(ifc_file_path, query)
#     print("\n" + "-"*50 + "\n" + str(result))

# if __name__ == "__main__":
#     main()

#------------------------------------------
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