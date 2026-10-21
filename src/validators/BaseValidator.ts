import { z } from "zod";

export type ValidationError = {
  path: string[];
  message: string;
};

export function mapZodErrors(issues: z.core.$ZodIssue[]): ValidationError[] {
  return issues.map((issue) => ({
    path: issue.path.map(String),
    message: issue.message,
  }));
}

export abstract class BaseValidator<T> {
  public errors: ValidationError[] = [];
  protected validatedData: T | null = null;

  abstract validate(): Promise<boolean>;

  get data(): T {
    if (!this.validatedData) throw new Error("Cannot access data on an invalid request.");
    return this.validatedData;
  }

  protected mapZodErrors(issues: z.core.$ZodIssue[]): void {
    this.errors = mapZodErrors(issues);
  }
}
