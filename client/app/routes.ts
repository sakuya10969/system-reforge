import { type RouteConfig, index, route } from "@react-router/dev/routes";

export default [
  index("routes/home.tsx"),
  route("projects", "pages/projects/ui.tsx"),
  route("projects/:projectId/upload", "pages/upload/ui.tsx"),
  route("projects/:projectId/analysis", "pages/analysis/ui.tsx"),
  route("jobs/:jobId/dependencies", "pages/dependencies/ui.tsx"),
] satisfies RouteConfig;
