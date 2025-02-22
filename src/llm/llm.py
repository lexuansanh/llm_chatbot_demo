from google import genai
from google.genai import types
from langchain_google_genai import ChatGoogleGenerativeAI

from src.config import DEFAULT_SYSTEM_PROMPT, configsetting
from src.utils.logger import logger


class GeminiLlmManager:
    """Singleton class to manage Gemini API keys and provide an LLM instance."""

    _instance = None  # Singleton instance

    def __new__(cls):
        """Ensure only one instance is created (Singleton)."""
        if cls._instance is None:
            cls._instance = super(GeminiLlmManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        """Initialize the key manager only once."""
        if not self._initialized:
            self.llm = None  # Store LLM instance
            self.search_llm = None
            self.api_keys = []
            self.rotation_attempts = 0  # Track key rotations
            self.max_rotations = 10  # Max retries before stopping
            self.load_keys()
            self._initialized = True  # Mark as initialized
            logger.info(f"init done {self.api_keys}, {self._initialized}")

    def load_keys(self):
        """Load API keys from .env file and store in a queue."""
        logger.info(configsetting.LLM_KEY)
        self.api_keys = [key.strip() for key in configsetting.LLM_KEY]
        logger.info(self.api_keys)
        if not self.api_keys:
            raise ValueError("No API keys found in .env file!")

    def reload_queue(self, key):
        """Rebuild the queue from the updated key list."""
        self.api_keys.remove(key)  # Remove from current position
        self.api_keys.append(key)  # Add to end of list

    def get_key(self):
        """Get the next available API key."""
        if not self.api_keys:
            raise ValueError("No available API keys!")
        return self.api_keys[0]

    def report_limit_reached(self, key):
        """Move key to the back of the list immediately (no cooldown)."""
        if key in self.api_keys:
            self.reload_queue(key)  # Reload queue with new order
            self.rotation_attempts += 1
            logger.info(
                f"API key {key} reached limit. Moved to the end of the list. Attempt {self.rotation_attempts}/{self.max_rotations})"
            )

    def update_key(self):
        """Dynamically update the API key for LLM."""
        if self.rotation_attempts >= self.max_rotations:
            raise RuntimeError(
                "🚨 Cannot invoke Gemini API: All keys failed after maximum rotations."
            )

        new_key = self.get_key()
        return new_key

    def get_llm(self):
        """Ensure a single LLM instance is created and updated dynamically."""
        if self.llm is None:
            self.llm = self.create_llm()
        return self.llm

    def get_search_llm(self):
        if self.search_llm is None:
            self.search_llm = self.create_search_llm()
        return self.search_llm

    def create_llm(self):
        """Create a new LLM instance with the latest API key."""
        new_key = self.get_key()
        logger.info(f"apply key {new_key} for main_llm")
        return ChatGoogleGenerativeAI(
            model=configsetting.MODEL_NAME,
            api_key=new_key,
            max_tokens=None,
            timeout=None,
            max_retries=2,
            verbose=True,
        )

    def create_search_llm(self):
        """Create a new LLM instance with the latest API key."""
        new_key = self.get_key()
        logger.info(f"apply key {new_key} for search_llm")
        return genai.Client(api_key=new_key)

    def rotate_llm(self, max_retries=10):
        """Rotate LLM instance when a key reaches its limit."""
        if self.rotation_attempts >= self.max_rotations:
            raise RuntimeError(
                "🚨 Cannot invoke Gemini API: All keys failed after maximum rotations."
            )

        old_key = self.api_keys[0]
        self.report_limit_reached(old_key)  # Move old key to end
        try:
            self.llm = self.create_llm()  # Replace with a new instance
            self.search_llm = self.create_search_llm()
            logger.info("✅ API key rotated successfully.")
        except Exception as e:
            logger.error(f"⚠️ Rotation failed: {e}")

    def invoke(self, messages):
        try:
            self.llm = self.get_llm()
            answer = self.llm.invoke(messages)
            self.rotation_attempts = 0
            return answer
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            llm_manager.rotate_llm()  # Rotate API key and LLM instance
            self.invoke(messages)  # Retry with new key

    def search_internet(self, message):
        try:
            self.search_llm = self.get_search_llm()
            answer = ""
            response = self.search_llm.models.generate_content(
                model=configsetting.MODEL_NAME,
                contents=message,
                config=types.GenerateContentConfig(
                    tools=[types.Tool(google_search=types.GoogleSearchRetrieval)]
                ),
            )
            print(response)
            for each in response.candidates[0].content.parts:
                answer += f"{each.text}\n"
            self.rotation_attempts = 0
            return answer
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            llm_manager.rotate_llm()  # Rotate API key and LLM instance
            self.search_internet(messages)  # Retry with new key

    def bind_tools(self, tools, tool_choice="any"):
        try:
            self.llm = self.get_llm()
            llm_bind_tools = self.llm.bind_tools(tools, tool_choice=tool_choice)
            self.rotation_attempts = 0
            return llm_bind_tools
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            llm_manager.rotate_llm()  # Rotate API key and LLM instance
            self.bind_tools(tools, tool_choice)  # Retry with new key


# Singleton Manager Instance
llm_manager = GeminiLlmManager()


def call_gemini_invoke(prompt):
    return llm_manager.invoke(prompt)


if __name__ == "__main__":
    messages = [
        ("system", DEFAULT_SYSTEM_PROMPT["default"]["parts"]["text"]),
        ("humans", "show me insight"),
    ]
    response = call_gemini_invoke(messages)
    logger.info(response.content)
