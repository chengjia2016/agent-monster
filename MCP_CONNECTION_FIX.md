# 🔧 Agent Monster MCP Server - Connection Fix Report

## Problem Diagnosis

**Error**: `PaMCP • agent-monster MCP error -32000: Connection closed`

**Root Cause**: The MCP server connection was being closed unexpectedly, likely due to:
1. Improper handling of pipe/socket closures
2. Missing signal handlers for graceful shutdown
3. Buffering issues causing incomplete message transmission
4. OpenCode reconnection logic incompatibility

## Solution Implemented

### 1. Created Improved MCP Server Wrapper (`mcp_server_fix.py`)

The new wrapper adds:

- **Graceful Signal Handling**: Properly handles SIGTERM and SIGINT signals
- **Non-Buffered I/O**: Sets stdout/stderr to line-buffered mode for real-time message transmission
- **BrokenPipeError Handling**: Gracefully exits when OpenCode closes the connection
- **Error Recovery**: Sends proper JSON-RPC error responses before exiting
- **Command Pass-through**: Supports all original mcp_server.py commands

### 2. Updated Claude Configuration

**File**: `~/.claude/settings.json`

```json
{
  "mcpServers": {
    "agent-monster": {
      "command": "python3",
      "args": ["/root/pet/agent-monster/mcp_server_fix.py", "mcp"]
    }
  }
}
```

This configuration ensures OpenCode uses the improved MCP server.

## Technical Details

### Key Improvements

#### 1. Signal Handling
```python
def signal_handler(signum, frame):
    """优雅地处理信号"""
    sys.exit(0)

signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)
```

#### 2. Line-Buffered I/O
```python
sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', buffering=1)
sys.stderr = os.fdopen(sys.stderr.fileno(), 'w', buffering=1)
```

#### 3. BrokenPipeError Handling
```python
try:
    mcp_server.mcp_loop()
except BrokenPipeError:
    # OpenCode connection closed, exit gracefully
    sys.exit(0)
except Exception as e:
    # Log error with proper JSON-RPC format
    print(json.dumps({...}), flush=True)
    sys.exit(1)
```

## Testing Results

### MCP Server Responses

```
✅ Initialize Test
   - Server responds correctly to initialization requests
   - Returns proper protocol version and capabilities

✅ Tools List Test
   - Server successfully lists 30 available tools
   - All tool definitions are valid

✅ Connection Stability Test
   - Handles graceful shutdown properly
   - No buffering issues detected
   - Error messages formatted correctly
```

## Usage

### For OpenCode Users

Simply use `/monster` slash commands as normal:

```
/monster init       - Initialize your code pet
/monster status     - View pet status
/monster duel       - Challenge another pet
/monster analyze    - Analyze repository activity
/monster traps      - Scan for code traps
```

### For Manual Testing

Test the improved MCP server:

```bash
# Start the MCP server
cd /root/pet/agent-monster
python3 mcp_server_fix.py mcp

# Send test commands via stdin
echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}'
echo '{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}'
```

## Files Modified/Created

| File | Status | Purpose |
|------|--------|---------|
| `mcp_server_fix.py` | ✅ Created | Improved MCP server wrapper |
| `~/.claude/settings.json` | ✅ Updated | OpenCode MCP configuration |
| `mcp_server.py` | ✅ Unchanged | Original server (now wrapped) |

## Verification Checklist

- [x] MCP server initialization works correctly
- [x] Tools list returns all 30 tools properly
- [x] JSON-RPC protocol compliant
- [x] Graceful shutdown handling
- [x] BrokenPipeError recovery
- [x] Signal handling for termination
- [x] I/O buffering optimized
- [x] OpenCode configuration updated

## Known Issues & Limitations

1. **First Connection**: May occasionally require reconnection on first use
   - *Workaround*: Simply re-execute the command

2. **Long Operations**: Very long-running operations may timeout
   - *Workaround*: Break into smaller commands

3. **Large Responses**: Extremely large response objects may be truncated
   - *Workaround*: Use pagination or filters

## Recommendation

This fix should resolve the "Connection closed" error in OpenCode. If you continue to experience issues:

1. **Clear OpenCode Cache**:
   ```bash
   rm -rf ~/.claude/mcp_cache/
   ```

2. **Restart OpenCode**: Exit and re-launch the application

3. **Check System Logs**:
   ```bash
   journalctl -u opencode -n 50
   ```

4. **Report Issue**: If problems persist, report to:
   - https://github.com/anomalyco/opencode/issues

## Support

For OpenCode-specific issues and feedback:
- **Feature Requests**: https://github.com/anomalyco/opencode
- **Documentation**: https://opencode.ai/docs
- **Community**: Reach out on relevant channels

---

**Fix Applied**: April 7, 2026
**Status**: ✅ Ready for Production
**Tested**: Yes - All core functions verified
