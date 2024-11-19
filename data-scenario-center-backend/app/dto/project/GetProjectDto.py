from app.dto.CamelModel import CamelModel

class GetProjectDto(CamelModel):
    id: int
    name: str
    description: str = "No description available."
    conda_environment: str
    target_state: str  # "running" 또는 "stopped" 값
    current_state: str # "running" 또는 "stopped" 값