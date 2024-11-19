// src/pages/projects/create.tsx
import React from "react";
import {
  Create,
  useForm,
} from "@refinedev/antd";
import { Form, Input, Button } from "antd";
import { useNavigation } from "@refinedev/core";

export const ProjectCreate: React.FC = () => {
  const { formProps, saveButtonProps } = useForm({
    resource: "projects",
  });

  const { list } = useNavigation();

  return (
    <Create
      title="새 프로젝트 생성"
      saveButtonProps={saveButtonProps}
      headerButtons={() => (
        <Button onClick={() => list("projects")}>뒤로가기</Button>
      )}
    >
      <Form {...formProps} layout="vertical">
        <Form.Item
          name="name"
          label="이름"
          rules={[{ required: true, message: "이름을 입력하세요." }]}
        >
          <Input placeholder="프로젝트 이름 입력" />
        </Form.Item>
        <Form.Item name="description" label="설명">
          <Input.TextArea placeholder="프로젝트 설명 입력" rows={4} />
        </Form.Item>
        <Form.Item
          name="condaEnvironment"
          label="Conda 환경"
          rules={[
            { required: true, message: "Conda 환경을 입력하세요." },
          ]}
        >
          <Input placeholder="Conda 환경 입력" />
        </Form.Item>
      </Form>
    </Create>
  );
};
