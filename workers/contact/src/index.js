import { EmailMessage } from "cloudflare:email";

const FROM = "contact@millillion.org";
const TO = "jordan.michael.last@gmail.com";
const back = (q) => Response.redirect(`https://millillion.org/contact/?${q}`, 303);
const clean = (s, n) => String(s || "").replace(/\r/g, "").trim().slice(0, n);
const header = (s) => clean(s, 200).replace(/[\n"<>]/g, " ");

export default {
  async fetch(request, env) {
    if (request.method !== "POST") return new Response("Method not allowed", { status: 405 });
    const form = await request.formData();
    if (clean(form.get("company"), 100)) return back("sent=1"); // honeypot: bots fill hidden fields
    const name = header(form.get("name"));
    const email = header(form.get("email"));
    const message = clean(form.get("message"), 5000);
    if (!name || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email) || message.length < 2) return back("error=1");
    if ((message.match(/https?:\/\//g) || []).length > 3) return back("error=1");

    const raw = [
      `From: Millillion website <${FROM}>`,
      `To: ${TO}`,
      `Reply-To: "${name}" <${email}>`,
      `Subject: Website message from ${name}`,
      `Message-ID: <${crypto.randomUUID()}@millillion.org>`,
      `Date: ${new Date().toUTCString()}`,
      "MIME-Version: 1.0",
      'Content-Type: text/plain; charset="utf-8"',
      "Content-Transfer-Encoding: 8bit",
      "",
      `Name: ${name}`,
      `Email: ${email}`,
      "",
      message,
      "",
    ].join("\r\n");
    try {
      await env.MAIL.send(new EmailMessage(FROM, TO, raw));
    } catch (e) {
      return back("error=1");
    }
    return back("sent=1");
  },
};
