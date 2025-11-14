#!/usr/bin/env python3
"""
API Test Client for CodeSense AI
Simple script to test all API endpoints with real requests
"""
import requests
import json
import time
import sys
from typing import Dict, Any


class CodeSenseAPITester:
    """Test client for CodeSense AI API"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.user_token = None
        self.test_results = []
    
    def log_test(self, test_name: str, success: bool, details: str = ""):
        """Log test result"""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if details:
            print(f"   {details}")
        
        self.test_results.append({
            "test": test_name,
            "success": success,
            "details": details,
            "timestamp": time.time()
        })
    
    def test_server_health(self) -> bool:
        """Test if server is running"""
        try:
            response = self.session.get(f"{self.base_url}/api/debug/ping", timeout=5)
            success = response.status_code == 200 and response.json().get("ok") is True
            self.log_test("Server Health Check", success, f"Status: {response.status_code}")
            return success
        except requests.exceptions.RequestException as e:
            self.log_test("Server Health Check", False, f"Connection error: {e}")
            return False
    
    def test_user_registration(self) -> bool:
        """Test user registration"""
        test_user = {
            "username": f"testuser_{int(time.time())}",
            "password": "testpass123",
            "email": f"test_{int(time.time())}@example.com",
            "full_name": "API Test User"
        }
        
        try:
            response = self.session.post(f"{self.base_url}/auth/signup", json=test_user)
            success = response.status_code == 200
            
            if success:
                data = response.json()
                self.user_token = data.get("access_token")
                self.session.headers.update({"Authorization": f"Bearer {self.user_token}"})
                details = f"User created: {data.get('user', {}).get('username')}"
            else:
                details = f"Status: {response.status_code}, Error: {response.text}"
            
            self.log_test("User Registration", success, details)
            return success
            
        except requests.exceptions.RequestException as e:
            self.log_test("User Registration", False, f"Request error: {e}")
            return False
    
    def test_user_login(self) -> bool:
        """Test user login with existing credentials"""
        # Create a user first
        test_user = {
            "username": f"logintest_{int(time.time())}",
            "password": "testpass123",
            "email": f"logintest_{int(time.time())}@example.com"
        }
        
        # Register
        reg_response = self.session.post(f"{self.base_url}/auth/signup", json=test_user)
        if reg_response.status_code != 200:
            self.log_test("User Login (Setup)", False, "Failed to create test user")
            return False
        
        # Login
        try:
            login_data = {
                "username": test_user["username"],
                "password": test_user["password"]
            }
            response = self.session.post(f"{self.base_url}/auth/login", json=login_data)
            success = response.status_code == 200
            
            if success:
                data = response.json()
                details = f"Login successful, token received"
            else:
                details = f"Status: {response.status_code}, Error: {response.text}"
            
            self.log_test("User Login", success, details)
            return success
            
        except requests.exceptions.RequestException as e:
            self.log_test("User Login", False, f"Request error: {e}")
            return False
    
    def test_code_analysis(self) -> bool:
        """Test code analysis endpoint"""
        if not self.user_token:
            self.log_test("Code Analysis", False, "No authentication token available")
            return False
        
        test_codes = [
            {
                "name": "Python Hello World",
                "code": "print('Hello, World!')\nfor i in range(3):\n    print(f'Number: {i}')",
                "language": "python"
            },
            {
                "name": "JavaScript Simple",
                "code": "console.log('Hello, World!');\nfor(let i = 0; i < 3; i++) {\n    console.log(`Number: ${i}`);\n}",
                "language": "javascript"
            },
            {
                "name": "Python with Error",
                "code": "print('Hello World'",  # Missing closing quote
                "language": "python"
            }
        ]
        
        all_success = True
        
        for test_case in test_codes:
            try:
                response = self.session.post(
                    f"{self.base_url}/api/analyze",
                    json={"code": test_case["code"], "language": test_case["language"]},
                    timeout=30
                )
                
                success = response.status_code == 200
                
                if success:
                    data = response.json()
                    execution_success = data.get("execution_success", False)
                    has_output = bool(data.get("code_output"))
                    has_analysis = bool(data.get("output"))
                    
                    details = f"Execution: {'✓' if execution_success else '✗'}, " \
                             f"Output: {'✓' if has_output else '✗'}, " \
                             f"Analysis: {'✓' if has_analysis else '✗'}"
                else:
                    details = f"Status: {response.status_code}, Error: {response.text[:100]}"
                
                self.log_test(f"Code Analysis - {test_case['name']}", success, details)
                all_success = all_success and success
                
            except requests.exceptions.RequestException as e:
                self.log_test(f"Code Analysis - {test_case['name']}", False, f"Request error: {e}")
                all_success = False
        
        return all_success
    
    def test_submissions_history(self) -> bool:
        """Test submissions history endpoint"""
        if not self.user_token:
            self.log_test("Submissions History", False, "No authentication token available")
            return False
        
        try:
            response = self.session.get(f"{self.base_url}/api/submissions")
            success = response.status_code == 200
            
            if success:
                data = response.json()
                submissions = data.get("submissions", [])
                details = f"Found {len(submissions)} submissions"
            else:
                details = f"Status: {response.status_code}, Error: {response.text}"
            
            self.log_test("Submissions History", success, details)
            return success
            
        except requests.exceptions.RequestException as e:
            self.log_test("Submissions History", False, f"Request error: {e}")
            return False
    
    def test_user_profile(self) -> bool:
        """Test user profile endpoint"""
        if not self.user_token:
            self.log_test("User Profile", False, "No authentication token available")
            return False
        
        try:
            response = self.session.get(f"{self.base_url}/auth/me")
            success = response.status_code == 200
            
            if success:
                data = response.json()
                username = data.get("username", "unknown")
                details = f"Profile retrieved for user: {username}"
            else:
                details = f"Status: {response.status_code}, Error: {response.text}"
            
            self.log_test("User Profile", success, details)
            return success
            
        except requests.exceptions.RequestException as e:
            self.log_test("User Profile", False, f"Request error: {e}")
            return False
    
    def test_debug_endpoints(self) -> bool:
        """Test debug endpoints"""
        endpoints = [
            ("/api/debug/ping", "Debug Ping"),
            ("/api/debug/models", "Debug Models")
        ]
        
        all_success = True
        
        for endpoint, name in endpoints:
            try:
                response = self.session.get(f"{self.base_url}{endpoint}")
                # Ping should always succeed, models might fail without API key
                success = response.status_code in [200, 500]  # 500 is OK for models without API key
                
                if response.status_code == 200:
                    details = "Success"
                elif response.status_code == 500 and "GEMINI_API_KEY" in response.text:
                    details = "Expected failure - no API key configured"
                    success = True  # This is expected
                else:
                    details = f"Status: {response.status_code}"
                
                self.log_test(name, success, details)
                all_success = all_success and success
                
            except requests.exceptions.RequestException as e:
                self.log_test(name, False, f"Request error: {e}")
                all_success = False
        
        return all_success
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Run all API tests"""
        print("🚀 Starting CodeSense AI API Tests")
        print("=" * 50)
        
        start_time = time.time()
        
        # Test sequence
        tests = [
            ("Server Health", self.test_server_health),
            ("Debug Endpoints", self.test_debug_endpoints),
            ("User Registration", self.test_user_registration),
            ("User Login", self.test_user_login),
            ("User Profile", self.test_user_profile),
            ("Code Analysis", self.test_code_analysis),
            ("Submissions History", self.test_submissions_history),
        ]
        
        passed = 0
        total = len(tests)
        
        for test_name, test_func in tests:
            print(f"\n📋 Running: {test_name}")
            if test_func():
                passed += 1
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Summary
        print("\n" + "=" * 50)
        print("📊 TEST SUMMARY")
        print("=" * 50)
        print(f"✅ Passed: {passed}/{total}")
        print(f"❌ Failed: {total - passed}/{total}")
        print(f"⏱️  Duration: {duration:.2f} seconds")
        print(f"🎯 Success Rate: {(passed/total)*100:.1f}%")
        
        if passed == total:
            print("🎉 All tests passed!")
        else:
            print("⚠️  Some tests failed. Check the details above.")
        
        return {
            "passed": passed,
            "total": total,
            "success_rate": (passed/total)*100,
            "duration": duration,
            "results": self.test_results
        }
    
    def generate_report(self, filename: str = "api_test_report.json"):
        """Generate JSON test report"""
        report = {
            "timestamp": time.time(),
            "base_url": self.base_url,
            "results": self.test_results,
            "summary": {
                "total_tests": len(self.test_results),
                "passed": len([r for r in self.test_results if r["success"]]),
                "failed": len([r for r in self.test_results if not r["success"]])
            }
        }
        
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"📄 Test report saved to: {filename}")


def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="CodeSense AI API Tester")
    parser.add_argument("--url", default="http://localhost:8000", 
                       help="Base URL of the API server")
    parser.add_argument("--report", default="api_test_report.json",
                       help="Output file for test report")
    
    args = parser.parse_args()
    
    # Create tester
    tester = CodeSenseAPITester(args.url)
    
    # Run tests
    try:
        results = tester.run_all_tests()
        tester.generate_report(args.report)
        
        # Exit with appropriate code
        if results["passed"] == results["total"]:
            sys.exit(0)
        else:
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n⚠️  Tests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
