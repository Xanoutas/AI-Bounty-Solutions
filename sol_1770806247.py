import os
import re

def find_solidity_files(directory):
    """Find all Solidity files in a given directory."""
    sol_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.sol'):
                sol_files.append(os.path.join(root, file))
    return sol_files

def remove_comments_and_strings(source_code):
    """Remove comments and string literals from the source code to prevent false positives."""
    # This regex removes single-line and multi-line comments
    clean_code = re.sub(r'//.*?$|/\*.*?\*/', '', source_code, flags=re.DOTALL | re.MULTILINE)
    # This regex removes string literals, ensuring escaped quotes are handled
    clean_code = re.sub(r'".*?(?<!\\)"|\'.*?(?<!\\)\'', '', clean_code, flags=re.DOTALL | re.MULTILINE)
    return clean_code

def check_for_reentrancy(filename):
    """Check a Solidity file for potential reentrancy vulnerabilities."""
    reentrancy_patterns = [
        r'\b(call|send|transfer)\b\s*\(',  # External call patterns
    ]
    warnings = []
    with open(filename, 'r', encoding='utf-8') as file:
        source_code = file.read()
        source_code_clean = remove_comments_and_strings(source_code)
        for pattern in reentrancy_patterns:
            matches = re.finditer(pattern, source_code_clean)
            for match in matches:
                call_position = match.start()
                subsequent_code = source_code_clean[call_position:]
                state_modifications = re.search(r'\b\w+\s*=(?!=)', subsequent_code)  # Look for state modifications
                if state_modifications and not re.search(r'\brequire\s*\(', source_code_clean[:call_position]):
                    warnings.append(f"Potential reentrancy vulnerability at byte {match.start()} in {filename}")
    return warnings

def main(directory):
    """Main function to scan Solidity files for reentrancy vulnerabilities."""
    sol_files = find_solidity_files(directory)
    vulnerabilities = []
    for sol_file in sol_files:
        vulnerabilities.extend(check_for_reentrancy(sol_file))
    if vulnerabilities:
        for warning in vulnerabilities:
            print(warning)
    else:
        print("No reentrancy vulnerabilities found.")

# Example usage
if __name__ == "__main__":
    DIRECTORY_TO_SCAN = './contracts'  # Define the directory containing Solidity files
    main(DIRECTORY_TO_SCAN)