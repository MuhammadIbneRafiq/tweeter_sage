# tools.py
import os
from crawl4ai import WebCrawler
from crawl4ai.extraction_strategy import LLMExtractionStrategy
from pydantic import BaseModel, Field
from praisonai_tools import BaseTool

class ModelFee(BaseModel):
    tweet_description: str = Field(..., description="Description of the tweet.")
    tweet_id: str = Field(..., description="Unique identifier for the tweet.")
    top_4_posts: list[str] = Field(..., description="List of top 4 posts related to the tweet.")
    username: str = Field(..., description="Username of the person who posted the tweet.")
    tweet_url: str = Field(..., description="URL of the tweet.")

class ModelFeeTool(BaseTool):
    name: str = "ModelFeeTool"
    description: str = "A tool to extract information from tweets about hiring UI/UX designers."

    def _run(self, url: str):
        crawler = WebCrawler()
        crawler.warmup()

        # Get the API token
        api_token = os.getenv('GROQ_API_KEY')
        if not api_token:
            raise ValueError("GROQ_API_KEY environment variable is not set")

        print(f"Using API Token: {api_token}")  # Debugging log

        result = crawler.run(
            url=url,
            word_count_threshold=1,
            extraction_strategy=LLMExtractionStrategy(
                provider="groq/llama3-8b-8192", 
                api_token=api_token, 
                # schema=ModelFee.schema(),
                # extraction_type="schema",
                instruction="""You are an intelligent text extraction and conversion assistant. Your task is to extract structured information 
                        from the given text and convert it into a pure JSON format. The JSON should contain only the structured data extracted from the text, 
                        with no additional commentary, explanations, or extraneous information. 
                        You could encounter cases where you can't find the data of the fields you have to extract or the data will be in a foreign language.
                        Extract the following information from the twitter post that matches the description 'hiring ui/ux designer', 
                        keep in mind the hiring part is important. 
                        keep in mind the information about these fields might not be obvious but try to get them by analyzing the context"""
            ),            
            bypass_cache=True,
        )

        # More detailed logging
        print(f"Extraction Result: {result}")
        if result.error_message:
            print(f"Error Message: {result.error_message}")

        if result.extracted_content is None:
            print("Extracted content is None")

        return result.extracted_content

if __name__ == "__main__":
    # Test the ModelFeeTool
    tool = ModelFeeTool()
    url = "https://www.skool.com/ai-automation-agency-hub-8466?c=ae064b712f48404ca2b74634461c360e&s=newest-cm&fl=&p=1"
    result = tool.run(url)
    print(result)