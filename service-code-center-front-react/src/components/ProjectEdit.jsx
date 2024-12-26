// src/components/ProjectEdit.jsx
import * as React from 'react';
import {Edit, SimpleForm, TextInput} from 'react-admin';

const ProjectEdit = () => (
    <Edit>
        <SimpleForm>
            <TextInput source="name"/>
            <TextInput source="description"/>
            <TextInput source="condaEnvironment"/>
            <TextInput source="targetState"/>
        </SimpleForm>
    </Edit>
);

export default ProjectEdit;
