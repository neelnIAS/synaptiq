import Link from "next/link";
import LogoutButton from "@/components/LogoutButton";

export default function WorkspaceLayout({ children }: { children: React.ReactNode }) {
  return (
    <>
      <nav>
        <b>Synaptiq</b>
        <Link href="/dashboard">Dashboard</Link>
        <Link href="/projects">Projects</Link>
        <Link href="/tasks">Tasks</Link>
        <Link href="/team">Team</Link>
        <Link href="/documents">Documents</Link>
        <LogoutButton />
      </nav>
      {children}
    </>
  );
}