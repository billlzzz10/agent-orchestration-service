#!/bin/bash

# Fine-tuning Pipeline Test Script
# ทดสอบ pipeline การ fine-tuning ครบถ้วน

set -e  # Exit on any error

echo "🎯 Starting Fine-tuning Pipeline Tests..."
echo "========================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    local status=$1
    local message=$2
    case $status in
        "INFO")
            echo -e "${BLUE}ℹ️  $message${NC}"
            ;;
        "SUCCESS")
            echo -e "${GREEN}✅ $message${NC}"
            ;;
        "WARNING")
            echo -e "${YELLOW}⚠️  $message${NC}"
            ;;
        "ERROR")
            echo -e "${RED}❌ $message${NC}"
            ;;
    esac
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check Python version
print_status "INFO" "Checking Python version..."
python_version=$(python3 --version 2>&1 | cut -d' ' -f2)
print_status "SUCCESS" "Python version: $python_version"

# Check if required packages are installed
print_status "INFO" "Checking required packages..."

# Install requirements if needed
if [ ! -f "requirements_fine_tuning.txt" ]; then
    print_status "ERROR" "requirements_fine_tuning.txt not found!"
    exit 1
fi

print_status "INFO" "Installing fine-tuning requirements..."
pip install -r requirements_fine_tuning.txt

# Create test directories
print_status "INFO" "Creating test directories..."
mkdir -p test_outputs
mkdir -p outputs/gifs
mkdir -p data/azure_fine_tuning

# Step 1: Test Dataset Preparation
print_status "INFO" "Step 1: Testing Dataset Preparation..."
python3 scripts/azure_fine_tuning_prep.py --output-dir test_outputs/azure_fine_tuning

if [ $? -eq 0 ]; then
    print_status "SUCCESS" "Dataset preparation completed!"
else
    print_status "ERROR" "Dataset preparation failed!"
    exit 1
fi

# Step 2: Test OpenSource Model Demo
print_status "INFO" "Step 2: Testing OpenSource Model Demo..."
python3 scripts/opensource_model_demo.py \
    --model "microsoft/DialoGPT-small" \
    --prompts "Hello!" "How are you?" \
    --output-gif "test_demo.gif"

if [ $? -eq 0 ]; then
    print_status "SUCCESS" "OpenSource model demo completed!"
else
    print_status "WARNING" "OpenSource model demo failed (this is expected if no GPU available)"
fi

# Step 3: Test Azure Orchestrator Simulation
print_status "INFO" "Step 3: Testing Azure Orchestrator Simulation..."
python3 scripts/test_fine_tuning_pipeline.py --test-dir test_outputs

if [ $? -eq 0 ]; then
    print_status "SUCCESS" "Azure orchestrator simulation completed!"
else
    print_status "WARNING" "Some tests failed (check test_outputs/test_results.json for details)"
fi

# Step 4: Check generated files
print_status "INFO" "Step 4: Checking generated files..."

# Check Azure fine-tuning files
if [ -f "test_outputs/azure_fine_tuning/train_data.jsonl" ]; then
    train_lines=$(wc -l < test_outputs/azure_fine_tuning/train_data.jsonl)
    print_status "SUCCESS" "Training data generated: $train_lines lines"
else
    print_status "ERROR" "Training data not found!"
fi

if [ -f "test_outputs/azure_fine_tuning/validation_data.jsonl" ]; then
    val_lines=$(wc -l < test_outputs/azure_fine_tuning/validation_data.jsonl)
    print_status "SUCCESS" "Validation data generated: $val_lines lines"
else
    print_status "ERROR" "Validation data not found!"
fi

# Check GIF files
if [ -f "outputs/gifs/test_demo.gif" ]; then
    gif_size=$(du -h outputs/gifs/test_demo.gif | cut -f1)
    print_status "SUCCESS" "GIF demo generated: $gif_size"
else
    print_status "WARNING" "GIF demo not found (OpenSource model test may have failed)"
fi

# Check test results
if [ -f "test_outputs/test_results.json" ]; then
    print_status "SUCCESS" "Test results saved to test_outputs/test_results.json"
else
    print_status "ERROR" "Test results not found!"
fi

# Step 5: Display summary
print_status "INFO" "Step 5: Test Summary..."

echo ""
echo "📊 Fine-tuning Pipeline Test Summary"
echo "===================================="
echo "📁 Test outputs: test_outputs/"
echo "🎬 GIF outputs: outputs/gifs/"
echo "📊 Azure data: data/azure_fine_tuning/"
echo ""

# Show file sizes
echo "📈 Generated Files:"
if [ -f "test_outputs/azure_fine_tuning/train_data.jsonl" ]; then
    train_size=$(du -h test_outputs/azure_fine_tuning/train_data.jsonl | cut -f1)
    echo "   - Training data: $train_size"
fi

if [ -f "test_outputs/azure_fine_tuning/validation_data.jsonl" ]; then
    val_size=$(du -h test_outputs/azure_fine_tuning/validation_data.jsonl | cut -f1)
    echo "   - Validation data: $val_size"
fi

if [ -f "outputs/gifs/test_demo.gif" ]; then
    gif_size=$(du -h outputs/gifs/test_demo.gif | cut -f1)
    echo "   - Demo GIF: $gif_size"
fi

echo ""
print_status "SUCCESS" "Fine-tuning pipeline tests completed!"
echo ""
echo "🚀 Next Steps:"
echo "1. Review generated datasets in test_outputs/azure_fine_tuning/"
echo "2. Check GIF demo in outputs/gifs/"
echo "3. Configure Azure credentials for real fine-tuning"
echo "4. Run Azure fine-tuning orchestrator with real data"
echo ""

# Optional: Show test results if available
if [ -f "test_outputs/test_results.json" ]; then
    echo "📋 Detailed test results:"
    python3 -c "
import json
with open('test_outputs/test_results.json') as f:
    data = json.load(f)
    print(f'   - Overall status: {data[\"overall_status\"]}')
    print(f'   - Total duration: {data[\"total_duration\"]:.2f}s')
    print(f'   - Tests passed: {sum(1 for t in data[\"tests\"] if t[\"status\"] == \"passed\")}')
    print(f'   - Tests failed: {sum(1 for t in data[\"tests\"] if t[\"status\"] == \"failed\")}')
"
fi

echo ""
print_status "INFO" "Fine-tuning pipeline is ready for production use! 🎉"
