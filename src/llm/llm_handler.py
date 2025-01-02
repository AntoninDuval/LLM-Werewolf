from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain


class LangChainHandler:
    def __init__(self, model="gpt-4", api_key=None, local_model_name=None):
        """
        Initialize the LangChainHandler.

        Args:
            model (str): The model to use ("gpt-4" for OpenAI, or local Hugging Face model).
            api_key (str): OpenAI API key (if using OpenAI model).
            local_model_name (str): Local model name for Hugging Face (if using local model).
        """
        if api_key:
            self.llm = ChatOpenAI(model=model, openai_api_key=api_key)
        elif local_model_name:
            from langchain.llms import (
                HuggingFacePipeline,
            )  # Import here only if needed to reduce load time
            from transformers import pipeline

            local_pipeline = pipeline("text-generation", model=local_model_name)
            self.llm = HuggingFacePipeline(pipeline=local_pipeline)
        else:
            raise ValueError("Either `api_key` or `local_model_name` must be provided.")

    def generate_response(self, prompt_template: str, variables: dict) -> str:
        """
        Generate a response using LangChain.

        Args:
            prompt_template (str): The template for the prompt.
            variables (dict): The variables to fill in the prompt.

        Returns:
            str: The generated response.
        """
        prompt = PromptTemplate(
            input_variables=list(variables.keys()), template=prompt_template
        )
        chain = LLMChain(llm=self.llm, prompt=prompt)
        response = chain.run(variables)
        return response
