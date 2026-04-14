from openclaw_compat import Agent, create_openclaw_client
from tools import fetch_data, analyze_text, alert_authority
from config import MODEL_NAME, OLLAMA_BASE_URL
from prompts import SYSTEM_PROMPT

agent = Agent(
    model=MODEL_NAME,
    base_url=OLLAMA_BASE_URL,
    tools=[fetch_data, analyze_text, alert_authority],
    system_prompt=SYSTEM_PROMPT
)

def run():
    # Optional: initialize OpenClaw (CMDOP) orchestration client.
    # Computation still uses the Ollama-backed Agent.
    try:
        client = create_openclaw_client()
        if client is not None:
            print(f"[openclaw] mode={client.mode} connected={client.is_connected}")
    except Exception as e:
        # Keep agent runnable even if CMDOP/OpenClaw is not configured.
        print(f"[openclaw] disabled: {e}")

    result = agent.run(
        "Scan posts and alert if hate speech is found"
    )
    print(result)


if __name__ == "__main__":
    run()