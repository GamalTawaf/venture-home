import logging
from django.conf import settings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

GOOGLE_API_KEY = settings.GOOGLE_API_KEY
logger = logging.getLogger(__name__)


def ask_venture_question(question, ventures):
    """
    Uses Gemini via LangChain to answer questions about ventures.
    Args:
        question (str): The user's question.
        ventures (list[dict]): List of venture data dicts.
    Returns:
        str: AI-generated answer.
    """
    if not GOOGLE_API_KEY:
        return "Google API key not configured."

    # Prepare context from ventures
    # convert json into toon format which is better for LLMs
    # example: {"name": "Venture 1", "metrics": {"burn_rate_monthly": 1000, "runway_months": 12, "pilot_customers": 100, "nps_score": 85}}
    # toon format:
    # name: Venture 1
    # metrics:
    # burn_rate_monthly: 1000
    # runway_months: 12
    # pilot_customers: 100
    # nps_score: 85
    ventures_context = toons.dumps(ventures)

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are an expert venture analyst. Use the provided venture data to answer user questions accurately and concisely. Always respond with plain text that is clear and readable. Format your response in a conversational, easy-to-understand manner. Do not use markdown, code blocks, or special formatting - just plain text.",
            ),
            (
                "human",
                "Here is the venture data:\n{ventures_context}\n\nQuestion: {question}\n\nPlease provide a clear, readable answer in plain text format.",
            ),
        ]
    )

    llm = ChatGoogleGenerativeAI(
        model="gemini-3-flash-preview",
        google_api_key=GOOGLE_API_KEY,
    )

    chain = prompt | llm

    try:
        result = chain.invoke(
            {"ventures_context": ventures_context, "question": question}
        )

        # Extract content from LangChain AIMessage
        if hasattr(result, "content"):
            content = result.content

            # Handle different content formats
            if isinstance(content, str):
                answer = content
            elif isinstance(content, dict):
                # Handle dict with 'text' key (Gemini response format)
                answer = (
                    content.get("text", "")
                    if isinstance(content.get("text"), str)
                    else str(content)
                )
            elif isinstance(content, list) and len(content) > 0:
                # If content is a list, extract text from each item
                text_parts = []
                for item in content:
                    if isinstance(item, str):
                        text_parts.append(item)
                    elif isinstance(item, dict) and "text" in item:
                        text_parts.append(item["text"])
                    else:
                        text_parts.append(str(item))
                answer = " ".join(text_parts) if text_parts else ""
            else:
                answer = str(content) if content else ""
        else:
            answer = str(result) if result else ""

        # Ensure we always return a non-empty string
        if not answer or not answer.strip():
            answer = "I couldn't generate a response based on the available data. Please try rephrasing your question."

        return answer.strip()
    except Exception as e:
        logger.error(f"Error generating chat response: {str(e)}", exc_info=True)
        return (
            f"I encountered an error while processing your question. Please try again."
        )
