#!/usr/bin/env python3
"""
Test Suite for Slash Command Integration with MCP Server
Tests the three new MCP tools: monster_slash_help, monster_slash_list, monster_slash_completions
"""

import json
import subprocess
import time
import sys
from typing import Dict, List, Any


class MCPServerTester:
    """Test the MCP server and slash command tools"""
    
    def __init__(self):
        self.proc = None
        self.responses = []
        
    def start_server(self):
        """Start the MCP server"""
        self.proc = subprocess.Popen(
            ["python3", "mcp_server.py", "mcp"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )
    
    def send_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Send a request to MCP server and get response"""
        if not self.proc:
            self.start_server()
            time.sleep(0.5)  # Give server time to start
        
        # Send request
        input_data = json.dumps(request) + "\n"
        self.proc.stdin.write(input_data)
        self.proc.stdin.flush()
        
        # Read response
        try:
            line = self.proc.stdout.readline()
            if line:
                return json.loads(line)
        except Exception as e:
            print(f"Error reading response: {e}")
        
        return {}
    
    def stop_server(self):
        """Stop the MCP server"""
        if self.proc:
            try:
                self.proc.terminate()
                self.proc.wait(timeout=2)
            except:
                self.proc.kill()
    
    def test_tools_registered(self) -> bool:
        """Test that slash command tools are registered"""
        print("=" * 50)
        print("TEST: Tools Registration")
        print("=" * 50)
        
        # Initialize
        init_req = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize"
        }
        self.send_request(init_req)
        time.sleep(0.2)
        
        # List tools
        list_req = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list"
        }
        response = self.send_request(list_req)
        
        if "result" not in response:
            print("✗ Failed to get tools list")
            return False
        
        tools = response["result"].get("tools", [])
        tool_names = [t["name"] for t in tools]
        
        print(f"Total tools registered: {len(tools)}")
        
        required_tools = [
            "monster_slash_help",
            "monster_slash_list", 
            "monster_slash_completions"
        ]
        
        all_present = True
        for tool in required_tools:
            if tool in tool_names:
                print(f"  ✓ {tool}")
            else:
                print(f"  ✗ {tool} NOT FOUND")
                all_present = False
        
        return all_present
    
    def test_slash_help(self) -> bool:
        """Test monster_slash_help tool"""
        print("\n" + "=" * 50)
        print("TEST: monster_slash_help")
        print("=" * 50)
        
        # Test without command_name
        req = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {
                "name": "monster_slash_help",
                "arguments": {}
            }
        }
        
        response = self.send_request(req)
        time.sleep(0.2)
        
        if "result" not in response:
            print("✗ Failed to get response")
            return False
        
        content = response["result"]["content"][0]["text"]
        
        # Check for expected content
        checks = [
            ("Contains header", "Agent Monster" in content),
            ("Contains menu section", "MENU" in content),
            ("Non-empty", len(content) > 100)
        ]
        
        all_pass = True
        for check_name, passed in checks:
            print(f"  {'✓' if passed else '✗'} {check_name}")
            all_pass = all_pass and passed
        
        print(f"\nResponse preview:\n{content[:200]}...\n")
        return all_pass
    
    def test_slash_list(self) -> bool:
        """Test monster_slash_list tool"""
        print("=" * 50)
        print("TEST: monster_slash_list")
        print("=" * 50)
        
        req = {
            "jsonrpc": "2.0",
            "id": 4,
            "method": "tools/call",
            "params": {
                "name": "monster_slash_list",
                "arguments": {}
            }
        }
        
        response = self.send_request(req)
        time.sleep(0.2)
        
        if "result" not in response:
            print("✗ Failed to get response")
            return False
        
        content = response["result"]["content"][0]["text"]
        
        # Check for expected content
        checks = [
            ("Contains commands", ("menu" in content.lower() or "/" in content)),
            ("Non-empty", len(content) > 100)
        ]
        
        all_pass = True
        for check_name, passed in checks:
            print(f"  {'✓' if passed else '✗'} {check_name}")
            all_pass = all_pass and passed
        
        print(f"\nResponse preview:\n{content[:200]}...\n")
        return all_pass
    
    def test_slash_completions(self) -> bool:
        """Test monster_slash_completions tool"""
        print("=" * 50)
        print("TEST: monster_slash_completions")
        print("=" * 50)
        
        # Test with various prefixes
        prefixes = ["menu", "shop"]
        all_pass = True
        
        for prefix in prefixes:
            req = {
                "jsonrpc": "2.0",
                "id": 5,
                "method": "tools/call",
                "params": {
                    "name": "monster_slash_completions",
                    "arguments": {"prefix": prefix}
                }
            }
            
            response = self.send_request(req)
            time.sleep(0.2)
            
            if "result" not in response:
                print(f"  ✗ Failed to get response for prefix '{prefix}'")
                all_pass = False
                continue
            
            content = response["result"]["content"][0]["text"]
            
            # Check for expected content - just check that we get a response
            has_content = len(content) > 50
            print(f"  {'✓' if has_content else '✗'} Completions for '{prefix}': {len(content)} chars")
            all_pass = all_pass and has_content
        
        return all_pass
    
    def test_tool_schemas(self) -> bool:
        """Test that tool schemas are correctly defined"""
        print("\n" + "=" * 50)
        print("TEST: Tool Input Schemas")
        print("=" * 50)
        
        # Initialize and get tools
        init_req = {"jsonrpc": "2.0", "id": 1, "method": "initialize"}
        self.send_request(init_req)
        time.sleep(0.2)
        
        list_req = {"jsonrpc": "2.0", "id": 2, "method": "tools/list"}
        response = self.send_request(list_req)
        
        if "result" not in response:
            print("✗ Failed to get tools list")
            return False
        
        tools = response["result"].get("tools", [])
        tool_map = {t["name"]: t for t in tools}
        
        all_pass = True
        
        # Check monster_slash_help
        if "monster_slash_help" in tool_map:
            tool = tool_map["monster_slash_help"]
            schema = tool.get("inputSchema", {})
            props = schema.get("properties", {})
            has_command_name = "command_name" in props
            print(f"  ✓ monster_slash_help has command_name parameter" if has_command_name else f"  ✗ monster_slash_help missing command_name")
            all_pass = all_pass and has_command_name
        
        # Check monster_slash_list
        if "monster_slash_list" in tool_map:
            print(f"  ✓ monster_slash_list is defined")
        else:
            print(f"  ✗ monster_slash_list not found")
            all_pass = False
        
        # Check monster_slash_completions
        if "monster_slash_completions" in tool_map:
            tool = tool_map["monster_slash_completions"]
            schema = tool.get("inputSchema", {})
            props = schema.get("properties", {})
            has_prefix = "prefix" in props
            print(f"  ✓ monster_slash_completions has prefix parameter" if has_prefix else f"  ✗ monster_slash_completions missing prefix")
            all_pass = all_pass and has_prefix
        
        return all_pass


def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print(" Slash Command Integration Test Suite")
    print("=" * 60 + "\n")
    
    tester = MCPServerTester()
    
    try:
        tests = [
            ("Tools Registration", tester.test_tools_registered),
            ("Tool Input Schemas", tester.test_tool_schemas),
            ("monster_slash_help", tester.test_slash_help),
            ("monster_slash_list", tester.test_slash_list),
            ("monster_slash_completions", tester.test_slash_completions),
        ]
        
        results = []
        for test_name, test_func in tests:
            try:
                result = test_func()
                results.append((test_name, result))
            except Exception as e:
                print(f"✗ Test '{test_name}' failed with error: {e}")
                results.append((test_name, False))
        
        # Summary
        print("\n" + "=" * 60)
        print(" Test Summary")
        print("=" * 60)
        
        passed = sum(1 for _, result in results if result)
        total = len(results)
        
        for test_name, result in results:
            status = "✓ PASS" if result else "✗ FAIL"
            print(f"{status}: {test_name}")
        
        print(f"\nTotal: {passed}/{total} tests passed")
        
        if passed == total:
            print("\n🎉 All tests passed!")
            return 0
        else:
            print(f"\n⚠️  {total - passed} test(s) failed")
            return 1
    
    finally:
        tester.stop_server()


if __name__ == "__main__":
    sys.exit(main())
