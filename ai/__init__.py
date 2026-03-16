# ai/__init__.py
from .classify import classify_email
from .analyze import summarize_email
from .response import generate_draft
__all__ = ["classify_email", "summarize_email", "generate_draft"]