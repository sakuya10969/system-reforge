const DEFAULT_API_ORIGIN = "http://localhost:8000";

export const API_ORIGIN =
  import.meta.env.VITE_API_ORIGIN?.replace(/\/$/, "") ?? DEFAULT_API_ORIGIN;

export const API_BASE_URL = `${API_ORIGIN}/api/v1`;
