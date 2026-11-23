import Link from "next/link";
export default function Home() {
  return <><nav><b>Synaptiq</b><Link href="/login">Login</Link><Link href="/signup">Sign up</Link><Link href="/dashboard">Dashboard</Link></nav><main><section className="panel"><h1>Synaptiq Workspace</h1><p>Plan projects, manage tasks, collaborate with your team and use AI-assisted workflows.</p><Link href="/login">Get started →</Link></section></main></>;
}
