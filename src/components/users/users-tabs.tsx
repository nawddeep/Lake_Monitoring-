type User = {
  id: string;
  firstName?: string | null;
  lastName?: string | null;
  name: string;
  email: string;
  role?: string | null;
  createdAt: Date;
  members: { organization: { id: string; name: string } }[];
};

export function UsersTabs({ users }: { users: User[] }) {
  return (
    <div className="mt-6">
      {users.length === 0 ? (
        <p className="text-sm text-muted-foreground">No users yet.</p>
      ) : (
        <div className="overflow-hidden rounded-lg border">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b bg-muted/50 text-left text-xs font-medium uppercase tracking-wider text-muted-foreground">
                <th className="px-4 py-3">First name</th>
                <th className="px-4 py-3">Last name</th>
                <th className="px-4 py-3">Email</th>
                <th className="px-4 py-3">Organizations</th>
                <th className="px-4 py-3">Role</th>
                <th className="px-4 py-3">Joined</th>
              </tr>
            </thead>
            <tbody className="divide-y">
              {users.map((user) => (
                <tr key={user.id} className="hover:bg-muted/30">
                  <td className="px-4 py-3 font-medium">{user.firstName ?? user.name}</td>
                  <td className="px-4 py-3">{user.lastName ?? "—"}</td>
                  <td className="px-4 py-3 text-muted-foreground">{user.email}</td>
                  <td className="px-4 py-3">
                    {user.members.length === 0 ? (
                      <span className="text-muted-foreground">—</span>
                    ) : (
                      <div className="flex flex-wrap gap-1">
                        {user.members.map(({ organization }) => (
                          <span
                            key={organization.id}
                            className="inline-flex items-center rounded-md bg-muted px-2 py-0.5 text-xs font-medium text-muted-foreground"
                          >
                            {organization.name}
                          </span>
                        ))}
                      </div>
                    )}
                  </td>
                  <td className="px-4 py-3 capitalize text-muted-foreground">{user.role ?? "—"}</td>
                  <td className="px-4 py-3 text-muted-foreground">
                    {user.createdAt.toLocaleDateString()}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
