import asyncio
from langchain_core.messages import HumanMessage
from app.agents.graph import voice_graph
from app.voice_out import speak_text
from app.voice_in import listen_to_user

async def run_voice_assistant():
    print("==================================================")
    print("      Nexus Voice Ops Agent: LIVE CONVERSATION    ")
    print("   (Say 'exit', 'quit', or 'bye' to terminate)   ")
    print("==================================================")
    
    # Startup greeting
    greeting = "Nexus voice system is active and listening. How can I assist your operations?"
    print(f"\nNexus: {greeting}")
    await speak_text(greeting)
    
    while True:
        # 1. Listen to user voice via Mic
        user_text = listen_to_user()
        
        if not user_text:
            continue
            
        # Exit condition
        if any(word in user_text.lower() for word in ["exit", "quit", "goodbye", "bye"]):
            farewell = "Shutting down voice operations. Goodbye."
            print(f"\nNexus: {farewell}")
            await speak_text(farewell)
            break
            
        # 2. Process through LangGraph Brain
        result = voice_graph.invoke({
            "messages": [HumanMessage(content=user_text)],
            "voice_output": ""
        })
        
        voice_response = result["voice_output"]
        print(f"\nNexus: {voice_response}")
        
        # 3. Speak the output via Speakers
        await speak_text(voice_response)

if __name__ == "__main__":
    asyncio.run(run_voice_assistant())