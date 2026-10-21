import { cn } from "@/lib/utils";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import type { User } from "@/types/user";

type UserAvatarProps = {
  user: Pick<User, "firstName" | "lastName" | "name" | "image">;
  alt?: string;
  fallbackClassName?: string;
} & React.ComponentProps<typeof Avatar>;

function getUserInitials({ firstName, lastName, name }: UserAvatarProps["user"]): string {
  const safeFirstName = firstName?.trim();
  const safeLastName = lastName?.trim();

  const initialsFromNames = [safeFirstName, safeLastName]
    .filter(Boolean)
    .map((value) => value.charAt(0))
    .join("");

  if (initialsFromNames) {
    return initialsFromNames.slice(0, 2).toUpperCase();
  }

  const nameParts = name?.trim().split(/\s+/).filter(Boolean);

  if (nameParts && nameParts.length > 0) {
    const initials = nameParts
      .map((part) => part.charAt(0))
      .join("")
      .slice(0, 2)
      .toUpperCase();

    if (initials) {
      return initials;
    }
  }

  const fallbackInitial = name?.trim().charAt(0);

  if (fallbackInitial) {
    return fallbackInitial.toUpperCase();
  }

  return "?";
}

export function UserAvatar({ user, className, fallbackClassName, alt, ...props }: UserAvatarProps) {
  const initials = getUserInitials(user);

  return (
    <Avatar className={className} {...props}>
      <AvatarImage src={user.image ?? undefined} alt={alt ?? user.name} />
      <AvatarFallback className={cn("text-sm font-semibold uppercase", fallbackClassName)}>
        {initials}
      </AvatarFallback>
    </Avatar>
  );
}
