"""
prompt_builder.py - Builds the LLM prompt for the AI Advisor tab.
Separated to avoid special-token issues in the main file.
"""


def build_ai_prompt(user_question: str, language: str) -> str:
    """Return a chat-formatted prompt asking the model to reply in *language*."""
    system_part = (
        "You are a helpful Indian Agriculture Expert. "
        "Give a short, practical answer in 3 sentences. "
        f"Answer in {language}."
    )
    # TinyLlama chat template tokens
    SYS = "<" + "|system|" + ">"
    USR = "<" + "|user|" + ">"
    AST = "<" + "|assistant|" + ">"
    return f"{SYS}\n{system_part}\n{USR}\n{user_question}\n{AST}\n"
