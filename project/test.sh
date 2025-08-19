#!/bin/bash

echo "🚀 Enhanced Dataset Processing Pipeline"
echo "========================================"

# ขั้นตอนที่ 0: ดาวน์โหลด enhanced datasets
if [ ! -d "data/raw" ] || [ -z "$(ls -A data/raw 2>/dev/null)" ]; then
    echo ""
    echo "📥 Step 0: Downloading enhanced datasets..."
    python scripts/enhanced_download.py
    
    if [ $? -ne 0 ]; then
        echo "❌ Error downloading datasets"
        exit 1
    fi
fi

# ขั้นตอนที่ 1: ประมวลผลขั้นสูงพร้อม filtering และ intent classification
echo ""
echo "🔍 Step 1: Advanced processing with filtering and intent classification..."
python scripts/advanced_processor.py

if [ $? -ne 0 ]; then
    echo "❌ Error in advanced processing"
    exit 1
fi

# ขั้นตอนที่ 2: วิเคราะห์ overlap ด้วย embedding clustering
echo ""
echo "📊 Step 2: Analyzing dataset overlap with clustering..."
python scripts/embedding_analyzer.py

if [ $? -ne 0 ]; then
    echo "❌ Error in clustering analysis"
    exit 1
fi

# ขั้นตอนที่ 3: ประเมินคุณภาพด้วย similarity (fallback)
echo ""
echo "📈 Step 3: Final quality evaluation..."
if [ -f "enhanced_dataset.jsonl" ]; then
    python scripts/basic_test.py enhanced_dataset.jsonl
else
    python scripts/basic_test.py
fi

if [ $? -ne 0 ]; then
    echo "❌ Error in quality evaluation"
    exit 1
fi

echo ""
echo "✅ Enhanced Pipeline completed successfully!"
echo "📁 Generated files:"
echo "   - enhanced_dataset.jsonl (filtered & classified)"
echo "   - data/dataset_manifest.json (tracking metadata)"
echo "   - processing_report.json (processing summary)"
echo "   - cluster_analysis.json (overlap analysis)"
echo "   - results.json (quality evaluation)"
