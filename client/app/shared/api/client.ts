import axios from "axios";

export const apiClient = axios.create({
  baseURL: "/api/v1",
  headers: { "Content-Type": "application/json" },
});

export interface DataResponse<T> {
  data: T;
}

export interface ErrorResponse {
  error: { code: string; message: string };
}

export interface PaginatedResponse<T> {
  data: T[];
  pagination: {
    total: number;
    page: number;
    per_page: number;
  };
}
