---
marp: true
title: "Greeneville AI Meetup: What AI Can Do for You"
description: Thursday, November 12, 2026, Big Spring Room, Greeneville/Greene County Public Library
author: Jordan Last
paginate: true
style: |
  section { font-size: 30px; }
  section.lead { text-align: center; }
  section.lead h1 { font-size: 56px; }
  .qr { width: 260px; }
  .cols { display: flex; gap: 48px; align-items: center; }
  .cols > div { flex: 1; }
  .small { font-size: 22px; color: #555; }
---

<!-- _class: lead -->
<!-- _paginate: false -->

# Greeneville AI Meetup

## What AI Can Do for You

Thursday, November 12, 2026
Big Spring Room, Greeneville/Greene County Public Library

Jordan Last

<!--
Doors at 7:00. Start about 7:05.
-->

---

## Welcome

- I'm Jordan Last. I build software with AI agents every day.
- Tonight is for everyone. Beginners are especially welcome.
- Questions are welcome at any time, not just at the end.
- Please sign up so I can tell you about future meetups.

<div class="cols">
<div>

**Slides:** millillion.org/meetup/slides
**Meetup page:** millillion.org/meetup

</div>
<img class="qr" src="images/qr-slides.svg" alt="QR code for the slides">
</div>

<!--
Point to the sign-up sheet / sign-up QR now.
Quick show of hands: who has used ChatGPT or Claude? Who uses one every week? Who has used an AI agent?
-->

---

## Tonight

| Time | |
|---|---|
| 7:10 | Chatbots, and a live demo |
| 7:30 | AI agents, and a live demo |
| 8:00 | Agents in every kind of knowledge work |
| 8:05 | How I check AI's work, and what I've built with it |
| 8:35 | Q&A |

---

<!-- _class: lead -->

# Part 1: Chatbots

---

## A chatbot is a conversation with an AI

- You type (or say) a **prompt**: a question or a request.
- The AI writes back a **response**.
- It's a lot like Google: you ask, it answers.
- The difference: it writes a full answer for you, and you can keep talking to refine it.

<!--
Emphasize the word "prompt". We'll use it all night.
-->

---

## The two main chatbots

<div class="cols">
<div>

**ChatGPT**
made by **OpenAI**

</div>
<div>

**Claude**
made by **Anthropic**

</div>
</div>

Both have free versions. Paid plans start around $20 a month.

---

## OpenAI

- Founded in **December 2015** in San Francisco as a nonprofit research lab.
- Co-founders included **Sam Altman**, **Greg Brockman**, **Ilya Sutskever** and **Elon Musk**.
- **Sam Altman**, the CEO, dropped out of Stanford to start a company, then ran **Y Combinator**, the best-known startup accelerator.
- Released **ChatGPT** on **November 30, 2022**. It became one of the fastest-growing apps in history.

<!--
Musk left the board in 2018 and later sued OpenAI. Altman was briefly fired by the board and reinstated in November 2023. Use either if the room is interested.
-->

---

## Anthropic

- Founded in **2021** by **Dario Amodei** and **Daniela Amodei**, a brother and sister, with several colleagues.
- They came from **OpenAI**: Dario was its VP of Research and led work on GPT-2 and GPT-3.
- They left to build an AI company focused on **safety**.
- Released **Claude** in **March 2023**. Their tool **Claude Code** is what I use every day, and what I'll demo tonight.

---

## Many others

- **Google:** Gemini
- **Microsoft:** Copilot
- **Meta:** Meta AI
- **xAI** (Elon Musk): Grok
- Plus many more in the US, China and Europe

They all work the same basic way: prompt and response.

---

## Live demo: chatbot

Try along on your phone at **chatgpt.com** or **claude.ai**.

<!--
Demo prompts (Claude or ChatGPT; voice mode is a good surprise for beginners):
1. "I run a small family restaurant on Main Street in Greeneville, Tennessee. Give me five low-cost ideas to bring in more customers this winter."
2. "Write a short Facebook post announcing the second idea."
3. "Translate that post into Spanish." Ask if anyone in the room speaks Spanish and can judge it.
4. Ask the audience for a question from their own work or life.
Optional: take a photo of something in the room (or the flyer) and ask about it.
-->

---

## Getting good answers

- **Give context:** who you are, what it's for, who will read it.
- **Be specific:** "two short paragraphs, friendly, no jargon."
- **Keep going:** ask for changes. It's a conversation.
- **Check what matters:** it can be confidently wrong about facts, numbers and names.
- **Protect privacy:** no passwords, account numbers or other people's private information.

---

<!-- _class: lead -->

# Part 2: AI agents

---

## From prompt and response to prompt and work

<div class="cols">
<div>

**Chatbot**
- You prompt, it responds
- You copy and paste the result
- One answer at a time

</div>
<div>

**Agent**
- You prompt, it **works**
- It plans, takes many steps on its own, and checks its work
- It hands you a finished result

</div>
</div>

---

## What an agent can work with

- **Your files:** read, write and organize them
- **Your email and calendar**, if you connect them
- **Your web browser:** it can click, type and fill in forms
- **Documents:** PDFs, spreadsheets, slides
- **Software:** whole programs, websites and apps, published online

In short, it can start doing knowledge work for you.

<!--
Agents: Claude Code (Anthropic), Codex (OpenAI), and others. Mention that you approve what it's allowed to do.
-->

---

## My last year as a software engineer

<div class="cols">
<div>

**A year ago**
- I wrote most of my code by hand
- AI suggested lines and answered questions

</div>
<div>

**Today**
- Agents write most of my code
- I decide what to build and check the work
- Several agents work at once

</div>
</div>

<!--
Tell the story in your own words: when it changed, what the turning point was, what a typical day looks like now, how much more you get done, and how it felt.
-->

---

## Live demo: Claude Code

1. Make a **PDF** flyer for a local business
2. Turn it into a **website**
3. Put it **live on the internet**, right now

<!--
Ask the room for a business name (or use a made-up one, e.g. "Big Spring Coffee, 101 Main St").
Prompts:
1. "Create a one-page PDF flyer for <business>: name, a one-line description, three menu items with prices, hours, and address. Open it when done."
2. "Turn the flyer into a simple, good-looking one-page website with the same content."
3. "Create a public GitHub repository for it under my account, push it, turn on GitHub Pages, and give me the live URL and a QR code for it."
Show the QR so people can open the site on their phones.
Rehearse beforehand. Pre-approve gh. Have a finished copy ready in case the Wi-Fi fails.
-->

---

## Any field of knowledge work

If the work happens on a computer, an agent can help do it.

- Software engineering
- Computer-aided drafting and design
- Accounting and bookkeeping
- Legal documents and contracts
- Marketing, writing and research
- Office work: forms, scheduling, data entry

---

<!-- _class: lead -->

# Part 3: Checking AI's work

---

## How I work with agents

1. **Deliberate and specify:** decide exactly what I want, with the AI's help
2. **Autonomous implementation:** the agent does the work
3. **Check the work:**
   - **Human review:** I read it
   - **AI review:** other AI agents read it
   - **Automated checks:** tests and tools that give the same answer every time
4. **Judge the evidence**

<!--
"Stochastic" checks (human and AI review) are like spot checks: useful, but they can miss things. "Deterministic" checks are programs that give the same answer every time: tests, type checkers, linters, mathematical proofs.
-->

---

## Becoming an agentic engineer

- My job shifts from **doing** the work to **judging the evidence** that the work is right.
- The goal: let the AI do more and more, and present me with evidence.
- That's how one person scales.

This works for any knowledge work: a contract, a drawing, a budget, a report.

<!--
Example outside software: a contract. Specify the terms; the agent drafts it; you read it, a second AI reviews it against a checklist, and a tool checks every cited law and date.
-->

---

## The automated checks

- **Tests:** run the work against examples
- **Property-based testing:** check rules across thousands of generated cases
- **Formal verification:** a mathematical proof that the software is correct
- **Slop Refinery:** automated checks for common AI coding mistakes

<!--
Show the Slop Refinery repo (github.com/HOWMZofficial/slop-refinery). Note it's from your work at HOWMZ.
-->

---

## What I've built with AI

- **Millillion:** millillion.org
- **Lasm:** runs Lean (a language for mathematical proofs) in JavaScript and WebAssembly
- **ProofScript:** a planned version of TypeScript with built-in proofs
- **Wasmetal:** a WebAssembly CPU in hardware

<!--
Show millillion.org and millillion.org/projects.
Show the tweet with the Fable video: <TWEET URL>
Lasm: my estimate is several people's work over about three years, done in about three weeks.
-->

---

## How AI helped with tonight

- The meetup website and calendar file
- The flyer and its QR code
- Finding who to contact, drafting emails, and checking the listings
- These slides, and publishing them online

---

<!-- _class: lead -->

# Q&A

Ask anything, at any level.

---

## Thank you

- **Sign up** to hear about the next meetup.
- **Next time:** locals presenting how they use AI in their businesses and lives. Want to present? Talk to me tonight or get in touch.
- **Contact:** millillion.org/contact

<div class="cols">
<div>

**Slides:** millillion.org/meetup/slides
**Meetup:** millillion.org/meetup

</div>
<img class="qr" src="images/qr-meetup.svg" alt="QR code for the meetup page">
</div>
