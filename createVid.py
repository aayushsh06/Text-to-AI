import subprocess
import time


scripts = ['TTS.py', 'makeCaption.py', 'combine.py']


for script in scripts:
    try:
        print(f"Executing {script}...")
        subprocess.run(['python3', script], check=True)
        print(f"{script} executed successfully.")
        time.sleep(2)  
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while executing {script}: {e}")
        break
