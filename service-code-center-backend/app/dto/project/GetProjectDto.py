from app.dto.CamelModel import CamelModel

class GetProjectDto(CamelModel):
    id: int
    name: str
    description: str = "No description available."
