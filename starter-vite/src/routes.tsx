// src/routes.tsx
import React from "react";
import { Navigate, useRoutes } from "react-router-dom";
import { ProjectList } from "./pages/projects/list";
import { ProjectCreate } from "./pages/projects/create";
import { ProjectShow } from "./pages/projects/show";

export const AppRoutes = () => {
  const element = useRoutes([
    {
      path: "/projects",
      element: <ProjectList />,
    },
    {
      path: "/projects/create",
      element: <ProjectCreate />,
    },
    {
      path: "/projects/show/:id",
      element: <ProjectShow />,
    },
    {
      path: "/",
      element: <Navigate to="/projects" />,
    },
  ]);

  return element;
};
