import type { ListParams } from "@/services/api/listParams";
import type { ApiErrorResponse, ApiSuccessResponse, PaginationData } from "@/app/api/response";

export class ApiError extends Error {
  constructor(
    public status: number,
    public code: string | undefined,
    public apiMessage: string | undefined,
    public details: ApiErrorResponse["error"]["details"],
  ) {
    super(apiMessage ?? code ?? "An unexpected error occurred.");
  }
}

export class ApiClient {
  constructor(private basePath = "/api") {}

  private async request<T>(method: string, path: string, body?: unknown): Promise<T> {
    const res = await fetch(`${this.basePath}${path}`, {
      method,
      headers: body !== undefined ? { "Content-Type": "application/json" } : {},
      body: body !== undefined ? JSON.stringify(body) : undefined,
    });

    if (res.status === 204) return undefined as T;

    const json = await res.json().catch(() => null);

    if (!res.ok) {
      const error = (json as ApiErrorResponse)?.error ?? {};
      throw new ApiError(res.status, error.code, error.message, error.details);
    }

    return (json as ApiSuccessResponse<T>).data;
  }

  get<T>(path: string, params?: Record<string, string | undefined>) {
    if (params) {
      const query = new URLSearchParams(
        Object.fromEntries(Object.entries(params).filter(([, v]) => v != null)) as Record<
          string,
          string
        >,
      ).toString();
      if (query) path = `${path}?${query}`;
    }
    return this.request<T>("GET", path);
  }

  async getPaginated<T>(
    path: string,
    params?: ListParams,
  ): Promise<{ data: T[]; pagination: PaginationData }> {
    if (params) {
      const { search, sort, order, page, perPage, filters } = params;
      const entries: [string, string][] = Object.entries({ search, sort, order, page, perPage })
        .filter(([, v]) => v != null)
        .map(([k, v]) => [k, String(v)]);
      if (filters) {
        for (const [key, value] of Object.entries(filters)) {
          if (Array.isArray(value) && value.length > 0) {
            entries.push([key, value.join(",")]);
          }
        }
      }
      const query = new URLSearchParams(entries).toString();
      if (query) path = `${path}?${query}`;
    }
    const res = await fetch(`${this.basePath}${path}`);
    const json = await res.json().catch(() => null);
    if (!res.ok) {
      const error = (json as ApiErrorResponse)?.error ?? {};
      throw new ApiError(res.status, error.code, error.message, error.details);
    }
    const { data, pagination } = json as ApiSuccessResponse<T[]> & { pagination: PaginationData };
    return { data, pagination };
  }

  post<T>(path: string, body: unknown) {
    return this.request<T>("POST", path, body);
  }

  patch<T>(path: string, body: unknown) {
    return this.request<T>("PATCH", path, body);
  }

  put<T>(path: string, body: unknown) {
    return this.request<T>("PUT", path, body);
  }

  delete(path: string) {
    return this.request<void>("DELETE", path);
  }
}

export const apiClient = new ApiClient();
export const adminApiClient = new ApiClient("/api/admin");
export const customerApiClient = new ApiClient("/api/customer");
