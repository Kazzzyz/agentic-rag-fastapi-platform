"""
Pydantic Schemas for API Requests and Responses
================================================
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


# ── System Schemas ──

class HealthResponse(BaseModel):
    status: str = Field(..., examples=["healthy"])
    version: str = Field("1.0.0", examples=["1.0.0"])
    llm_model: str = Field(..., examples=["openrouter/free"])
    stt_provider: str = Field(..., examples=["groq"])
    stt_model: str = Field(..., examples=["whisper-large-v3-turbo"])
    timestamp: str


class StatsResponse(BaseModel):
    collection_name: str
    persist_directory: str
    total_chunks: int
    unique_sources_count: int
    sources: List[str]


# ── Knowledge Base / Ingestion Schemas ──

class IngestPathRequest(BaseModel):
    source: str = Field(
        ...,
        description="Path to a local document file, web URL, or Wikipedia query ('wiki:Topic')",
        examples=["wiki:Machine Learning"],
    )


class IngestBatchRequest(BaseModel):
    sources: List[str] = Field(
        ...,
        description="List of paths, URLs, or wiki queries to ingest",
        examples=[["wiki:Artificial Intelligence", "wiki:Deep Learning"]],
    )


class IngestResponse(BaseModel):
    status: str = Field(..., examples=["success"])
    source: str
    chunks_ingested: int
    message: Optional[str] = None
    extracted_text_length: Optional[int] = None
    ocr_confidence: Optional[float] = None


class BatchIngestResponse(BaseModel):
    total_sources: int
    results: List[IngestResponse]


class DocumentListResponse(BaseModel):
    total_sources: int
    sources: List[str]


class DeleteSourceResponse(BaseModel):
    status: str
    deleted_source: str
    remaining_chunks: int


class ClearResponse(BaseModel):
    status: str
    message: str


# ── Query / RAG Schemas ──

class QueryRequest(BaseModel):
    query: str = Field(..., min_length=1, description="Question for the RAG agents", examples=["What is agentic RAG?"])
    chat_history: Optional[List[Dict[str, str]]] = Field(
        default=None,
        description="Optional prior conversation turns: [{'role': 'user'|'assistant', 'content': '...'}]",
    )
    source_style: Optional[str] = Field(
        default="numbered",
        description="Formatting style for source citations ('numbered', 'bullet', or 'table')",
        examples=["numbered"],
    )
    max_analyst_loops: Optional[int] = Field(
        default=2,
        ge=0,
        le=5,
        description="Maximum follow-up retrieval loops for the Analyst agent",
        examples=[2],
    )


class QueryResponse(BaseModel):
    question: str
    answer: str
    sources: str
    evidence: List[Dict[str, Any]] = Field(default_factory=list)
    analysis: str = ""
    analyst_tool_calls: List[Dict[str, Any]] = Field(default_factory=list)
    answer_tool_calls: List[Dict[str, Any]] = Field(default_factory=list)
    execution_time_seconds: float


# ── Voice Schemas ──

class TranscriptionResponse(BaseModel):
    text: str
    provider: str
    model: str
    language: Optional[str] = None
    duration: Optional[float] = None


class VoiceQueryResponse(BaseModel):
    transcription: TranscriptionResponse
    question: str
    answer: str
    sources: str
    evidence: List[Dict[str, Any]] = Field(default_factory=list)
    analysis: str = ""
    analyst_tool_calls: List[Dict[str, Any]] = Field(default_factory=list)
    answer_tool_calls: List[Dict[str, Any]] = Field(default_factory=list)
    execution_time_seconds: float


# ── Report Schemas ──

class ReportGenerateRequest(BaseModel):
    result: Dict[str, Any] = Field(
        ...,
        description="The query response dict containing question, answer, analysis, sources",
    )
    instructions: Optional[str] = Field(
        default="clean, modern, and professional",
        description="Custom formatting instructions for the Report Generator Agent",
    )
    filename: Optional[str] = Field(
        default=None,
        description="Optional custom filename for the generated PDF",
    )


class ReportGenerateResponse(BaseModel):
    status: str = "success"
    pdf_path: str
    filename: str
    download_url: str
    summary: str
    tool_calls: List[Dict[str, Any]] = Field(default_factory=list)
