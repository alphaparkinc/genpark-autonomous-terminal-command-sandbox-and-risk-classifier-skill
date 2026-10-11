"""MCP server for Autonomous Terminal Command Sandbox & Risk Classifier."""
import sys
import json
from client import TerminalCommandRiskClassifier

def handle_request(req):
    method = req.get("method")
    if method == "tools/list":
        return {
            "tools": [{
                "name": "classify_terminal_command",
                "description": "Audits shell commands for destructive blast radius before execution",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "command": {"type": "string"}
                    },
                    "required": ["command"]
                }
            }]
        }
    elif method == "tools/call":
        params = req.get("params", {})
        if params.get("name") == "classify_terminal_command":
            cmd = params.get("arguments", {}).get("command", "")
            res = TerminalCommandRiskClassifier.classify_command(cmd)
            return {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
    return {"error": "Method not found"}

if __name__ == "__main__":
    for line in sys.stdin:
        if line.strip():
            print(json.dumps(handle_request(json.loads(line))))
            sys.stdout.flush()
