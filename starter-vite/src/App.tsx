import React from "react";
import ReactDOM from "react-dom/client";
import { Refine } from "@refinedev/core";
import { notificationProvider, RefineThemes } from "@refinedev/antd";
import "@refinedev/antd/dist/reset.css";
import { ConfigProvider } from "antd";
import koKR from "antd/locale/ko_KR";
import { BrowserRouter } from "react-router-dom";
import { dataProvider } from "./providers/data-provider";
import { AppRoutes } from "./routes";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
function App() {
  const queryClient = new QueryClient();

  return (
    <QueryClientProvider client={queryClient}>
    <BrowserRouter>
      <ConfigProvider locale={koKR} theme={RefineThemes.Blue}>
        <Refine
          dataProvider={dataProvider}
          notificationProvider={notificationProvider}
          resources={[
            {
              name: "projects",
              list: "/projects",
              create: "/projects/create",
              show: "/projects/show/:id",
              meta: {
                label: "Projects",
              },
            },
          ]}
          options={{ syncWithLocation: true }}
        />
        <AppRoutes />
      </ConfigProvider>
    </BrowserRouter>
    </QueryClientProvider>
  );
}

export default App;
