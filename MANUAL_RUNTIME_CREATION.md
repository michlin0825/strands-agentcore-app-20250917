# Manual AgentCore Runtime Creation

Since the `bedrock-agentcore-control` CLI service is not available in the current AWS CLI version, you need to create the runtime manually through the AWS Console.

## 🚀 **Step-by-Step Instructions**

### **1. Navigate to AWS Console**
- Go to **AWS Console** → **Bedrock** → **AgentCore**
- Or direct URL: https://console.aws.amazon.com/bedrock/home?region=us-east-1#/agentcore

### **2. Create New Runtime**
Click **"Create Runtime"** and use these **exact parameters**:

#### **Basic Configuration:**
- **Runtime Name**: `StrandsAgentCoreApp20250917`
- **Description**: `Strands AgentCore App deployed with updated naming scheme and environment-based configuration`

#### **Container Configuration:**
- **Container URI**: `111735445051.dkr.ecr.us-east-1.amazonaws.com/strands-agentcore-app-20250917:latest`

#### **Environment Variables:**
Add these two environment variables:
```
TAVILY_API_KEY = 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
BEDROCK_KNOWLEDGE_BASE_ID = VVJWR6EQPY
```

#### **Network Configuration:**
- **Network Mode**: `PUBLIC` (or `VPC` if you prefer private networking)
- **Security Groups**: (if VPC mode) - use default or create appropriate security groups
- **Subnets**: (if VPC mode) - select appropriate subnets

#### **Protocol Configuration:**
- **Server Protocol**: `HTTP` (standard for web applications)

#### **IAM Role:**
- **Role ARN**: Create or use an existing role with these permissions:
  - `AmazonBedrockFullAccess` (or more restrictive permissions)
  - `AmazonEC2ContainerRegistryReadOnly`
  - Trust relationship for `bedrock-agentcore.amazonaws.com`

### **3. Wait for Deployment**
- The runtime creation will take **5-15 minutes**
- Status will change from `CREATING` → `ACTIVE`
- **Do not proceed until status is ACTIVE**

### **4. Copy the Runtime ARN**
Once created, copy the full Runtime ARN. It will look like:
```
arn:aws:bedrock-agentcore:us-east-1:111735445051:runtime/StrandsAgentCoreApp20250917-XXXXX
```

## 🔧 **Alternative: IAM Role Creation**

If you need to create the IAM role, use these settings:

### **Trust Policy:**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "bedrock-agentcore.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

### **Permissions Policy:**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "bedrock:InvokeModel",
        "bedrock:InvokeModelWithResponseStream",
        "bedrock:RetrieveAndGenerate",
        "bedrock:Retrieve"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "ecr:GetAuthorizationToken",
        "ecr:BatchCheckLayerAvailability",
        "ecr:GetDownloadUrlForLayer",
        "ecr:BatchGetImage"
      ],
      "Resource": "*"
    }
  ]
}
```

## ✅ **Verification Steps**

After creating the runtime:

1. **Status Check**: Ensure runtime status is `ACTIVE`
2. **ARN Copy**: Copy the complete Runtime ARN
3. **Update Environment**: Update your `.env` file with the new ARN
4. **Test Connection**: Run the test script to verify connectivity

## 📝 **Next Steps**

Once you have the Runtime ARN:

1. **Update `.env` file**:
   ```bash
   AGENT_RUNTIME_ARN=arn:aws:bedrock-agentcore:us-east-1:111735445051:runtime/StrandsAgentCoreApp20250917-ACTUAL_SUFFIX
   ```

2. **Test the deployment**:
   ```bash
   python test_deployed_agent.py
   ```

3. **Start the Streamlit app**:
   ```bash
   ./start_env_app.sh
   ```

## 🚨 **Important Notes**

- **Container URI**: Must be exactly `111735445051.dkr.ecr.us-east-1.amazonaws.com/strands-agentcore-app-20250917:latest`
- **Environment Variables**: Both `TAVILY_API_KEY` and `BEDROCK_KNOWLEDGE_BASE_ID` are required
- **Runtime Name**: Must be exactly `StrandsAgentCoreApp20250917` (no spaces, hyphens, or special characters)
- **Region**: Must be `us-east-1`

## 🔄 **Old Runtime Cleanup**

After the new runtime is working, you can delete the old runtime:
- **Old Runtime Name**: `HelloWorldStrandsAgentV2-R3GAODHoRb`
- Go to AgentCore console and delete the old runtime

---

**Please create the runtime using these exact parameters and provide me with the actual Runtime ARN once it's created.**
