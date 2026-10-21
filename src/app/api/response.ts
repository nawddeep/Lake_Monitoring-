import type { ValidationError } from "@/validators/BaseValidator";

export interface ApiSuccessResponse<T> {
  success: true;
  data: T;
}

export interface ApiErrorResponse {
  success: false;
  error: {
    code: string;
    message?: string;
    details?: Array<{ path?: string; message?: string }> | null;
  };
}

export type ApiResult<T> = ApiSuccessResponse<T> | ApiErrorResponse;

export interface PaginationInput {
  page: number;
  perPage: number;
  total: number;
}

export interface PaginationData {
  page: number;
  per_page: number;
  total_pages: number;
  total_results: number;
}

export type ListResponse<T> = ApiResult<T[]>;

export type DetailResponse<T> = ApiResult<T>;

export type PaginatedResponse<T> = ApiSuccessResponse<T[]> & {
  pagination: PaginationData;
};

export function listResponse<T>(results: T[]): Response {
  return Response.json({ success: true, data: results } satisfies ListResponse<T>, { status: 200 });
}

export function detailResponse<T>(item: T): Response {
  return Response.json({ success: true, data: item } satisfies DetailResponse<T>, { status: 200 });
}

export function paginatedResponse<T>(
  results: T[],
  { page, perPage, total }: PaginationInput,
): Response {
  const pagination: PaginationData = {
    page,
    per_page: perPage,
    total_pages: Math.ceil(total / perPage),
    total_results: total,
  };
  return Response.json(
    { success: true, data: results, pagination } satisfies PaginatedResponse<T>,
    { status: 200 },
  );
}

export function noContentResponse(): Response {
  return new Response(null, { status: 204 });
}

export function createdResponse<T>(data: T): Response {
  return Response.json({ success: true, data } satisfies ApiSuccessResponse<T>, { status: 201 });
}

export function unauthorizedResponse(message = "Unauthorized."): Response {
  return Response.json(
    { success: false, error: { code: "unauthorized", message } } satisfies ApiErrorResponse,
    { status: 401 },
  );
}

export function forbiddenResponse(message = "Forbidden."): Response {
  return Response.json(
    { success: false, error: { code: "forbidden", message } } satisfies ApiErrorResponse,
    { status: 403 },
  );
}

export function notFoundResponse(message = "Not found."): Response {
  return Response.json(
    { success: false, error: { code: "not_found", message } } satisfies ApiErrorResponse,
    { status: 404 },
  );
}

export function conflictResponse(message: string): Response {
  return Response.json(
    { success: false, error: { code: "conflict", message } } satisfies ApiErrorResponse,
    { status: 409 },
  );
}

export function validationErrorResponse(errors: ValidationError[]): Response {
  return Response.json(
    {
      success: false,
      error: {
        code: "validation_failed",
        message: "One or more fields are invalid.",
        details: errors.map((e) => ({ path: e.path.join("."), message: e.message })),
      },
    } satisfies ApiErrorResponse,
    { status: 400 },
  );
}
