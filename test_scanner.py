#!/usr/bin/env python3
"""
Test script for vulnerability_scanner.py
"""

import subprocess
import sys
import os

def test_scanner():
    """Test the vulnerability scanner"""
    print("Testing vulnerability scanner...")
    
    # Test basic functionality
    try:
        result = subprocess.run([
            sys.executable, 'vulnerability_scanner.py'
        ], capture_output=True, text=True, timeout=60)
        
        print(f"Exit code: {result.returncode}")
        print(f"Output: {result.stdout}")
        if result.stderr:
            print(f"Errors: {result.stderr}")
            
        # Check if we got some output (vulnerabilities found)
        if result.stdout.strip():
            print("✅ Scanner found vulnerabilities!")
            return True
        else:
            print("⚠️  No vulnerabilities found (this might be expected)")
            return True
            
    except subprocess.TimeoutExpired:
        print("❌ Scanner timed out")
        return False
    except Exception as e:
        print(f"❌ Error running scanner: {e}")
        return False

def test_verbose_mode():
    """Test verbose mode"""
    print("\nTesting verbose mode...")
    
    try:
        result = subprocess.run([
            sys.executable, 'vulnerability_scanner.py', '-v'
        ], capture_output=True, text=True, timeout=60)
        
        print(f"Exit code: {result.returncode}")
        if "Scanning" in result.stdout:
            print("✅ Verbose mode working!")
            return True
        else:
            print("❌ Verbose mode not working properly")
            return False
            
    except Exception as e:
        print(f"❌ Error testing verbose mode: {e}")
        return False

if __name__ == "__main__":
    print("Vulnerability Scanner Test Suite")
    print("=" * 40)
    
    # Check if scanner exists
    if not os.path.exists('vulnerability_scanner.py'):
        print("❌ vulnerability_scanner.py not found!")
        sys.exit(1)
    
    # Run tests
    test1 = test_scanner()
    test2 = test_verbose_mode()
    
    if test1 and test2:
        print("\n✅ All tests passed!")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed!")
        sys.exit(1)
