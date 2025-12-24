from typing import List, Dict, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class WorkflowMetrics:
    """Metrics for workflow execution."""
    workflow_type: str
    task: str
    start_time: datetime
    end_time: Optional[datetime]
    agents_used: List[str]
    total_tokens: int
    success: bool


class MetricsTracker:
    """Track and analyze workflow metrics."""
    
    def __init__(self):
        self.metrics: List[WorkflowMetrics] = []
    
    def start_workflow(self, workflow_type: str, task: str) -> WorkflowMetrics:
        """Start tracking a new workflow."""
        metric = WorkflowMetrics(
            workflow_type=workflow_type,
            task=task,
            start_time=datetime.now(),
            end_time=None,
            agents_used=[],
            total_tokens=0,
            success=False
        )
        self.metrics.append(metric)
        return metric
    
    def end_workflow(self, metric: WorkflowMetrics, success: bool = True):
        """Complete workflow tracking."""
        metric.end_time = datetime.now()
        metric.success = success
    
    def get_summary(self) -> Dict:
        """Get summary of all tracked workflows."""
        if not self.metrics:
            return {"total": 0, "successful": 0, "failed": 0}
        
        successful = sum(1 for m in self.metrics if m.success)
        failed = len(self.metrics) - successful
        
        avg_duration = sum(
            (m.end_time - m.start_time).total_seconds()
            for m in self.metrics if m.end_time
        ) / len(self.metrics)
        
        return {
            "total": len(self.metrics),
            "successful": successful,
            "failed": failed,
            "avg_duration_seconds": round(avg_duration, 2),
            "workflows_by_type": self._count_by_type()
        }
    
    def _count_by_type(self) -> Dict[str, int]:
        """Count workflows by type."""
        counts = {}
        for metric in self.metrics:
            counts[metric.workflow_type] = counts.get(metric.workflow_type, 0) + 1
        return counts


def format_response(response: str, max_width: int = 80) -> str:
    """
    Format long response text for display.
    
    Args:
        response: The response text to format
        max_width: Maximum line width
        
    Returns:
        Formatted text with word wrapping
    """
    words = response.split()
    lines = []
    current_line = []
    current_length = 0
    
    for word in words:
        if current_length + len(word) + 1 > max_width:
            lines.append(" ".join(current_line))
            current_line = [word]
            current_length = len(word)
        else:
            current_line.append(word)
            current_length += len(word) + 1
    
    if current_line:
        lines.append(" ".join(current_line))
    
    return "\n".join(lines)


def save_result(result: Dict, filename: str):
    """
    Save workflow result to file.
    
    Args:
        result: Result dictionary from workflow
        filename: Output filename
    """
    import json
    from pathlib import Path
    
    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)
    
    filepath = output_dir / filename
    
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    print(f"Result saved to: {filepath}")


def load_result(filename: str) -> Optional[Dict]:
    """
    Load workflow result from file.
    
    Args:
        filename: Input filename
        
    Returns:
        Result dictionary or None if file not found
    """
    import json
    from pathlib import Path
    
    filepath = Path("outputs") / filename
    
    if not filepath.exists():
        print(f"File not found: {filepath}")
        return None
    
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


