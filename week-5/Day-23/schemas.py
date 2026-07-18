from typing import List
from pydantic import BaseModel, Field


class Fact(BaseModel):
    title: str = Field(..., description="Short title of the fact")
    description: str = Field(..., description="Detailed description of the fact")


class FactExtraction(BaseModel):
    facts: List[Fact]


class SectionSentiment(BaseModel):
    section: str
    sentiment: str
    confidence: float


class SentimentAnalysis(BaseModel):
    sentiments: List[SectionSentiment]


class ExecutiveSummary(BaseModel):
    summary: str
    key_points: List[str]