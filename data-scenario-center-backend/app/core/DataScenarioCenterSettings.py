from pydantic_settings import BaseSettings


class DataScenarioCenterSettings:
    def __init__(self):
        self.projects_path: str = ".\\projects"
