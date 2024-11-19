// src/pages/projects/show.tsx
import React from "react";
import {
  Show,
  TagField,
} from "@refinedev/antd";
import { Button, Typography } from "antd";
import { useNavigation, useShow } from "@refinedev/core";
const { Title, Text } = Typography;

interface IProject {
  id: number;
  name: string;
  description: string;
  condaEnvironment: string;
  targetState: string;
  currentState: string;
}

export const ProjectShow: React.FC = () => {
  const { queryResult } = useShow<IProject>({
    resource: "projects",
  });
  const { data, isLoading } = queryResult;
  const record = data?.data;

  const { list } = useNavigation();

  return (
    <Show
      isLoading={isLoading}
      title="프로젝트 상세 정보"
      headerButtons={() => (
        <Button onClick={() => list("projects")}>뒤로가기</Button>
      )}
    >
      <Title level={5}>ID</Title>
      <Text>{record?.id}</Text>

      <Title level={5}>이름</Title>
      <Text>{record?.name}</Text>

      <Title level={5}>설명</Title>
      <Text>{record?.description}</Text>

      <Title level={5}>Conda 환경</Title>
      <Text>{record?.condaEnvironment}</Text>

      <Title level={5}>목표 상태</Title>
      <TagField value={record?.targetState} />

      <Title level={5}>현재 상태</Title>
      <TagField value={record?.currentState} />
    </Show>
  );
};
