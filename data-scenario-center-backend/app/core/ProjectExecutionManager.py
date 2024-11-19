import threading

from app.core.ProjectInfoManager import ProjectInfoManager, project_info_manager_instance
import signal
import subprocess
import pathlib

from app.exceptions.AlreadyStartedException import AlreadyStartedException


class DataScenarioExecutor(threading.Thread):
    def __init__(self, data_scenario):
        super().__init__()
        self.__data_scenario = data_scenario
        self.__is_running = False
        self.__is_started = False
        self.__popen_instance = None
        self.__uid = None

    def run(self):
        script_path = self.__data_scenario["script_path"]
        command = f"conda run -n {self.__data_scenario["conda_environment"]} python {str(script_path.resolve())}"
        #command = f"python {str(script_path.resolve())}"
        #print(script_path)
        #print(command)

        self.__popen_instance = subprocess.Popen(command, shell=True)
        self.__is_running = True
        self.__is_started = True
        self.__uid = self.__popen_instance.pid
        self.__popen_instance.wait()

        # 프로세스가 완료될 때까지 기다리고 결과를 받음
        stdout, stderr = self.__popen_instance.communicate()

        # 종료 코드 확인
        return_code = self.__popen_instance.returncode

        #print(f"표준 출력: {stdout}")
        #print(f"표준 에러: {stderr}")
        #print(f"종료 코드: {return_code}")

    def stop(self):
        self.request_stop()

    def request_stop(self):
        self.__popen_instance.terminate()

    def stop_force(self):
        self.__popen_instance.kill()

    @property
    def is_running(self):
        if self.__popen_instance is None:
            self.__is_running = False
        elif self.__popen_instance.poll() is not None:
            self.__is_running = False
        return self.__is_running

    @property
    def uid_str(self):
        return str(self.__uid)

    @property
    def data_scenario(self):
        return self.__data_scenario

    @property
    def is_started(self):
        return self.__is_started



class ProjectExecutionManager:
    def __init__(self, project_info_manager: ProjectInfoManager):
        self.project_executions = {}
        self.project_info_manager = project_info_manager

    def start_project(self, id_):
        """프로젝트를 실행 상태로 전환"""
        if id_ not in self.project_executions.keys():
            data_scenario_executor = DataScenarioExecutor(self.project_info_manager.get_project(id_))
            data_scenario_executor.start()
            self.project_executions[id_] = data_scenario_executor
        else:
            raise AlreadyStartedException()

    def stop_project(self, id_):
        """프로젝트를 정지 상태로 전환"""
        # 10초 대기후 kill 기능 추가 필요
        if id_ in self.project_executions.keys():
            self.project_executions["id"].stop()
            del self.project_executions[id_]

    def get_running_project_id(self):
        return self.project_executions.keys()

    def check_running_project(self, id_):
        if id_ in self.project_executions.keys():
            if self.project_executions[id_].is_running:
                return "running"
        return "stopped"

    def collect_garbage_project_executor(self):
        del_list = []
        for key_data, project_executor in self.project_executions.items():
            if project_executor.is_started and not project_executor.is_running:
                del_list.append(key_data)

        for del_item in del_list:
            del self.project_executions[del_item]

    '''
    def collect_garbage_project_executor(self):
        del_list = []
        for key_data, project_executor in self.project_executions.items():
            if project_executor.is_started and not project_executor.is_running:
                del_list.append(key_data)

        for del_item in del_list:
            del self.project_executions[del_item]
    
    def sync_project_states(self):
        # 현재 상태의 조사
        """목표 상태와 현재 상태를 비교하여 동기화"""
        for project_name, state in self.project_states.items():
            if state["target_state"] != state["current_state"]:
                if state["target_state"] == "running":
                    self.start_project(project_name)
                else:
                    self.stop_project(project_name)
    '''

project_execution_manager_instance = ProjectExecutionManager(project_info_manager_instance)
