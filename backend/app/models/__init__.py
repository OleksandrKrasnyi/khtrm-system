"""
Models package initialization
"""

from .assignment import Assignment
from .base import Base
from .employee import Employee
from .route import Route
from .user import User
from .vehicle import Vehicle

# Export all models for easier imports
__all__ = ["Base", "User", "Assignment", "Route", "Employee", "Vehicle"]
