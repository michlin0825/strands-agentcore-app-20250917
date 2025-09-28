# Manual Deployment Instructions

## 🚀 Deploying Strands AgentCore App 20250917

Since the automated deployment script requires Docker and specific AWS CLI configurations, here are the manual steps to deploy the new runtime:

### Step 1: Prepare Docker Image

1. **Start Docker Desktop** (if not running)

2. **Build the Docker image**:
   ```bash
   cd /Users/mba/Desktop/strands-agentcore-app-20250917
   docker build -t strands-agentcore-app-20250917 .
   ```

3. **Get ECR login and push image**:
   ```bash
   # Get ECR login token
   aws ecr get-login-password --region us-east-1 --profile CloudChef01 | docker login --username AWS --password-stdin 111735445051.dkr.ecr.us-east-1.amazonaws.com

   # Tag the image
   docker tag strands-agentcore-app-20250917:latest 111735445051.dkr.ecr.us-east-1.amazonaws.com/strands-agentcore-app-20250917:latest

   # Push to ECR
   docker push 111735445051.dkr.ecr.us-east-1.amazonaws.com/strands-agentcore-app-20250917:latest
   ```

### Step 2: Create AgentCore Runtime (AWS Console)

1. **Go to AWS Console** → Bedrock → AgentCore

2. **Create new runtime** with these settings:
   - **Name**: `StrandsAgentCoreApp20250917`
   - **Image URI**: `111735445051.dkr.ecr.us-east-1.amazonaws.com/strands-agentcore-app-20250917:latest`
   - **Environment Variables**:
     - `TAVILY_API_KEY`: `tvly-YOUR_API_KEY_HERE`
     - `BEDROCK_KNOWLEDGE_BASE_ID`: `VVJWR6EQPY`

3. **Wait for deployment** to complete (status: ACTIVE)

4. **Copy the Runtime ARN** (will look like: `arn:aws:bedrock-agentcore:us-east-1:111735445051:runtime/StrandsAgentCoreApp20250917-XXXXX`)

### Step 3: Update Configuration

1. **Update .env file** with the new Runtime ARN:
   ```bash
   # Replace PLACEHOLDER with actual ARN from Step 2
   AGENT_RUNTIME_ARN=arn:aws:bedrock-agentcore:us-east-1:111735445051:runtime/StrandsAgentCoreApp20250917-ACTUAL_SUFFIX
   ```

### Step 4: Delete Old Runtime (Optional)

1. **In AWS Console** → Bedrock → AgentCore
2. **Find old runtime**: `HelloWorldStrandsAgentV2-R3GAODHoRb`
3. **Delete** the old runtime

### Step 5: Test New Deployment

1. **Test the agent**:
   ```bash
   python test_deployed_agent.py
   ```

2. **Start the Streamlit app**:
   ```bash
   ./start_env_app.sh
   ```

## 🔧 Alternative: Automated Deployment

If Docker is running, you can use the automated script:

```bash
python deploy_agentcore_v2.py
```

## 📝 Configuration Changes

### New Naming Convention:
- **Runtime Name**: `StrandsAgentCoreApp20250917` (reflects project folder)
- **ECR Repository**: `strands-agentcore-app-20250917`
- **Environment Variables**: Updated in `.env` and `.env.example`

### Old vs New:
- **Old ARN**: `arn:aws:bedrock-agentcore:us-east-1:111735445051:runtime/HelloWorldStrandsAgentV2-R3GAODHoRb`
- **New ARN**: `arn:aws:bedrock-agentcore:us-east-1:111735445051:runtime/StrandsAgentCoreApp20250917-XXXXX`

## ✅ Verification

After deployment, verify:
1. ✅ New runtime is ACTIVE in AWS Console
2. ✅ Old runtime is deleted (optional)
3. ✅ `.env` file has correct new ARN
4. ✅ Test script passes: `python test_deployed_agent.py`
5. ✅ Streamlit app works: `./start_env_app.sh`
