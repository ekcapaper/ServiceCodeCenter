// src/dataProvider.js
import {fetchUtils} from 'react-admin';
import {stringify} from 'query-string';

const apiUrl = 'http://localhost:8000/api/v1';
const httpClient = fetchUtils.fetchJson;

const dataProvider = {
    getList: (resource, params) => {
        const url = `${apiUrl}/${resource}`;
        return httpClient(url).then(({json}) => ({
            data: json.data.map(record => ({id: record.id, ...record})),
            total: json.data.length,
        }));
    },
    getOne: (resource, params) =>
        httpClient(`${apiUrl}/${resource}/${params.id}`).then(({json}) => ({
            data: json.data,
        })),
    getMany: (resource, params) => {
        const query = {
            filter: JSON.stringify({id: params.ids}),
        };
        const url = `${apiUrl}/${resource}?${stringify(query)}`;
        return httpClient(url).then(({json}) => ({
            data: json.data,
        }));
    },
    getManyReference: (resource, params) => {
        const url = `${apiUrl}/${resource}`;
        return httpClient(url).then(({json}) => ({
            data: json.data,
            total: json.data.length,
        }));
    },
    update: (resource, params) =>
        httpClient(`${apiUrl}/${resource}/${params.id}`, {
            method: 'PATCH',
            body: JSON.stringify(params.data),
        }).then(({json}) => ({data: json.data})),
    create: (resource, params) =>
        httpClient(`${apiUrl}/${resource}`, {
            method: 'POST',
            body: JSON.stringify(params.data),
        }).then(({json}) => ({data: {...params.data, id: json.data.id}})),
    delete: (resource, params) =>
        httpClient(`${apiUrl}/${resource}/${params.id}`, {
            method: 'DELETE',
        }).then(({json}) => ({data: json.data})),
};

export default dataProvider;
