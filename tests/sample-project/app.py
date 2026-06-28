import anthropic

client = anthropic.Anthropic()

# An intentionally weak prompt for the scanner to improve.
SYSTEM = "you are a bot. answer questions. dont make mistakes."

def ask(question: str) -> str:
    msg = client.messages.create(
        model="claude-opus-4-8",
        max_tokens=512,
        system=SYSTEM,
        messages=[{"role": "user", "content": question}],
    )
    return msg.content[0].text
