import { EmailMessage } from "cloudflare:email";

const FROM = "contact@millillion.org";
const TO = "jordan.michael.last@gmail.com";
const back = (q) => Response.redirect(`https://millillion.org/contact/?${q}`, 303);
// Event news sign-ups come from the meetup page or the dedicated /meetup/signup/ page; send people back where they were.
const backEvents = (form, q) =>
  form.get("back") === "/meetup/signup/"
    ? Response.redirect(`https://millillion.org/meetup/signup/?${q}`, 303)
    : Response.redirect(`https://millillion.org/meetup/?${q}#event-news`, 303);
const clean = (s, n) => String(s || "").replace(/\r/g, "").trim().slice(0, n);
const header = (s) => clean(s, 200).replace(/[\n"<>]/g, " ");
const isEmail = (s) => /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(s);

const mail = (env, subject, replyTo, lines) =>
  env.MAIL.send(
    new EmailMessage(
      FROM,
      TO,
      [
        `From: Millillion website <${FROM}>`,
        `To: ${TO}`,
        `Reply-To: ${replyTo}`,
        `Subject: ${subject}`,
        `Message-ID: <${crypto.randomUUID()}@millillion.org>`,
        `Date: ${new Date().toUTCString()}`,
        "MIME-Version: 1.0",
        'Content-Type: text/plain; charset="utf-8"',
        "Content-Transfer-Encoding: 8bit",
        "",
        ...lines,
        "",
      ].join("\r\n"),
    ),
  );

async function contact(form, env) {
  if (clean(form.get("company"), 100)) return back("sent=1"); // honeypot: bots fill hidden fields
  const name = header(form.get("name"));
  const email = header(form.get("email"));
  const message = clean(form.get("message"), 5000);
  if (!name || !isEmail(email) || message.length < 2) return back("error=1");
  if ((message.match(/https?:\/\//g) || []).length > 3) return back("error=1");
  try {
    await mail(env, `Website message from ${name}`, `"${name}" <${email}>`, [`Name: ${name}`, `Email: ${email}`, "", message]);
  } catch (e) {
    return back("error=1");
  }
  return back("sent=1");
}

// Millillion event news sign-up: one KV entry per email address (signing up again just updates it).
async function events(form, env) {
  if (clean(form.get("company"), 100)) return backEvents(form, "joined=1"); // honeypot
  const name = header(form.get("name"));
  const email = header(form.get("email")).toLowerCase();
  if (!name || !isEmail(email)) return backEvents(form, "error=1");
  const entry = { name, email, source: clean(form.get("source"), 100) || "website", at: new Date().toISOString() };
  try {
    await env.EVENTS.put(email, JSON.stringify(entry));
  } catch (e) {
    return backEvents(form, "error=1");
  }
  try {
    await mail(env, `Event news sign-up: ${name}`, `"${name}" <${email}>`, [`Name: ${name}`, `Email: ${email}`, `Source: ${entry.source}`]);
  } catch (e) {
    // The sign-up is already saved; the notification email is a convenience.
  }
  return backEvents(form, "joined=1");
}

export default {
  async fetch(request, env) {
    if (request.method !== "POST") return new Response("Method not allowed", { status: 405 });
    const form = await request.formData();
    return new URL(request.url).pathname === "/api/events" ? events(form, env) : contact(form, env);
  },
};
