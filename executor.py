import subprocess
import tempfile
import os

def execute_python_code(code: str) -> dict:
    print(f"Starting execution of code: {code[:50]}...")  # Log the start and truncate long code
    
    # Create a temporary file to store the code
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as temp_file:
        temp_file.write(code)
        temp_file_path = temp_file.name
        print(f"Created temp file: {temp_file_path}")  # Log the temp file path

    try:
        # Execute the code and capture both stdout and stderr
        print("Running the Python script...")
        result = subprocess.run(
            ['python', temp_file_path],
            capture_output=True,
            text=True,
            timeout=10  # Add timeout to prevent infinite loops
        )
        
        print(f"Execution finished with return code: {result.returncode}")
        return {
            'success': result.returncode == 0,
            'output': result.stdout,
            'error': result.stderr if result.stderr else None
        }
    except subprocess.TimeoutExpired as e:
        print("Execution timed out!")
        return {
            'success': False,
            'output': e.stdout,
            'error': 'Execution timed out after 10 seconds'
        }
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return {
            'success': False,
            'output': '',
            'error': str(e)
        }
    finally:
        # Clean up the temporary file
        if os.path.exists(temp_file_path):
            print(f"Cleaning up temp file: {temp_file_path}")
            os.remove(temp_file_path)