/**
 * AIOS OpenRouter API Test Script
 * Tests the DeepSeek integration via OpenRouter API
 */

const https = require('https');

const API_KEY = "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";
const API_URL = "https://openrouter.ai/api/v1/chat/completions";

async function testOpenRouterConnection() {
    console.log('🧪 Testing AIOS OpenRouter DeepSeek Integration...');
    
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