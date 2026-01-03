from flask import Flask, render_template, request, jsonify
import subprocess

app = Flask(__name__)

# This is the page the user sees
@app.route('/')
def index():
    # We will need an 'index.html' file in a 'templates' folder
    return render_template('index.html')

# This is the endpoint that runs your Python script
@app.route('/run-script', methods=['POST'])
def run_script():
    # Define the command to run your script
    # Replace 'my_script.py' with the actual path/name of your script
    try:
        # Use subprocess to execute the script and capture the output
        result = subprocess.run(
            ['python3', 'my_script.py'],
            capture_output=True,
            text=True,
            check=True # Raise an exception for non-zero exit codes
        )
        output = f"Script Output:\n{result.stdout}"
        
    except subprocess.CalledProcessError as e:
        output = f"Error running script:\n{e.stderr}"
        
    except FileNotFoundError:
        output = "Error: Python interpreter or script not found."
        
    # Return the result as a JSON response to be used by the frontend
    return jsonify({'result': output})

if __name__ == '__main__':
    # Flask's built-in server is perfect for development/low-traffic Pi use
    app.run(host='10.42.0.1', port=8080, debug=True)
