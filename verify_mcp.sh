#!/bin/bash
echo "=== Project Chimera MCP Verification ==="
echo "Timestamp: $(date)"

echo "1. Checking MCP Sense connection..."
if curl -s http://localhost:3000/health > /dev/null 2>&1; then
    echo "✓ MCP Sense: ACTIVE on port 3000"
    
    # Log initialization event
    curl -X POST "http://localhost:3000/log" \
      -H "Content-Type: application/json" \
      -d "{\"project\": \"project-chimera\", \"event\": \"spec_kit_initialized\", \"phase\": \"specification\", \"timestamp\": \"$(date -Iseconds)\"}"
else
    echo "✗ MCP Sense: INACTIVE"
    echo "Please start Tenx MCP Sense before continuing"
    exit 1
fi

echo "2. Checking spec-kit installation..."
if command -v specify &> /dev/null; then
    echo "✓ Spec Kit: INSTALLED"
    specify --version
else
    echo "✗ Spec Kit: NOT FOUND"
    echo "Run: uvx --from git+https://github.com/github/spec-kit.git specify --help"
fi

echo "3. Checking directory structure..."
required_dirs=("specs" "tests" "skills" ".github/workflows")
for dir in "${required_dirs[@]}"; do
    if [ -d "$dir" ]; then
        echo "✓ Directory: $dir exists"
    else
        echo "✗ Missing: $dir"
    fi
done

echo "=== Verification Complete ==="
