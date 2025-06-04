import uuid
import os
import sys
import colorama
from langchain.prompts import MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI 
from langchain.prompts import ChatPromptTemplate
from langchain_mongodb import MongoDBChatMessageHistory

def main():
    colorama.init()
    # sanitize LLM endpoint, ensuring we don't append '/v1' twice
    llm_url = os.environ.get('url', 'http://localhost:1234').strip().rstrip('/')
    if llm_url.endswith('/v1'):
        base_url = llm_url
    else:
        base_url = f"{llm_url}/v1"
    llm_model = os.environ.get('model', 'meta-llama-3.1-8b-instruct').strip()
    mongo_url = os.environ.get('mongo', 'mongodb://localhost:27017').strip()
    api_key = os.environ.get('OPENAI_API_KEY', 'dummy').strip()
    session_id = str(uuid.uuid4())
    
    if len(sys.argv) > 1:
        try:
            arg = str(sys.argv[1]).strip()
            session_id = str(uuid.UUID(arg))
        except ValueError:
            pass

    print(f"{colorama.Style.BRIGHT}{colorama.Fore.YELLOW}Session:{colorama.Style.RESET_ALL} {session_id}")
    print()

    # llm
    llm = ChatOpenAI(base_url=base_url, model=llm_model, api_key=api_key)

    # history
    history = MongoDBChatMessageHistory(
        connection_string=mongo_url, 
        database_name='localai_experiments', 
        collection_name='chat_history', 
        session_id=session_id,
        create_index=True
    )

    # prompt
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant who answers in an assertive yet enthusiastic tone who believes in what they are saying. Assertive doesn't mean rude."),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}")
    ])

    chain = prompt_template | llm

    # memory
    memory_chain = RunnableWithMessageHistory(
        chain,
        get_session_history=lambda _: history,
        input_messages_key="input",
        history_messages_key="history"
    )
    
    def get_user_input():
        prompt = colorama.Style.BRIGHT + colorama.Fore.GREEN + "You: " + colorama.Style.RESET_ALL
        
        while True:
            you = input(prompt)
            print()
            
            if you.lower() == "clear":
                os.system('clear')
                
                continue
            
            return you
    
    while True:
        try:
            you = get_user_input()
            
            print(colorama.Style.BRIGHT + colorama.Fore.BLUE + "AI: " + colorama.Style.RESET_ALL, end="", flush=True)
            
            config = {
                "configurable": {
                    "session_id": session_id
                }
            }
            
            # typewriter output
            for m in memory_chain.stream({"input": you}, config=config):
                print(m.content, end="", flush=True)

            print()
        except KeyboardInterrupt:
            sys.exit(0)
        except Exception as exp:
            print(f"{colorama.Style.BRIGHT}{colorama.Fore.RED}{exp}", end="", flush=True)
            
            sys.exit(1)
        finally:
            print(colorama.Style.RESET_ALL)
            

if __name__ == "__main__":
    main()
