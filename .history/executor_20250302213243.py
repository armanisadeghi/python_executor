import subprocess
import tempfile
import os

def execute_python_code(code: str) -> dict:
    # Create a temporary file to store the code
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as temp_file:
        temp_file.write(code)
        temp_file_path = temp_file.name

    try:
        # Execute the code and capture both stdout and stderr
        result = subprocess.run(
            ['python', temp_file_path],
            capture_output=True,
            text=True,
            timeout=10  # Add timeout to prevent infinite loops
        )
        
        return {
            'success': result.returncode == 0,
            'output': result.stdout,
            'error': result.stderr if result.stderr else None
        }
    except subprocess.TimeoutExpired as e:
        return {
            'success': False,
            'output': e.stdout,
            'error': 'Execution timed out after 10 seconds'
        }
    except Exception as e:
        return {
            'success': False,
            'output': '',
            'error': str(e)
        }
    finally:
        # Clean up the temporary file
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)