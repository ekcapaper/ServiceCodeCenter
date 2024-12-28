
import yaml

def stop_project():
    # YAML 파일 불러오기
    with open('project.yaml', 'r') as file:
        data = yaml.safe_load(file)

    # target-state 변경
    data['project']['target-state'] = 'stopped'

    # 변경된 내용을 YAML 파일에 저장
    with open('project.yaml', 'w') as file:
        yaml.dump(data, file, default_flow_style=False)