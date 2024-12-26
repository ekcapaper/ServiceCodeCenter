// src/App.js
import * as React from 'react';
import {Admin, Resource} from 'react-admin';
import dataProvider from './dataProvider';
import ProjectList from './components/ProjectList.jsx';
import ProjectCreate from './components/ProjectCreate.jsx';
import ProjectEdit from './components/ProjectEdit.jsx';
import ProjectShow from './components/ProjectShow.jsx';

function App() {
    return (
        <Admin dataProvider={dataProvider}>
            <Resource
                name="projects"
                list={ProjectList}
                create={ProjectCreate}
                edit={ProjectEdit}
                show={ProjectShow}
            />
        </Admin>
    );
}

export default App;
