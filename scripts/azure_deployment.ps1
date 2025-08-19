# Azure Fine-tuning Deployment Script
# สคริปต์สำหรับ deploy fine-tuned model ไปยัง Azure OpenAI

param(
    [Parameter(Mandatory=$true)]
    [string]$SubscriptionId,
    
    [Parameter(Mandatory=$true)]
    [string]$ResourceGroup,
    
    [Parameter(Mandatory=$true)]
    [string]$Location = "eastus",
    
    [Parameter(Mandatory=$true)]
    [string]$OpenAIResourceName,
    
    [Parameter(Mandatory=$true)]
    [string]$StorageAccountName,
    
    [string]$ModelName = "ai-training-platform-model",
    [string]$DeploymentName = "ai-training-platform-model-v1"
)

# Colors for output
$Red = "Red"
$Green = "Green"
$Yellow = "Yellow"
$Blue = "Blue"

function Write-ColorOutput {
    param(
        [string]$Message,
        [string]$Color = "White"
    )
    Write-Host $Message -ForegroundColor $Color
}

function Write-Status {
    param(
        [string]$Status,
        [string]$Message
    )
    switch ($Status) {
        "INFO" { Write-ColorOutput "ℹ️  $Message" $Blue }
        "SUCCESS" { Write-ColorOutput "✅ $Message" $Green }
        "WARNING" { Write-ColorOutput "⚠️  $Message" $Yellow }
        "ERROR" { Write-ColorOutput "❌ $Message" $Red }
    }
}

# Start deployment
Write-Status "INFO" "🚀 Starting Azure Fine-tuning Deployment..."
Write-Status "INFO" "Model: $ModelName"
Write-Status "INFO" "Resource Group: $ResourceGroup"
Write-Status "INFO" "Location: $Location"

# Step 1: Login to Azure
Write-Status "INFO" "Step 1: Logging into Azure..."
try {
    az login
    az account set --subscription $SubscriptionId
    Write-Status "SUCCESS" "Azure login successful"
} catch {
    Write-Status "ERROR" "Failed to login to Azure: $($_.Exception.Message)"
    exit 1
}

# Step 2: Create Resource Group
Write-Status "INFO" "Step 2: Creating Resource Group..."
try {
    az group create --name $ResourceGroup --location $Location
    Write-Status "SUCCESS" "Resource group created: $ResourceGroup"
} catch {
    Write-Status "WARNING" "Resource group may already exist"
}

# Step 3: Create Storage Account
Write-Status "INFO" "Step 3: Creating Storage Account..."
try {
    az storage account create `
        --name $StorageAccountName `
        --resource-group $ResourceGroup `
        --location $Location `
        --sku Standard_LRS `
        --kind StorageV2
    
    Write-Status "SUCCESS" "Storage account created: $StorageAccountName"
} catch {
    Write-Status "WARNING" "Storage account may already exist"
}

# Step 4: Create Storage Container
Write-Status "INFO" "Step 4: Creating Storage Container..."
try {
    $storageKey = az storage account keys list --account-name $StorageAccountName --resource-group $ResourceGroup --query "[0].value" -o tsv
    az storage container create `
        --name "fine-tuning-data" `
        --account-name $StorageAccountName `
        --account-key $storageKey
    
    Write-Status "SUCCESS" "Storage container created: fine-tuning-data"
} catch {
    Write-Status "WARNING" "Storage container may already exist"
}

# Step 5: Upload Dataset
Write-Status "INFO" "Step 5: Uploading Dataset..."
try {
    $datasetPath = "outputs/datasets/azure_fine_tuning_data.jsonl"
    if (Test-Path $datasetPath) {
        az storage blob upload `
            --account-name $StorageAccountName `
            --account-key $storageKey `
            --container-name "fine-tuning-data" `
            --name "training_data.jsonl" `
            --file $datasetPath `
            --overwrite
        
        Write-Status "SUCCESS" "Dataset uploaded successfully"
    } else {
        Write-Status "ERROR" "Dataset file not found: $datasetPath"
        exit 1
    }
} catch {
    Write-Status "ERROR" "Failed to upload dataset: $($_.Exception.Message)"
    exit 1
}

# Step 6: Create Azure OpenAI Resource
Write-Status "INFO" "Step 6: Creating Azure OpenAI Resource..."
try {
    az cognitiveservices account create `
        --name $OpenAIResourceName `
        --resource-group $ResourceGroup `
        --kind OpenAI `
        --sku S0 `
        --location $Location
    
    Write-Status "SUCCESS" "Azure OpenAI resource created: $OpenAIResourceName"
} catch {
    Write-Status "WARNING" "Azure OpenAI resource may already exist"
}

# Step 7: Get OpenAI API Key
Write-Status "INFO" "Step 7: Getting OpenAI API Key..."
try {
    $openaiKey = az cognitiveservices account keys list --name $OpenAIResourceName --resource-group $ResourceGroup --query "key1" -o tsv
    $openaiEndpoint = az cognitiveservices account show --name $OpenAIResourceName --resource-group $ResourceGroup --query "properties.endpoint" -o tsv
    
    Write-Status "SUCCESS" "OpenAI API key retrieved"
    Write-Status "INFO" "Endpoint: $openaiEndpoint"
} catch {
    Write-Status "ERROR" "Failed to get OpenAI API key: $($_.Exception.Message)"
    exit 1
}

# Step 8: Create Fine-tuning Job
Write-Status "INFO" "Step 8: Creating Fine-tuning Job..."
try {
    $trainingFileUrl = "https://$StorageAccountName.blob.core.windows.net/fine-tuning-data/training_data.jsonl"
    
    # Create fine-tuning job using REST API
    $headers = @{
        "api-key" = $openaiKey
        "Content-Type" = "application/json"
    }
    
    $body = @{
        model = "gpt-35-turbo"
        training_file = $trainingFileUrl
        hyperparameters = @{
            n_epochs = 3
            batch_size = 1
            learning_rate_multiplier = 1.0
        }
    } | ConvertTo-Json -Depth 3
    
    $response = Invoke-RestMethod `
        -Uri "$openaiEndpoint/openai/deployments/fine-tunings?api-version=2024-02-15-preview" `
        -Method POST `
        -Headers $headers `
        -Body $body
    
    $jobId = $response.id
    Write-Status "SUCCESS" "Fine-tuning job created: $jobId"
} catch {
    Write-Status "ERROR" "Failed to create fine-tuning job: $($_.Exception.Message)"
    exit 1
}

# Step 9: Monitor Fine-tuning Job
Write-Status "INFO" "Step 9: Monitoring Fine-tuning Job..."
try {
    $maxAttempts = 60  # 5 minutes with 5-second intervals
    $attempt = 0
    
    while ($attempt -lt $maxAttempts) {
        $jobStatus = Invoke-RestMethod `
            -Uri "$openaiEndpoint/openai/deployments/fine-tunings/$jobId?api-version=2024-02-15-preview" `
            -Method GET `
            -Headers $headers
        
        Write-Status "INFO" "Job status: $($jobStatus.status)"
        
        if ($jobStatus.status -eq "succeeded") {
            Write-Status "SUCCESS" "Fine-tuning completed successfully!"
            $fineTunedModel = $jobStatus.fine_tuned_model
            break
        } elseif ($jobStatus.status -eq "failed") {
            Write-Status "ERROR" "Fine-tuning failed: $($jobStatus.error.message)"
            exit 1
        }
        
        Start-Sleep -Seconds 5
        $attempt++
    }
    
    if ($attempt -eq $maxAttempts) {
        Write-Status "WARNING" "Fine-tuning job still running after timeout"
    }
} catch {
    Write-Status "ERROR" "Failed to monitor fine-tuning job: $($_.Exception.Message)"
    exit 1
}

# Step 10: Deploy Fine-tuned Model
Write-Status "INFO" "Step 10: Deploying Fine-tuned Model..."
try {
    $deploymentBody = @{
        model = $fineTunedModel
        scale_settings = @{
            scale_type = "Standard"
        }
    } | ConvertTo-Json -Depth 3
    
    $deploymentResponse = Invoke-RestMethod `
        -Uri "$openaiEndpoint/openai/deployments/$DeploymentName?api-version=2024-02-15-preview" `
        -Method PUT `
        -Headers $headers `
        -Body $deploymentBody
    
    Write-Status "SUCCESS" "Model deployed successfully: $DeploymentName"
} catch {
    Write-Status "ERROR" "Failed to deploy model: $($_.Exception.Message)"
    exit 1
}

# Step 11: Test Deployment
Write-Status "INFO" "Step 11: Testing Deployment..."
try {
    $testBody = @{
        messages = @(
            @{
                role = "user"
                content = "Hello! How are you today?"
            }
        )
        max_tokens = 150
        temperature = 0.7
    } | ConvertTo-Json -Depth 3
    
    $testResponse = Invoke-RestMethod `
        -Uri "$openaiEndpoint/openai/deployments/$DeploymentName/chat/completions?api-version=2024-02-15-preview" `
        -Method POST `
        -Headers $headers `
        -Body $testBody
    
    Write-Status "SUCCESS" "Test successful!"
    Write-Status "INFO" "Response: $($testResponse.choices[0].message.content)"
} catch {
    Write-Status "ERROR" "Test failed: $($_.Exception.Message)"
    exit 1
}

# Final summary
Write-Host ""
Write-Host "🎉 Azure Fine-tuning Deployment Completed!" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "📊 Model: $ModelName" -ForegroundColor White
Write-Host "🚀 Deployment: $DeploymentName" -ForegroundColor White
Write-Host "🌐 Endpoint: $openaiEndpoint" -ForegroundColor White
Write-Host "📁 Resource Group: $ResourceGroup" -ForegroundColor White

Write-Host ""
Write-Host "📋 Next Steps:" -ForegroundColor Yellow
Write-Host "1. Monitor model performance" -ForegroundColor White
Write-Host "2. Set up logging and alerts" -ForegroundColor White
Write-Host "3. Implement user feedback collection" -ForegroundColor White
Write-Host "4. Plan for model retraining" -ForegroundColor White

Write-Host ""
Write-Host "🔗 Useful Commands:" -ForegroundColor Yellow
Write-Host "az cognitiveservices account show --name $OpenAIResourceName --resource-group $ResourceGroup" -ForegroundColor White
Write-Host "az cognitiveservices account deployment list --name $OpenAIResourceName --resource-group $ResourceGroup" -ForegroundColor White
