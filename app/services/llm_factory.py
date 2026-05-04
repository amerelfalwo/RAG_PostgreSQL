import logging
from typing import Any, Dict, List, Type, Optional

import instructor
from anthropic import Anthropic
from openai import OpenAI
from pydantic import BaseModel

from app.config.settings import get_settings


class LLMFactory:
    def __init__(self, provider: str):
        self.provider = provider.lower()
        
        try:
            self.settings = getattr(get_settings(), self.provider)
        except AttributeError:
            raise ValueError(
                f"Settings for provider '{self.provider}' not found in config/settings.py. "
                f"Please add {self.provider.capitalize()}Settings to your Settings class."
            )
            
        self.client = self._initialize_client()

    def _initialize_client(self) -> Any:
        client_initializers = {
            "openai": lambda s: instructor.from_openai(
                OpenAI(api_key=s.api_key, base_url=s.base_url)
            ),
            "anthropic": lambda s: instructor.from_anthropic(
                Anthropic(api_key=s.api_key)
            ),
            "llama": lambda s: instructor.from_openai(
                OpenAI(base_url=s.base_url, api_key=s.api_key),
                mode=instructor.Mode.JSON,
            ),
        }

        initializer = client_initializers.get(self.provider)
        if initializer:
            return initializer(self.settings)
        raise ValueError(f"Unsupported LLM provider: {self.provider}")

    def create_completion(
        self, response_model: Type[BaseModel], messages: List[Dict[str, str]], **kwargs
    ) -> Any:
        
        completion_params = {
            "model": kwargs.get("model", self.settings.default_model),
            "temperature": kwargs.get("temperature", self.settings.temperature),
            "max_retries": kwargs.get("max_retries", self.settings.max_retries),
            "response_model": response_model,
            "messages": messages,
        }

        max_tokens = kwargs.get("max_tokens", self.settings.max_tokens)
        
        if max_tokens is not None:
            completion_params["max_tokens"] = max_tokens
        elif self.provider == "anthropic":
            completion_params["max_tokens"] = 1024 

        logging.info(f"Generating completion using {self.provider} ({completion_params['model']})")
        
        return self.client.chat.completions.create(**completion_params)