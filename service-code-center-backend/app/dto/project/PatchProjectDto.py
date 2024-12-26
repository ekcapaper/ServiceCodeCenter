from app.dto.CamelModel import CamelModel

class PatchProjectDto(CamelModel):
    target_state: str
