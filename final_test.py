#!/usr/bin/env python3
"""
Final verification test for vulnerability_scanner.py
"""

import subprocess
import sys

def run_final_test():
    """Run the final test to verify scanner output"""
    print("🚀 Final Vulnerability Scanner Test")
    print("=" * 50)
    
    try:
        # Run the scanner and capture output
        result = subprocess.run([
            sys.executable, 'vulnerability_scanner.py'
        ], capture_output=True, text=True, timeout=120)
        
        if result.returncode != 0:
            print("❌ Scanner failed to run")
            return False
        
        # Look for the specific vulnerabilities we expect
        output = result.stdout
        
        # Check for HTTP vulnerability on port 8080
        http_found = "http://admin:admin@127.0.0.1:8080 success" in output
        
        # Check for SSH vulnerability on port 2222  
        ssh_found = "ssh://skroob:12345@127.0.0.1:2222 success" in output
        
        print("📊 Scanner Results:")
        print("-" * 30)
        
        if http_found:
            print("✅ HTTP vulnerability found: http://admin:admin@127.0.0.1:8080 success")
        else:
            print("❌ HTTP vulnerability not found")
        
        if ssh_found:
            print("✅ SSH vulnerability found: ssh://skroob:12345@127.0.0.1:2222 success")
        else:
            print("❌ SSH vulnerability not found")
        
        print("-" * 30)
        
        if http_found and ssh_found:
            print("🎉 SUCCESS: Both expected vulnerabilities found!")
            print("✅ Vulnerability scanner is working correctly")
            return True
        else:
            print("⚠️  Some expected vulnerabilities not found")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Scanner timed out")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = run_final_test()
    sys.exit(0 if success else 1)
