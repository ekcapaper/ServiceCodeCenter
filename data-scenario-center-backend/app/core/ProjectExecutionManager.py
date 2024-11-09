class ProjectExecutionManager:
    def __init__(self, info_manager: ProjectInfoManager):
        self.info_manager = info_manager
        self.project_states = {}

    def initialize_project_states(self):
        """초기화 시 모든 프로젝트의 상태를 'stopped'으로 설정"""
        for project_name in self.info_manager.projects_info.keys():
            self.project_states[project_name] = {
                "target_state": "stopped",
                "current_state": "stopped"
            }

    def start_project(self, project_name):
        """프로젝트를 실행 상태로 전환"""
        if project_name in self.project_states:
            self.project_states[project_name]["current_state"] = "running"
            print(f"{project_name} started")

    def stop_project(self, project_name):
        """프로젝트를 정지 상태로 전환"""
        if project_name in self.project_states:
            self.project_states[project_name]["current_state"] = "stopped"
            print(f"{project_name} stopped")

    def sync_project_states(self):
        """목표 상태와 현재 상태를 비교하여 동기화"""
        for project_name, state in self.project_states.items():
            if state["target_state"] != state["current_state"]:
                if state["target_state"] == "running":
                    self.start_project(project_name)
                else:
                    self.stop_project(project_name)

    def update_target_state(self, project_name, target_state):
        """목표 상태를 설정하고 동기화"""
        if project_name in self.project_states:
            self.project_states[project_name]["target_state"] = target_state
            self.sync_project_states()