// src/pages/projects/list.tsx
import React from "react";
import {
  List,
  useTable,
  TagField,
  ShowButton,
} from "@refinedev/antd";
import { Table, Space, Switch, Button } from "antd";
import { IResourceComponentsProps, useNavigation, useNotification, useUpdate } from "@refinedev/core";

interface IProject {
  id: number;
  name: string;
  description: string;
  condaEnvironment: string;
  targetState: string;
  currentState: string;
}

export const ProjectList: React.FC<IResourceComponentsProps> = () => {
  const { tableProps } = useTable<IProject>({
    resource: "projects",
  });

  const { edit, show } = useNavigation();
  const { mutate } = useUpdate();
  const { open } = useNotification();

  const handleToggle = (id: number, targetState: string) => {
    mutate(
      {
        resource: "projects",
        id,
        values: { targetState },
        mutationMode: "optimistic",
      },
      {
        onSuccess: () => {
          open?.({
            type: "success",
            message: "프로젝트 상태가 업데이트되었습니다.",
          });
        },
        onError: (error) => {
          open?.({
            type: "error",
            message: "상태 업데이트 중 오류가 발생했습니다.",
            description: error.message,
          });
        },
      }
    );
  };

  return (
    <List
      title="프로젝트 목록"
      headerButtons={() => (
        <Button type="primary" onClick={() => edit("projects", "create")}>
          새 프로젝트
        </Button>
      )}
    >
      <Table {...tableProps} rowKey="id">
        <Table.Column dataIndex="id" title="ID" />
        <Table.Column dataIndex="name" title="이름" sorter />
        <Table.Column dataIndex="description" title="설명" />
        <Table.Column dataIndex="condaEnvironment" title="Conda 환경" />
        <Table.Column
          dataIndex="targetState"
          title="목표 상태"
          render={(value, record: IProject) => (
            <Switch
              checked={value === "running"}
              onChange={(checked) =>
                handleToggle(
                  record.id,
                  checked ? "running" : "stopped"
                )
              }
            />
          )}
        />
        <Table.Column
          dataIndex="currentState"
          title="현재 상태"
          render={(value) => <TagField value={value} />}
        />
        <Table.Column<IProject>
          title="액션"
          render={(_, record) => (
            <Space>
              <ShowButton
                hideText
                size="small"
                recordItemId={record.id.toString()}
              />
            </Space>
          )}
        />
      </Table>
    </List>
  );
};
