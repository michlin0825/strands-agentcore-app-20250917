# Update AgentCore Runtime with Concise Prompt

## 🔄 **Runtime Update Required**

The Docker image has been updated with a more concise system prompt. You need to update the AgentCore runtime to use the new image.

### **Updated System Prompt:**
```
You are a helpful AI assistant. Provide concise, accurate, and direct answers. Use tools when needed for current information or specific knowledge. Keep responses brief while maintaining factual accuracy.
```

## 📋 **Manual Update Steps:**

### **Option 1: Update Existing Runtime (Recommended)**
1. **Go to AWS Console** → Bedrock → AgentCore
2. **Find Runtime**: `StrandsAgentCoreApp20250917-I3867LFr4j`
3. **Click "Update"**
4. **Update Container URI** to: `111735445051.dkr.ecr.us-east-1.amazonaws.com/strands-agentcore-app-20250917:latest`
5. **Keep all other settings** the same
6. **Save and wait** for update to complete (5-10 minutes)

### **Option 2: Create New Runtime Version**
1. **Go to AWS Console** → Bedrock → AgentCore
2. **Create new runtime** with same settings but new image
3. **Update `.env` file** with new ARN
4. **Test the deployment**

## ✅ **Verification**

After updating, test the runtime:

```bash
python test_deployed_agent.py
```

You should see more concise responses while maintaining accuracy.

## 🎯 **Expected Changes**

**Before**: Verbose, detailed explanations
**After**: Concise, direct answers that are still factually correct

The agent will now:
- Give shorter, more focused responses
- Maintain factual accuracy
- Use tools when needed for current information
- Avoid unnecessary elaboration
