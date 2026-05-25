from __future__ import annotations

import json
from typing import Protocol

from app.schemas.models import BadStoryReport, InvestAnalysis
from app.services.prompt_registry import PromptTemplate


class InvestAnalyzer(Protocol):
    model_name: str

    def analyze(self, user_story_text: str, prompt: PromptTemplate) -> InvestAnalysis:
        ...


class ReportGenerator(Protocol):
    model_name: str

    def generate(
        self,
        user_story_text: str,
        analysis: InvestAnalysis,
        prompt: PromptTemplate,
    ) -> BadStoryReport:
        ...


class LangChainInvestAnalyzer:
    def __init__(self, model_name: str, temperature: float = 0.0) -> None:
        try:
            from langchain_openai import ChatOpenAI
        except ImportError as exc:
            raise RuntimeError(
                "langchain-openai is required for the llm backend"
            ) from exc
        self.model_name = model_name
        self._llm = ChatOpenAI(model=model_name, temperature=temperature)

    def analyze(self, user_story_text: str, prompt: PromptTemplate) -> InvestAnalysis:
        structured = self._llm.with_structured_output(InvestAnalysis)
        return structured.invoke(prompt.format(user_story_text=user_story_text))


class LangChainReportGenerator:
    def __init__(self, model_name: str, temperature: float = 0.0) -> None:
        try:
            from langchain_openai import ChatOpenAI
        except ImportError as exc:
            raise RuntimeError(
                "langchain-openai is required for the llm backend"
            ) from exc
        self.model_name = model_name
        self._llm = ChatOpenAI(model=model_name, temperature=temperature)

    def generate(
        self,
        user_story_text: str,
        analysis: InvestAnalysis,
        prompt: PromptTemplate,
    ) -> BadStoryReport:
        structured = self._llm.with_structured_output(BadStoryReport)
        return structured.invoke(
            prompt.format(
                user_story_text=user_story_text,
                invest_analysis_json=json.dumps(
                    analysis.model_dump(),
                    ensure_ascii=False,
                    sort_keys=True,
                ),
            )
        )

