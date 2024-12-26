// src/components/ProjectShow.jsx
import * as React from 'react';
import {Show, SimpleShowLayout, TextField} from 'react-admin';

const ProjectShow = () => (
    <Show>
        <SimpleShowLayout>
            <TextField source="id"/>
            <TextField source="name"/>
            <TextField source="description"/>
            <TextField source="condaEnvironment"/>
            <TextField source="targetState"/>
            <TextField source="currentState"/>
        </SimpleShowLayout>
    </Show>
);

export default ProjectShow;
