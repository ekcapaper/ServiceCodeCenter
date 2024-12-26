// src/components/ProjectCreate.jsx
import * as React from 'react';
import {Create, SimpleForm, TextInput} from 'react-admin';

const ProjectCreate = () => (
    <Create>
        <SimpleForm>
            <TextInput source="name"/>
            <TextInput source="description"/>
            <TextInput source="condaEnvironment"/>
        </SimpleForm>
    </Create>
);

export default ProjectCreate;
