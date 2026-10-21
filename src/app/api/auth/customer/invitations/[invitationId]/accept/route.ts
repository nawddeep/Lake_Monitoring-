import { AcceptCustomerInvitationValidator } from "./validator";
import {
  AcceptCustomerInvitationError,
  acceptCustomerInvitation,
} from "@/services/customer/invitationService";
import { conflictResponse, createdResponse, validationErrorResponse } from "@/app/api/response";
import { withErrorHandler } from "@/app/api/with-error-handler";

export const POST = withErrorHandler(async (request, context) => {
  const { invitationId } = await context.params;
  const validator = new AcceptCustomerInvitationValidator(invitationId, await request.json());
  const isValid = await validator.validate();
  if (!isValid) return validationErrorResponse(validator.errors);

  try {
    const { firstName, lastName, email, password, role, organizationId } = validator.data;
    const result = await acceptCustomerInvitation({
      invitationId,
      email,
      password,
      firstName,
      lastName,
      role,
      organizationId,
    });

    return createdResponse(result);
  } catch (error) {
    if (error instanceof AcceptCustomerInvitationError) {
      return conflictResponse(error.message);
    }
    throw error;
  }
});
