#!/usr/bin/env python3
"""
Test runner with colored output
Shows file being executed and test results in colors
"""
import subprocess
import sys
import re
from pathlib import Path

# Color codes
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'
BOLD = '\033[1m'

def run_tests():
    """Run pytest and display colored output"""
    
    print(f"\n{BLUE}{'='*80}{RESET}")
    print(f"{BLUE}{BOLD}RUNNING ALL TEST CASES{RESET}")
    print(f"{BLUE}{'='*80}{RESET}\n")
    
    # Run pytest with verbose output
    cmd = [
        sys.executable, "-m", "pytest",
        "tests/authentication/",
        "-v",
        "--tb=short",
        "--color=yes"
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        output = result.stdout + result.stderr
        
        # Track current file
        current_file = None
        file_tests = {}
        current_line_output = ""
        
        # Process output line by line
        for line in output.split('\n'):
            # Check if this is a test file line
            if '::' in line and ('PASSED' in line or 'FAILED' in line or 'SKIPPED' in line):
                # Extract file name
                match = re.search(r'(test_\w+\.py)::', line)
                if match:
                    file_name = match.group(1)
                    if file_name != current_file:
                        if current_file is not None and current_line_output:
                            print(f"  {current_line_output}")
                        current_file = file_name
                        current_line_output = ""
                        if current_file not in file_tests:
                            file_tests[current_file] = {'passed': 0, 'failed': 0, 'skipped': 0}
                        print(f"\n{BLUE}{BOLD}📄 Executing: {file_name}{RESET}\n  ", end="")
                
                # Add colored dot for result
                if 'PASSED' in line:
                    file_tests[current_file]['passed'] += 1
                    current_line_output += f"{GREEN}●{RESET}"
                elif 'FAILED' in line:
                    file_tests[current_file]['failed'] += 1
                    current_line_output += f"{RED}✗{RESET}"
                elif 'SKIPPED' in line:
                    file_tests[current_file]['skipped'] += 1
                    current_line_output += f"{YELLOW}⊘{RESET}"
        
        # Print final line
        if current_line_output:
            print(f"{current_line_output}")
        
        # Print file summary
        if file_tests:
            print(f"\n{BLUE}{'='*80}{RESET}")
            print(f"{BLUE}{BOLD}TEST SUMMARY BY FILE{RESET}")
            print(f"{BLUE}{'='*80}{RESET}")
            
            total_passed = 0
            total_failed = 0
            total_skipped = 0
            
            for file_name in sorted(file_tests.keys()):
                stats = file_tests[file_name]
                total_passed += stats['passed']
                total_failed += stats['failed']
                total_skipped += stats['skipped']
                
                print(f"\n📄 {file_name}")
                if stats['passed'] > 0:
                    print(f"   {GREEN}✓ Passed:  {stats['passed']}{RESET}")
                if stats['failed'] > 0:
                    print(f"   {RED}✗ Failed:  {stats['failed']}{RESET}")
                if stats['skipped'] > 0:
                    print(f"   {YELLOW}⊘ Skipped: {stats['skipped']}{RESET}")
            
            print(f"\n{BLUE}{'='*80}{RESET}")
            
            # Print colored summary based on results
            if total_failed == 0 and total_passed > 0:
                print(f"{GREEN}{BOLD}✓ ALL TESTS PASSED! SUCCESS!{RESET}")
                print(f"   {GREEN}✓ Passed:  {total_passed}{RESET}")
                if total_skipped > 0:
                    print(f"   {YELLOW}⊘ Skipped: {total_skipped}{RESET}")
            elif total_failed > 0:
                print(f"{RED}{BOLD}✗ SOME TESTS FAILED!{RESET}")
                print(f"   {GREEN}✓ Passed:  {total_passed}{RESET}")
                print(f"   {RED}✗ Failed:  {total_failed}{RESET}")
                if total_skipped > 0:
                    print(f"   {YELLOW}⊘ Skipped: {total_skipped}{RESET}")
            
            print(f"{BLUE}{'='*80}\n{RESET}")
        
        return result.returncode
    
    except Exception as e:
        print(f"{RED}Error running tests: {e}{RESET}")
        return 1

if __name__ == "__main__":
    sys.exit(run_tests())
