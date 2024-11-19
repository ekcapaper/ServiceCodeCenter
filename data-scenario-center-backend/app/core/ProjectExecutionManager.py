from app.core.ProjectInfoManager import ProjectInfoManager, project_info_manager_instance


class ProjectExecutionManager:
    def __init__(self, project_info_manager: ProjectInfoManager):
        self.project_executions = {}
        self.project_info_manager = project_info_manager

    def start_project(self, id_):
        """프로젝트를 실행 상태로 전환"""
        # 임시 코드, id에 기반해서 데이터를 가져온 후에 thread 기반 실행 및 정지 코드 추가 필요
        self.project_executions[id_] = "RUNNING"




    def stop_project(self, id_):
        """프로젝트를 정지 상태로 전환"""
        if id_ in self.project_executions:
            del self.project_executions[id_]

    def get_running_project_id(self):
        return self.project_executions.keys()

    def check_running_project(self, id_):
        if id_ in self.project_executions:
            return "running"
        else:
            return "stopped"

    '''
    def sync_project_states(self):
        """목표 상태와 현재 상태를 비교하여 동기화"""
        for project_name, state in self.project_states.items():
            if state["target_state"] != state["current_state"]:
                if state["target_state"] == "running":
                    self.start_project(project_name)
                else:
                    self.stop_project(project_name)
    '''

project_execution_manager_instance = ProjectExecutionManager(project_info_manager_instance)
