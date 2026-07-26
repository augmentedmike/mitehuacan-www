const json = (data, status = 200) =>
  new Response(JSON.stringify(data), {
    status,
    headers: { "Content-Type": "application/json", "Cache-Control": "public, max-age=60", "X-Robots-Tag": "noindex" },
  });

export async function onRequestGet({ env }) {
  try {
    const { results } = await env.DB.prepare("SELECT slug FROM combi_lines").all();
    const slugs = results.map(r => r.slug);
    return json({ slugs });
  } catch {
    return json({ slugs: [] });
  }
}
