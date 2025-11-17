/**
 * AIOS OpenRouter API Test Script
 * Tests the DeepSeek integration via OpenRouter API
 */

const https = require('https');

// Load API key from Windows User PATH environment variable
const API_KEY = process.env.DEEPSEEK_API_KEY;

// Validation
if (!API_KEY) {
    console.error('ERROR: DEEPSEEK_API_KEY not found in environment variables.');
    console.error('Please set it in Windows User Environment Variables:');
    console.error('  1. Press Win+X → System → Advanced → Environment Variables');
    console.error('  2. Under "User variables", click "New..."');
    console.error('  3. Variable name: DEEPSEEK_API_KEY');
    console.error('  4. Variable value: your-regenerated-key');
    console.error('  5. Click OK and restart terminal/VS Code');
    process.exit(1);
}

const API_URL = "https://openrouter.ai/api/v1/chat/completions";

async function testOpenRouterConnection() {
    console.log('🧪 Testing AIOS OpenRouter DeepSeek Integration...');
    console.log('Key loaded from environment: ' + API_KEY.substring(0, 15) + '...' + API_KEY.substring(API_KEY.length - 10));
    
    const testPayload = {
        model: "deepseek/deepseek-chat",
        messages: [
            {
                role: "system",
                content: "You are AIOS (Artificial Intelligence Operative System), an advanced AI assistant specialized in multi-language development platform architecture."
            },
            {
                role: "user", 
                content: "Hello! Can you briefly explain what AIOS is and confirm you're working properly?"
            }
        ],
        max_tokens: 500,
        temperature: 0.7
    };

    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${API_KEY}`,
                'Content-Type': 'application/json',
                'HTTP-Referer': 'https://aios.dev',
                'X-Title': 'AIOS Development Platform Test'
            },
            body: JSON.stringify(testPayload)
        });

        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(`API Error ${response.status}: ${errorText}`);
        }

        const result = await response.json();
        
        console.log('✅ OpenRouter API Connection Successful!');
        console.log('📊 Response Details:');
        console.log(`   Model: ${result.model}`);
        console.log(`   Tokens Used: ${result.usage?.total_tokens || 'Unknown'}`);
        console.log('🤖 AI Response:');
        console.log(result.choices[0].message.content);
        
        return true;

    } catch (error) {
        console.error('❌ OpenRouter API Test Failed:', error.message);
        return false;
    }
}

// Run the test
testOpenRouterConnection().then(success => {
    if (success) {
        console.log('\n🎉 AIOS Real AI Integration is ready!');
        console.log('💡 Try these commands in VS Code:');
        console.log('   @aios analyze AIOS architecture');
        console.log('   @aios help me with Python development');
        console.log('   @aios explain consciousness crystal framework');
    } else {
        console.log('\n⚠️  Integration test failed. Check API key and network connection.');
    }
});