from app.dto.CamelModel import CamelModel

class CreateProjectDto(CamelModel):
    name: str
    description: str = "No description available."
    conda_environment: str