# Assembly File Processing Project Using Python

## Description

This project is designed to process and convert Assembly (ASM) files using Python. The project includes a script that reads an ASM file, processes it, and saves the result in a specified folder.

## Requirements

- Python 3.x
- Required Python libraries (if any are specified in the scripts, such as `os` or others)

## How to Use

### 1. Setting Up the Environment

1. Make sure Python is installed on your machine. You can download Python from the [official website](https://www.python.org/downloads/).
2. Download all the project files to your local machine.
3. Ensure that you have a `testFiles` folder that contains your `.asm` files.

### 2. Running the Script

To run the project scripts, follow these steps:

1. Open Command Prompt (Windows) or Terminal (Mac/Linux).
2. Run the batch script by typing the following command:
   ```bash
   pass1.bat
   pass2.bat
   ```

The script will do the following:

- If the `output_folder` does not exist, it will be created automatically.
- It will then execute the `pass1.py` script to process the `test1.asm` or `test2.asm` file from the `testFiles` folder, saving the result as `intermediateFile1.txt` or `intermediateFile2.txt` in the `output_folder`.

### 3. Output

The result will be found in the `output_folder`, where the `intermediateFile1.txt` or `intermediateFile2.txt` file will be created with the processed data.

## Folders and Files

- `testFiles/`: Contains the ASM files for testing.
- `output_folder/`: Stores the resulting files.
- `pass1.py`: Python script that processes and converts ASM files.
- `test1.bat` or `test2.bat`: Batch script that sets up and runs the processing.
