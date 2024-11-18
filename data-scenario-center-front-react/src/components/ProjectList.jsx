// src/components/ProjectList.js
import * as React from 'react';
import {Datagrid, FunctionField, List, useDataProvider, useRefresh} from 'react-admin';
import {Switch} from '@mui/material';

const ProjectList = () => {
    const refresh = useRefresh();
    const dataProvider = useDataProvider();

    return (
        <List>
            <Datagrid rowClick={() => {
            }}> {/* 모든 클릭 동작을 비활성화 */}
                <FunctionField
                    label="ID"
                    render={record => <span>{record.id}</span>}
                />
                <FunctionField
                    label="Name"
                    render={record => <span>{record.name}</span>}
                />
                <FunctionField
                    label="Description"
                    render={record => <span>{record.description}</span>}
                />
                <FunctionField
                    label="Conda Environment"
                    render={record => <span>{record.condaEnvironment}</span>}
                />

                {/* 토글 버튼 필드 */}
                <FunctionField
                    label="Target State"
                    render={record => (
                        <Switch
                            checked={record.targetState === 'running'}
                            onChange={async () => {
                                const newState = record.targetState === 'running' ? 'stopped' : 'running';
                                await dataProvider.update('projects', {
                                    id: record.id,
                                    data: {targetState: newState},
                                    previousData: record,
                                });
                                refresh(); // 상태 변경 후 새로고침하여 UI 업데이트
                            }}
                        />
                    )}
                />

                <FunctionField
                    label="Current State"
                    render={record => <span>{record.currentState}</span>}
                />
            </Datagrid>
        </List>
    );
};

export default ProjectList;
