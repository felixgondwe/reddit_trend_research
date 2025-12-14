"""Data storage service for saving and loading analysis results."""
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List
import logging

from app.config import settings
from app.models.domain import AnalysisResult

logger = logging.getLogger(__name__)


class DataStorage:
    """Service for storing and retrieving collected data and analysis results."""
    
    def __init__(self):
        """Initialize data storage."""
        self.reports_dir = Path(settings.reports_dir)
        self.data_dir = Path(settings.data_dir)
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        self.data_dir.mkdir(parents=True, exist_ok=True)
    
    def save_collected_data(
        self,
        subreddit_data: Dict[str, Any],
        filename: Optional[str] = None
    ) -> str:
        """
        Save collected Reddit data to JSON file.
        
        Args:
            subreddit_data: Dictionary with collected data
            filename: Optional custom filename
            
        Returns:
            Path to saved file
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            subreddit = subreddit_data.get("subreddit", "unknown")
            filename = f"{subreddit}_{timestamp}.json"
        
        filepath = self.data_dir / filename
        
        try:
            with open(filepath, 'w') as f:
                json.dump(subreddit_data, f, indent=2, default=str)
            logger.info(f"Saved collected data to {filepath}")
            return str(filepath)
        except Exception as e:
            logger.error(f"Error saving data: {e}")
            raise
    
    def save_analysis_result(
        self,
        analysis_result: AnalysisResult,
        filename: Optional[str] = None
    ) -> str:
        """
        Save analysis result to JSON file.
        
        Args:
            analysis_result: AnalysisResult object
            filename: Optional custom filename
            
        Returns:
            Path to saved file
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"analysis_{timestamp}.json"
        
        filepath = self.reports_dir / filename
        
        try:
            with open(filepath, 'w') as f:
                json.dump(analysis_result.model_dump(), f, indent=2, default=str)
            logger.info(f"Saved analysis result to {filepath}")
            return str(filepath)
        except Exception as e:
            logger.error(f"Error saving analysis: {e}")
            raise
    
    def load_collected_data(self, filename: str) -> Optional[Dict[str, Any]]:
        """
        Load collected data from JSON file.
        
        Args:
            filename: Name of file to load
            
        Returns:
            Dictionary with data or None if not found
        """
        filepath = self.data_dir / filename
        
        if not filepath.exists():
            logger.warning(f"File not found: {filepath}")
            return None
        
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            logger.info(f"Loaded data from {filepath}")
            return data
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            return None
    
    def load_analysis_result(self, filename: str) -> Optional[Dict[str, Any]]:
        """
        Load analysis result from JSON file.
        
        Args:
            filename: Name of file to load
            
        Returns:
            Dictionary with analysis or None if not found
        """
        filepath = self.reports_dir / filename
        
        if not filepath.exists():
            logger.warning(f"File not found: {filepath}")
            return None
        
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            logger.info(f"Loaded analysis from {filepath}")
            return data
        except Exception as e:
            logger.error(f"Error loading analysis: {e}")
            return None
    
    def list_collected_data(self) -> List[str]:
        """List all collected data files."""
        return [f.name for f in self.data_dir.glob("*.json")]
    
    def list_analysis_results(self) -> List[str]:
        """List all analysis result files."""
        return [f.name for f in self.reports_dir.glob("*.json")]
    
    def get_latest_analysis(self) -> Optional[Dict[str, Any]]:
        """Get the most recent analysis result."""
        files = sorted(self.reports_dir.glob("analysis_*.json"), reverse=True)
        if files:
            return self.load_analysis_result(files[0].name)
        return None

