# 🚀 Quick Start Guide

**Get up and running in 5 minutes!**

---

## ⚡ Super Quick Start (2 minutes)

### 1. Setup Environment
```bash
# Navigate to project directory
cd project/

# Install dependencies (Python 3.11+ required)
py -3.11 -m pip install -r requirements_integrated.txt
```

### 2. Test Basic Functionality
```bash
# Generate 100 test pairs
py -3.11 scripts/build_pairs.py --target 100 --out test.jsonl

# Check the output
head -5 test.jsonl
```

### 3. Run Agent System
```bash
# Start the multi-agent orchestrator
py -3.11 scripts/agent_orchestrator.py
```

**🎉 You're ready to go!**

---

## 🔧 Full Setup (5 minutes)

### Prerequisites
- **Python 3.11+** (Required for compatibility)
- **Git** (For version control)
- **Internet connection** (For dataset downloads)

### Step 1: Environment Setup
```bash
# Check Python version
py -3.11 --version

# Install all dependencies
py -3.11 -m pip install -r requirements_integrated.txt

# Verify installation
py -3.11 -c "import datasets, numpy, anthropic; print('✅ All packages installed')"
```

### Step 2: Configuration
```bash
# Set up API keys (optional - for Claude/OpenAI integration)
export ANTHROPIC_API_KEY="your-claude-key"  # Linux/Mac
set ANTHROPIC_API_KEY=your-claude-key       # Windows

export OPENAI_API_KEY="your-openai-key"     # Linux/Mac
set OPENAI_API_KEY=your-openai-key          # Windows
```

### Step 3: Test All Components
```bash
# 1. Dataset Processing
py -3.11 scripts/build_pairs.py --target 500 --out sample.jsonl

# 2. Quality Evaluation
py -3.11 scripts/evaluate_dataset.py sample.jsonl

# 3. Agent System
py -3.11 scripts/agent_orchestrator.py

# 4. MCP Integration
py -3.11 scripts/mcp_integrated_system.py
```

---

## 📊 What You Can Do Now

### Dataset Processing
```bash
# Generate instruction-response pairs
py -3.11 scripts/build_pairs.py --target 5000 --out dataset.jsonl

# Options:
# --min-len 5          # Minimum token length
# --max-len 512        # Maximum token length  
# --dim 4096           # Embedding dimension
# --k auto             # Auto-determine clusters
```

### Quality Analysis
```bash
# Evaluate dataset quality
py -3.11 scripts/evaluate_dataset.py dataset.jsonl

# Output includes:
# - Total pairs and distribution
# - Intent classification stats
# - Cluster analysis
# - Quality metrics
```

### Multi-Agent Workflows
```bash
# Run agent orchestrator
py -3.11 scripts/agent_orchestrator.py

# Features:
# - 10+ node workflows
# - Multiple agent types
# - Tool integration
# - Memory management
```

### Claude Integration
```bash
# Set up Claude environment
py -3.11 scripts/claude_setup.py

# Demo Claude usage
py -3.11 scripts/claude_demo.py

# Evaluate responses
py -3.11 scripts/claude_eval.py
```

---

## 🎯 Common Use Cases

### 1. Generate Training Data
```bash
# Create 10,000 high-quality pairs
py -3.11 scripts/build_pairs.py \
  --target 10000 \
  --min-len 10 \
  --max-len 256 \
  --out training_data.jsonl
```

### 2. Analyze Dataset Quality
```bash
# Evaluate existing dataset
py -3.11 scripts/evaluate_dataset.py your_dataset.jsonl

# Look for:
# - Intent distribution balance
# - Cluster efficiency
# - Length statistics
# - Quality scores
```

### 3. Run Agent Workflow
```bash
# Execute multi-agent system
py -3.11 scripts/agent_orchestrator.py

# Monitor:
# - Agent interactions
# - Tool executions
# - Memory usage
# - Response quality
```

### 4. Test MCP Integration
```bash
# Run MCP system
py -3.11 scripts/mcp_integrated_system.py

# Features:
# - External tool integration
# - Server management
# - Tool registry
# - Enhanced agents
```

---

## 🚨 Troubleshooting

### Python Version Issues
```bash
# Problem: Python 3.12 compatibility issues
# Solution: Use Python 3.11
py -3.11 --version
py -3.11 -m pip install -r requirements_integrated.txt
```

### Missing Dependencies
```bash
# Problem: Import errors
# Solution: Reinstall dependencies
py -3.11 -m pip install --upgrade -r requirements_integrated.txt
```

### Memory Issues
```bash
# Problem: Out of memory for large datasets
# Solution: Reduce target size
py -3.11 scripts/build_pairs.py --target 1000 --out small_dataset.jsonl
```

### API Key Issues
```bash
# Problem: Claude/OpenAI API errors
# Solution: Check environment variables
echo $ANTHROPIC_API_KEY  # Linux/Mac
echo %ANTHROPIC_API_KEY% # Windows
```

---

## 📈 Performance Tips

### For Large Datasets
```bash
# Use streaming for memory efficiency
py -3.11 scripts/build_pairs.py --target 50000 --out large_dataset.jsonl

# Monitor memory usage
# Consider running in batches if memory is limited
```

### For Fast Processing
```bash
# Optimize for speed
py -3.11 scripts/build_pairs.py \
  --target 1000 \
  --dim 2048 \
  --k 16 \
  --out fast_dataset.jsonl
```

### For Quality Focus
```bash
# Optimize for quality
py -3.11 scripts/build_pairs.py \
  --target 5000 \
  --min-len 20 \
  --max-len 512 \
  --dim 4096 \
  --k auto \
  --out quality_dataset.jsonl
```

---

## 🔍 Monitoring & Debugging

### Check System Health
```bash
# Verify all components work
py -3.11 -c "
import datasets, numpy, anthropic
print('✅ Core dependencies OK')
"

# Test dataset loading
py -3.11 scripts/build_pairs.py --target 10 --out test.jsonl
```

### View Logs
```bash
# Most scripts output to stderr for logging
py -3.11 scripts/build_pairs.py --target 100 2>&1 | tee build.log

# Check for errors
grep -i error build.log
```

### Performance Monitoring
```bash
# Monitor memory usage (Linux/Mac)
top -p $(pgrep -f "python.*build_pairs")

# Monitor memory usage (Windows)
tasklist /FI "IMAGENAME eq python.exe"
```

---

## 📚 Next Steps

### Learn More
1. **Read Documentation**: Check `INTEGRATED_README.md`
2. **Explore Examples**: Look at generated datasets
3. **Customize Configs**: Modify `mcp_config.json` and `agent_flow_config.json`
4. **Extend Functionality**: Add new agents or tools

### Advanced Usage
1. **Custom Datasets**: Add your own data sources
2. **Agent Customization**: Create specialized agents
3. **Tool Integration**: Add new MCP tools
4. **Quality Metrics**: Implement custom evaluation

### Production Deployment
1. **Environment Setup**: Configure production environment
2. **Monitoring**: Set up logging and metrics
3. **Scaling**: Optimize for larger workloads
4. **Security**: Implement proper access controls

---

## 🆘 Need Help?

### Quick Reference
- **Main Docs**: `INTEGRATED_README.md`
- **Development Rules**: `DEVELOPMENT_RULES.md`
- **Current Status**: `CURRENT_STATUS.md`
- **Daily Checklist**: `DAILY_CHECKLIST.md`

### Common Commands
```bash
# Check status
py -3.11 --version
pip list | grep -E "(datasets|numpy|anthropic)"

# Test components
py -3.11 scripts/build_pairs.py --target 10
py -3.11 scripts/evaluate_dataset.py test.jsonl

# Get help
py -3.11 scripts/build_pairs.py --help
```

---

**🎉 You're all set! Start exploring the system and let me know if you need any help!**
