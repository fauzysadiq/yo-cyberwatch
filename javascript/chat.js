const apiKey = ''; 
const modelEndpoint = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key=YOUR_API_KEY'; 

const generationConfig = {
    temperature: 1,
    topP: 0.95,
    topK: 64,
    maxOutputTokens: 8192,
    responseMimeType: 'text/plain',
};

async function run() {
    const chatSession = await startChatSession();
    await sendMessageAndStreamResponse(chatSession, 'INSERT_INPUT_HERE');
}

async function startChatSession() {
    const response = await fetch(modelEndpoint, {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${apiKey}`,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            generationConfig: generationConfig,
            history: []
        })
    });
    if (!response.ok) {
        throw new Error(`Error starting chat session: ${response.statusText}`);
    }
    return response.json(); 
}

async function sendMessageAndStreamResponse(chatSession, message) {
    const response = await fetch(`${modelEndpoint}/${chatSession.id}/message`, {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${apiKey}`,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            text: message
        })
    });

    if (!response.ok) {
        throw new Error(`Error sending message: ${response.statusText}`);
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let result = '';

    while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        result += decoder.decode(value, { stream: true });
        console.log(result); 
    }

    console.log('Complete response:', result); 
}

// run().catch(error => console.error('Error:', error));
