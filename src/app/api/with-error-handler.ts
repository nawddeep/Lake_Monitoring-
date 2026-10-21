import { ZodError } from "zod";
import { mapZodErrors } from "@/validators/BaseValidator";
import { validationErrorResponse } from "@/app/api/response";

type RouteHandler = (
  request: Request,
  context: { params: Promise<Record<string, string>> },
) => Promise<Response>;

export function withErrorHandler(handler: RouteHandler): RouteHandler {
  return async (request, context) => {
    try {
      return await handler(request, context);
    } catch (err) {
      if (err instanceof ZodError) {
        return validationErrorResponse(mapZodErrors(err.issues));
      }
      throw err;
    }
  };
}
