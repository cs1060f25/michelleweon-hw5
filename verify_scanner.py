#!/usr/bin/env python3
"""
Verification script for vulnerability_scanner.py
Tests the scanner against running HTTP and SSH servers
"""

import subprocess
import sys
import re

def verify_scanner_output():
    """Verify the vulnerability scanner produces correct output"""
    print("🔍 Running vulnerability scanner verification...")
    print("=" * 60)
    
    try:
        # Run the scanner
        result = subprocess.run([
            sys.executable, 'vulnerability_scanner.py'
        ], capture_output=True, text=True, timeout=120)
        
        print(f"Exit code: {result.returncode}")
        
        if result.returncode != 0:
            print("❌ Scanner failed to run")
            return False
        
        # Parse the output
        output_lines = result.stdout.strip().split('\n')
        vulnerabilities = []
        
        for line in output_lines:
            if line.strip():
                vulnerabilities.append(line.strip())
        
        print(f"📊 Found {len(vulnerabilities)} vulnerabilities:")
        print("-" * 40)
        
        # Check for expected vulnerabilities
        expected_patterns = [
            r'http://admin:admin@127\.0\.0\.1:8080\s+success',
            r'ssh://skroob:12345@127\.0\.0\.1:2222\s+success'
        ]
        
        found_expected = []
        for vuln in vulnerabilities:
            print(f"✅ {vuln[:80]}{'...' if len(vuln) > 80 else ''}")
            
            # Check if this matches expected patterns
            for pattern in expected_patterns:
                if re.search(pattern, vuln):
                    found_expected.append(pattern)
        
        print("-" * 40)
        
        # Verify we found the expected vulnerabilities
        if len(found_expected) >= 2:
            print("✅ SUCCESS: Found expected HTTP and SSH vulnerabilities!")
            print(f"   - HTTP server on port 8080 with admin:admin")
            print(f"   - SSH server on port 2222 with skroob:12345")
            return True
        else:
            print("⚠️  WARNING: Expected vulnerabilities not found")
            print(f"   Found {len(found_expected)}/2 expected patterns")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Scanner timed out")
        return False
    except Exception as e:
        print(f"❌ Error running scanner: {e}")
        return False

def check_servers_running():
    """Check if the required servers are running"""
    print("🔍 Checking if servers are running...")
    
    try:
        # Check HTTP server
        http_result = subprocess.run([
            'curl', '-s', '-u', 'admin:admin', 'http://127.0.0.1:8080/'
        ], capture_output=True, text=True, timeout=5)
        
        if http_result.returncode == 0 and 'success' in http_result.stdout:
            print("✅ HTTP server running on port 8080")
            http_ok = True
        else:
            print("❌ HTTP server not responding on port 8080")
            http_ok = False
        
        # Check SSH server (basic port check)
        ssh_result = subprocess.run([
            'nc', '-z', '127.0.0.1', '2222'
        ], capture_output=True, text=True, timeout=5)
        
        if ssh_result.returncode == 0:
            print("✅ SSH server running on port 2222")
            ssh_ok = True
        else:
            print("❌ SSH server not responding on port 2222")
            ssh_ok = False
        
        return http_ok and ssh_ok
        
    except Exception as e:
        print(f"❌ Error checking servers: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Vulnerability Scanner Verification")
    print("=" * 60)
    
    # Check if servers are running
    servers_ok = check_servers_running()
    print()
    
    if not servers_ok:
        print("⚠️  Some servers are not running. Please start them first:")
        print("   cd hw5_server && python3 http_server.py --port 8080 --username admin --password admin &")
        print("   cd hw5_server && python3 ssh_server.py --port 2222 --username skroob --password 12345 &")
        print()
    
    # Run scanner verification
    scanner_ok = verify_scanner_output()
    
    print("\n" + "=" * 60)
    if scanner_ok:
        print("🎉 VERIFICATION PASSED: Vulnerability scanner is working correctly!")
        sys.exit(0)
    else:
        print("❌ VERIFICATION FAILED: Scanner needs attention")
        sys.exit(1)
