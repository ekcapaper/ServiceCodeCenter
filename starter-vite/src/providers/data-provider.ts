import { DataProvider, DeleteOneParams, DeleteOneResponse } from "@refinedev/core";
import axios, { AxiosInstance } from "axios";

const API_URL = "http://your-api-url.com/api/v1";

const axiosInstance: AxiosInstance = axios.create({
  baseURL: API_URL,
});

export const dataProvider: DataProvider = {
  getList: async ({ resource }) => {
    const url = `/${resource}`;

    const response = await axiosInstance.get(url);

    return {
      data: response.data.data,
      total: response.data.data.length,
    };
  },
  getOne: async ({ resource, id }) => {
    const url = `/${resource}/${id}`;

    const response = await axiosInstance.get(url);

    return {
      data: response.data.data,
    };
  },
  create: async ({ resource, variables }) => {
    const url = `/${resource}`;

    const response = await axiosInstance.post(url, variables);

    return {
      data: response.data.data,
    };
  },
  update: async ({ resource, id, variables }) => {
    const url = `/${resource}/${id}`;

    const response = await axiosInstance.patch(url, variables);

    return {
      data: response.data.data,
    };
  },
  /*
  deleteOne<TData, TVariables>(params: DeleteOneParams<TVariables>): Promise<DeleteOneResponse<TData>> {
    return Promise.resolve(undefined);
  },
  getApiUrl(): string {
    return "";
  },
   */
};
