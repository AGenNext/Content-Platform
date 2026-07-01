async function getHealth() {
  const base = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8080';
  try {
    const res = await fetch(`${base}/health`, { cache: 'no-store' });
    return await res.json();
  } catch {
    return { status: 'offline' };
  }
}

export default async function Page() {
  const health = await getHealth();
  return (
    <main style={{ padding: 32, background: '#f8fafc', minHeight: '100vh' }}>
      <section style={{ maxWidth: 1000, margin: '0 auto' }}>
        <p style={{ color: '#2563eb', fontWeight: 700 }}>AGenNext</p>
        <h1 style={{ fontSize: 44, margin: '8px 0' }}>Content Platform</h1>
        <p style={{ fontSize: 18, color: '#475569' }}>
          Release-ready alpha for AI-assisted authoring, workflow approvals, and multi-channel publishing.
        </p>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 16, marginTop: 32 }}>
          {['Content API', 'Camunda Workflow', 'Langflow AI', 'n8n Workers', 'Connector Runtime', 'Analytics'].map((item) => (
            <div key={item} style={{ background: 'white', padding: 20, borderRadius: 16, border: '1px solid #e2e8f0' }}>
              <strong>{item}</strong>
              <p style={{ color: '#64748b' }}>Alpha module ready for implementation.</p>
            </div>
          ))}
        </div>
        <pre style={{ marginTop: 32, padding: 16, background: '#0f172a', color: '#e2e8f0', borderRadius: 12 }}>
{JSON.stringify(health, null, 2)}
        </pre>
      </section>
    </main>
  );
}
