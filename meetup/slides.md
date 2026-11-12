---
marp: true
theme: millillion
title: "Greeneville AI Meetup: What AI Can Do for You"
description: Thursday, November 12, 2026, Big Spring Room, Greeneville/Greene County Public Library
author: Jordan Last
---

<!-- _class: title -->

<img class="logo" src="images/millillion-black.svg" alt="ɛ∞ɜ">

# Greeneville AI Meetup

<div class="sub">What AI Can Do for You</div>
<div class="meta">Thursday, November 12, 2026 · Big Spring Room, Greeneville/Greene County Public Library</div>
<div class="seal"></div>

<!--
Doors at 7:00. Start about 7:05.
-->

---

## Tonight

<ol class="overview">
<li>Introduction</li>
<li>Chatbots</li>
<li>Agents</li>
<li>One Year Ago</li>
<li>Slop Refinery Pipeline</li>
<li>Agentic Engineers</li>
</ol>

<p class="muted small">Questions are welcome at any time.</p>

---

<!-- _class: divider -->

<div class="num">01</div>

# Introduction

<div class="brush"></div>

---

## Jordan Last

- Agentic engineer
- Software, built with AI agents, every day
- Greeneville, Tennessee

<!--
Who you are, how you got here, why you moved to Greeneville, why you're starting this meetup.
Quick show of hands: who has used ChatGPT or Claude? Who uses one every week? Who has used an AI agent?
-->

---

## Millillion

<p class="tagline">Impossibly ambitious AI</p>

<div class="tiles three">
<div><span class="big">Lasm</span><span class="cap">Lean for JavaScript and WebAssembly runtimes</span></div>
<div><span class="big">ProofScript</span><span class="cap">A variant of TypeScript with dependent types and formal verification</span></div>
<div><span class="big">WasMetal</span><span class="cap">A bare metal physical implementation of WebAssembly. That's right, a WebAssembly CPU.</span></div>
</div>

<p class="caption">millillion.org</p>

<!--
What Millillion is and why. Show millillion.org and the projects page.
-->

---

<!-- _class: divider -->

<div class="num">02</div>

# Chatbots

<div class="brush"></div>

---

## Prompt and response

<svg class="diagram" viewBox="0 0 1088 230" xmlns="http://www.w3.org/2000/svg">
<defs><marker id="a1" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="9" markerHeight="9" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#161412"/></marker></defs>
<g font-family="Shippori Mincho, serif" font-weight="600" text-anchor="middle">
<rect x="10" y="60" width="230" height="110" rx="8" fill="#ece6da"/>
<text x="125" y="128" font-size="38" fill="#161412">You</text>
<rect x="429" y="60" width="230" height="110" rx="8" fill="#b3341f"/>
<text x="544" y="128" font-size="38" fill="#f6f2ea">AI</text>
<rect x="848" y="60" width="230" height="110" rx="8" fill="#ece6da"/>
<text x="963" y="128" font-size="38" fill="#161412">Answer</text>
<line x1="250" y1="115" x2="419" y2="115" stroke="#161412" stroke-width="3" marker-end="url(#a1)"/>
<line x1="669" y1="115" x2="838" y2="115" stroke="#161412" stroke-width="3" marker-end="url(#a1)"/>
<text x="334" y="96" font-size="28" fill="#57524b">prompt</text>
<text x="753" y="96" font-size="28" fill="#57524b">response</text>
</g>
</svg>

<p class="caption">Like Google: you ask, it answers.</p>

---

## Two of the main chatbots

<div class="tiles two">
<div><span class="big">ChatGPT</span><span class="cap">OpenAI · 2015 · Sam Altman, Elon Musk</span></div>
<div><span class="big">Claude</span><span class="cap">Anthropic · 2021 · Dario and Daniela Amodei</span></div>
</div>

<p class="caption">And many others: Gemini, Copilot, Meta AI, Grok, DeepSeek</p>

<!--
OpenAI: founded December 2015 in San Francisco as a nonprofit research lab. Co-founders included Sam Altman, Greg Brockman, Ilya Sutskever and Elon Musk. Altman dropped out of Stanford to start a company (Loopt), then ran Y Combinator, the best-known startup accelerator. ChatGPT launched November 30, 2022 and became one of the fastest-growing apps in history.
Anthropic: founded 2021 by siblings Dario and Daniela Amodei and several colleagues, all from OpenAI. Dario was OpenAI's VP of Research and led work on GPT-2 and GPT-3. They left to build an AI company focused on safety. Claude launched March 2023.
Others: Google (Gemini), Microsoft (Copilot), Meta (Meta AI), xAI (Grok), DeepSeek (China).
-->

---

<!-- _class: statement -->

# Demo

<p>claude.ai</p>

<!--
Jordan's plan (claude.ai):
1. "Are there any AI meetups in Greeneville tonight?"
2. Ask where it is, and how much it costs.
3. "What if I don't know anything about AI?"
4. Ask it to translate the answer into Spanish for my wife, then play the audio.
5. Voice mode: talk to it out loud.
6. "Can you teach me about yourself?"
People can try along on their phones at claude.ai.
-->

---

## Getting started

<div class="plans">
<div>
<h3>Claude <span>claude.ai</span></h3>
<table>
<tr><td>Free</td><td>$0</td></tr>
<tr><td>Pro</td><td>$20 a month</td></tr>
<tr><td>Max</td><td>$100 a month</td></tr>
<tr><td>Ultra</td><td>$200 a month</td></tr>
</table>
</div>
<div>
<h3>ChatGPT <span>chatgpt.com</span></h3>
<table>
<tr><td>Free</td><td>$0</td></tr>
<tr><td>Go</td><td>$8 a month</td></tr>
<tr><td>Plus</td><td>$20 a month</td></tr>
<tr><td>Pro</td><td>$100, $200 or $500 a month</td></tr>
</table>
</div>
</div>

<p class="caption">Both: web, Mac, Windows, iPhone and Android. Start free.</p>

<!--
Checked on claude.com/pricing and chatgpt.com/pricing on November 11, 2026. Prices are before tax.
Claude: Free $0. Pro $20 a month, or $17 a month billed yearly ($200 up front); includes Claude Code. Max $100 a month (5x Pro usage). Ultra $200 a month (10x Pro weekly usage).
ChatGPT: Free $0. Go $8 a month (may include ads). Plus $20 a month. Pro comes in three tiers: $100, $200 or $500 a month.
Apps: claude.com/download and chatgpt.com/download for desktop; App Store and Google Play for phones. Same account everywhere.
Advice: start with the free plan. If you use it every day, $20 a month (Claude Pro or ChatGPT Plus) is the usual next step.
-->

---

<!-- _class: divider -->

<div class="num">03</div>

# Agents

<div class="brush"></div>

---

## Prompt and work

<svg class="diagram" viewBox="0 0 1088 400" xmlns="http://www.w3.org/2000/svg">
<defs><marker id="a2" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="9" markerHeight="9" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#161412"/></marker><marker id="a2w" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="14" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#f6f2ea"/></marker></defs>
<g font-family="Shippori Mincho, serif" font-weight="600" text-anchor="middle">
<rect x="10" y="70" width="200" height="110" rx="8" fill="#ece6da"/>
<text x="110" y="138" font-size="36" fill="#161412">You</text>
<rect x="354" y="20" width="380" height="210" rx="8" fill="#b3341f"/>
<text x="544" y="76" font-size="36" fill="#f6f2ea">Agent</text>
<text x="544" y="136" font-size="28" fill="#f6f2ea">plan → act → check</text>
<path d="M 645 148 C 645 194, 441 194, 441 152" fill="none" stroke="#f6f2ea" stroke-width="2.5" stroke-linecap="round" marker-end="url(#a2w)"/>
<text x="544" y="215" font-size="20" fill="#f6f2ea" font-weight="500">repeats until done</text>
<rect x="878" y="70" width="200" height="110" rx="8" fill="#ece6da"/>
<text x="978" y="124" font-size="32" fill="#161412">Finished</text>
<text x="978" y="160" font-size="32" fill="#161412">work</text>
<line x1="220" y1="125" x2="344" y2="125" stroke="#161412" stroke-width="3" marker-end="url(#a2)"/>
<line x1="744" y1="125" x2="868" y2="125" stroke="#161412" stroke-width="3" marker-end="url(#a2)"/>
<text x="282" y="106" font-size="26" fill="#57524b">prompt</text>
<g font-size="26" fill="#161412">
<rect x="84" y="310" width="140" height="70" rx="6" fill="none" stroke="#161412" stroke-width="2"/><text x="154" y="354">Files</text>
<rect x="240" y="310" width="140" height="70" rx="6" fill="none" stroke="#161412" stroke-width="2"/><text x="310" y="354">Terminal</text>
<rect x="396" y="310" width="140" height="70" rx="6" fill="none" stroke="#161412" stroke-width="2"/><text x="466" y="354">Programs</text>
<rect x="552" y="310" width="140" height="70" rx="6" fill="none" stroke="#161412" stroke-width="2"/><text x="622" y="354">Browser</text>
<rect x="708" y="310" width="140" height="70" rx="6" fill="none" stroke="#161412" stroke-width="2"/><text x="778" y="354">Email</text>
<rect x="864" y="310" width="140" height="70" rx="6" fill="none" stroke="#161412" stroke-width="2"/><text x="934" y="354">Calendar</text>
</g>
<g stroke="#57524b" stroke-width="2" stroke-dasharray="6 6">
<line x1="154" y1="308" x2="400" y2="232"/><line x1="310" y1="308" x2="458" y2="232"/><line x1="466" y1="308" x2="516" y2="232"/><line x1="622" y1="308" x2="574" y2="232"/><line x1="778" y1="308" x2="632" y2="232"/><line x1="934" y1="308" x2="690" y2="232"/>
</g>
</g>
</svg>

<!--
A chatbot gives you an answer. An agent does the work: it plans, takes many steps on its own, checks its work, and hands you the result.
It can read and write your files, run commands in the terminal, use the programs on your computer, use your email and calendar if you connect them, and control your browser: click, type, fill in forms.
It can make PDFs, spreadsheets, websites and whole software projects. Examples: Claude Code (Anthropic), Codex (OpenAI).
-->

---

<!-- _class: statement -->

# Demo

<svg class="diagram" viewBox="0 0 1088 160" xmlns="http://www.w3.org/2000/svg" style="margin-top:40px">
<defs><marker id="a3" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="9" markerHeight="9" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#161412"/></marker></defs>
<g font-family="Shippori Mincho, serif" font-weight="600" text-anchor="middle" font-size="36">
<rect x="40" y="25" width="250" height="110" rx="8" fill="#ece6da"/><text x="165" y="93" fill="#161412">PDF</text>
<rect x="419" y="25" width="250" height="110" rx="8" fill="#ece6da"/><text x="544" y="93" fill="#161412">Website</text>
<rect x="798" y="25" width="250" height="110" rx="8" fill="#b3341f"/><text x="923" y="93" fill="#f6f2ea">Live online</text>
<line x1="300" y1="80" x2="409" y2="80" stroke="#161412" stroke-width="3" marker-end="url(#a3)"/>
<line x1="679" y1="80" x2="788" y2="80" stroke="#161412" stroke-width="3" marker-end="url(#a3)"/>
</g>
</svg>

<p>Claude Code</p>

<!--
Ask the room for a business name (or use a made-up one, e.g. "Big Spring Coffee, 101 Main St").
1. "Create a one-page PDF flyer for <business>: name, a one-line description, three menu items with prices, hours, and address. Open it when done."
2. "Turn the flyer into a simple, good-looking one-page website with the same content."
3. "Create a public GitHub repository for it under my account, push it, turn on GitHub Pages, and give me the live URL and a QR code for it."
Show the QR so people can open the site on their phones.
Rehearse beforehand. Pre-approve gh. Have a finished copy ready in case the Wi-Fi fails.
-->

---

## Any knowledge work

<div class="tiles">
<div>Software</div>
<div>Drafting and CAD</div>
<div>Accounting</div>
<div>Contracts</div>
<div>Marketing</div>
<div>Research</div>
<div>Office work</div>
<div>Teaching</div>
</div>

<p class="caption">If the work happens on a computer, an agent can help do it.</p>

---

## The main levers

<svg class="diagram" viewBox="0 0 1088 432" xmlns="http://www.w3.org/2000/svg">
<defs>
<filter id="ink" x="-5%" y="-5%" width="110%" height="110%"><feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="2" seed="7"/><feDisplacementMap in="SourceGraphic" scale="3.5"/></filter>
<marker id="dot" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="7" markerHeight="7"><circle cx="5" cy="5" r="4" fill="#b3341f"/></marker>
</defs>
<g filter="url(#ink)" fill="none" stroke="#161412" stroke-linecap="round" stroke-linejoin="round">
<rect x="14" y="8" width="1060" height="232" rx="14" stroke-width="4.5"/>
<line x1="14" y1="54" x2="1074" y2="54" stroke-width="3"/>
<line x1="34" y1="176" x2="1054" y2="176" stroke-width="2.5" stroke="#57524b"/>
<rect x="852" y="198" width="190" height="20" rx="4" stroke-width="2.5"/>
</g>
<g filter="url(#ink)"><rect x="854" y="200" width="76" height="16" rx="3" fill="#b3341f"/></g>
<g fill="#161412"><circle cx="44" cy="31" r="7"/><circle cx="68" cy="31" r="7"/><circle cx="92" cy="31" r="7"/></g>
<g font-family="ui-monospace, Menlo, Consolas, monospace" font-size="24" fill="#161412">
<text x="44" y="98">&gt; Make a PDF flyer for Big Spring Coffee</text>
<text x="44" y="140" fill="#57524b">● Writing flyer.pdf … done</text>
<text x="70" y="216" font-weight="700">Opus</text><text x="150" y="216">5.5</text>
<text x="330" y="216">effort: high</text>
<text x="600" y="216">fast: off</text>
</g>
<g filter="url(#ink)" stroke="#b3341f" stroke-width="3" stroke-linecap="round" fill="none">
<path d="M 102 226 C 98 260, 106 290, 110 318" marker-start="url(#dot)"/>
<path d="M 170 226 C 210 262, 280 290, 310 318" marker-start="url(#dot)"/>
<path d="M 410 226 C 420 262, 510 292, 525 318" marker-start="url(#dot)"/>
<path d="M 655 226 C 680 262, 735 292, 745 318" marker-start="url(#dot)"/>
<path d="M 946 226 C 950 262, 958 292, 960 318" marker-start="url(#dot)"/>
</g>
<g font-family="Shippori Mincho, serif" text-anchor="middle">
<g font-size="28" font-weight="600" fill="#161412">
<text x="110" y="356">Model family</text><text x="310" y="356">Version</text><text x="525" y="356">Reasoning effort</text><text x="745" y="356">Speed</text><text x="960" y="356">Cost</text>
</g>
<g font-size="21" font-weight="500" fill="#57524b">
<text x="110" y="392">Fable, Opus,</text><text x="110" y="420">Sonnet, Haiku</text>
<text x="310" y="392">newer is</text><text x="310" y="420">smarter</text>
<text x="525" y="392">how long it thinks:</text><text x="525" y="420">low to max</text>
<text x="745" y="392">fast mode and</text><text x="745" y="420">smaller models</text>
<text x="960" y="392">your plan's</text><text x="960" y="420">usage</text>
</g>
</g>
</svg>


<!--
These are the controls that matter most, in Claude Code, claude.ai and ChatGPT alike.
The tradeoff: more capable models and more thinking give better work, but cost more usage and take more time.
Model family: Fable (Anthropic's top model), Opus, Sonnet, Haiku. Bigger is more capable; smaller is faster and cheaper. ChatGPT has its own families in a model picker.
Version: the number, like 5.5. Newer versions are smarter. Use the latest.
Reasoning effort: how long the model thinks before it answers: low, medium, high, extra high, max. Harder problems deserve more effort.
Speed: smaller models and fast mode answer sooner.
Cost: every request uses part of your plan's usage. Bigger models and more effort use it up faster. Check your usage in settings.
Rule of thumb: start with a strong model at medium or high effort; turn effort up for hard problems and down for quick ones.
The interface drawn here is a sketch in the style of Claude Code, not an exact screenshot.
-->

---

<!-- _class: statement -->

# Ask it to teach you

<p>Anything from tonight, explained the way you learn best.</p>

<div class="examples">
<div>“Explain reasoning effort like I’m new to computers.”</div>
<div>“Quiz me on the difference between a chatbot and an agent.”</div>
<div>“Make me a one-page cheat sheet of tonight’s ideas.”</div>
</div>

<!--
The AI can teach you how to use the AI. Any concept from tonight: ask it to explain it simply, with examples from your own work, as a quiz, a diagram, a story, or out loud in voice mode. Ask follow-up questions until it makes sense.
-->

---

<!-- _class: divider -->

<div class="num">04</div>

# One Year Ago

<div class="brush"></div>

---

## Then and now

<svg class="diagram" viewBox="0 0 1088 420" xmlns="http://www.w3.org/2000/svg">
<defs><marker id="a4" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="9" markerHeight="9" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#161412"/></marker></defs>
<g font-family="Shippori Mincho, serif" font-weight="600" text-anchor="middle">
<text x="10" y="86" font-size="30" fill="#57524b" text-anchor="start">A year ago</text>
<rect x="250" y="35" width="170" height="80" rx="8" fill="#ece6da"/><text x="335" y="86" font-size="32" fill="#161412">Me</text>
<rect x="878" y="35" width="200" height="80" rx="8" fill="#ece6da"/><text x="978" y="86" font-size="32" fill="#161412">Code</text>
<line x1="430" y1="75" x2="868" y2="75" stroke="#161412" stroke-width="3" marker-end="url(#a4)"/>
<text x="649" y="60" font-size="24" fill="#57524b" font-weight="500">I write it, AI suggests a line</text>
<line x1="10" y1="170" x2="1078" y2="170" stroke="#d9d2c5" stroke-width="2"/>
<text x="10" y="326" font-size="30" fill="#b3341f" text-anchor="start">Today</text>
<rect x="250" y="275" width="170" height="80" rx="8" fill="#ece6da"/><text x="335" y="326" font-size="32" fill="#161412">Me</text>
<g font-size="24" fill="#f6f2ea">
<rect x="560" y="205" width="170" height="52" rx="6" fill="#b3341f"/><text x="645" y="240">Agent</text>
<rect x="560" y="265" width="170" height="52" rx="6" fill="#b3341f"/><text x="645" y="300">Agent</text>
<rect x="560" y="325" width="170" height="52" rx="6" fill="#b3341f"/><text x="645" y="360">Agent</text>
</g>
<text x="645" y="410" font-size="30" fill="#b3341f">⋮</text>
<rect x="878" y="275" width="200" height="80" rx="8" fill="#ece6da"/><text x="978" y="326" font-size="32" fill="#161412">Code</text>
<g stroke="#161412" stroke-width="2.5">
<line x1="430" y1="315" x2="552" y2="231" marker-end="url(#a4)"/><line x1="430" y1="315" x2="552" y2="291" marker-end="url(#a4)"/><line x1="430" y1="315" x2="552" y2="351" marker-end="url(#a4)"/>
<line x1="738" y1="231" x2="870" y2="305" marker-end="url(#a4)"/><line x1="738" y1="291" x2="870" y2="313" marker-end="url(#a4)"/><line x1="738" y1="351" x2="870" y2="323" marker-end="url(#a4)"/>
</g>
</g>
</svg>

<!--
Tell the story in your own words: when it changed, the turning point, what a typical day looks like now, how much more you get done, and how it felt.
-->

---

<!-- _class: divider -->

<div class="num">05</div>

# Slop Refinery Pipeline

<div class="brush"></div>

---

## Specify, implement, check, judge

<svg class="diagram" viewBox="0 0 1088 420" xmlns="http://www.w3.org/2000/svg">
<defs><marker id="a5" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="9" markerHeight="9" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#161412"/></marker><marker id="a5r" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="9" markerHeight="9" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#b3341f"/></marker></defs>
<g font-family="Shippori Mincho, serif" font-weight="600" text-anchor="middle">
<rect x="0" y="130" width="190" height="110" rx="8" fill="#ece6da"/><text x="95" y="182" font-size="30" fill="#161412">Specify</text><text x="95" y="218" font-size="20" fill="#57524b" font-weight="500">you + AI</text>
<rect x="250" y="130" width="190" height="110" rx="8" fill="#b3341f"/><text x="345" y="182" font-size="30" fill="#f6f2ea">Implement</text><text x="345" y="218" font-size="20" fill="#f6f2ea" font-weight="500">AI, on its own</text>
<rect x="500" y="30" width="270" height="310" rx="8" fill="none" stroke="#161412" stroke-width="2"/>
<text x="635" y="72" font-size="30" fill="#161412">Check</text>
<g font-size="22" font-weight="500">
<rect x="520" y="95" width="230" height="64" rx="6" fill="#ece6da"/><text x="635" y="135" fill="#161412">Deterministic checks</text>
<rect x="520" y="175" width="230" height="64" rx="6" fill="#ece6da"/><text x="635" y="215" fill="#161412">AI review</text>
<rect x="520" y="255" width="230" height="64" rx="6" fill="#ece6da"/><text x="635" y="295" fill="#161412">Human review</text>
</g>
<rect x="830" y="130" width="250" height="110" rx="8" fill="#ece6da"/><text x="955" y="182" font-size="30" fill="#161412">Evidence</text><text x="955" y="218" font-size="20" fill="#57524b" font-weight="500">you judge it</text>
<g stroke="#161412" stroke-width="3">
<line x1="198" y1="185" x2="242" y2="185" marker-end="url(#a5)"/>
<line x1="448" y1="185" x2="492" y2="185" marker-end="url(#a5)"/>
<line x1="778" y1="185" x2="822" y2="185" marker-end="url(#a5)"/>
</g>
<path d="M 955 248 C 955 415, 345 415, 345 250" fill="none" stroke="#b3341f" stroke-width="3" stroke-dasharray="8 7" marker-end="url(#a5r)"/>
<text x="650" y="406" font-size="24" fill="#b3341f">not yet: fix and check again</text>
</g>
</svg>

<!--
1. Deliberation and specification: decide exactly what you want, with the AI's help.
2. Autonomous implementation: the AI does the work.
3. Checks: human cognitive stochastic checks (you read it), AI cognitive stochastic checks (other agents review it), and deterministic checks (tests, type checks, linters, proofs: same answer every time).
4. The AI presents evidence; you judge it. If it's not right yet, back to implementation.
This works for any knowledge work, not just software.
-->

---

## Verification

<svg class="diagram" viewBox="0 0 1088 420" xmlns="http://www.w3.org/2000/svg">
<g font-family="Shippori Mincho, serif" font-weight="600" text-anchor="middle">
<polygon points="40,10 720,10 660,140 100,140" fill="#161412"/>
<text x="380" y="68" font-size="32" fill="#f6f2ea">1. Deterministic checks</text>
<text x="380" y="108" font-size="22" fill="#f6f2ea" font-weight="500">as many as possible</text>
<polygon points="108,150 652,150 592,280 168,280" fill="#b3341f"/>
<text x="380" y="208" font-size="32" fill="#f6f2ea">2. AI review</text>
<text x="380" y="248" font-size="22" fill="#f6f2ea" font-weight="500">what programs can't check</text>
<polygon points="176,290 584,290 524,410 236,410" fill="#ece6da"/>
<text x="380" y="345" font-size="32" fill="#161412">3. Human review</text>
<text x="380" y="383" font-size="22" fill="#57524b" font-weight="500">whatever is left</text>
<g text-anchor="start" font-size="24">
<line x1="770" y1="20" x2="770" y2="130" stroke="#161412" stroke-width="3"/>
<text x="792" y="58" fill="#161412">Deterministic</text>
<text x="792" y="92" fill="#57524b" font-weight="500" font-size="20">A program or script.</text>
<text x="792" y="120" fill="#57524b" font-weight="500" font-size="20">Same input, same result.</text>
<line x1="770" y1="160" x2="770" y2="400" stroke="#b3341f" stroke-width="3"/>
<text x="792" y="250" fill="#b3341f">Stochastic</text>
<text x="792" y="284" fill="#57524b" font-weight="500" font-size="20">Judgment by AI or people.</text>
<text x="792" y="312" fill="#57524b" font-weight="500" font-size="20">Results can vary.</text>
</g>
</g>
</svg>

<p class="caption">Fill each level in order. The agentic engineer guides the AI through it.</p>

<!--
Robust verification combines deterministic and stochastic checks.
Deterministic checks are repeatable and predictable: always the same result for the same input. Usually a program or script: tests, type checks, linters, proofs.
Stochastic checks are what AIs and humans do: reading, judging, reviewing. Useful, but results can vary.
Order: get as many deterministic checks as possible. Whatever can't be done deterministically, check stochastically with AI, as much as possible. Whatever is left over must be checked by humans.
The agentic engineer guides the AI through this: fill up the deterministic checks first, then decide what AI review can cover, then what a human must review.
Formal verification is the strongest deterministic check: a mathematical proof that the code is correct.
-->

---

<!-- _class: statement -->

# Lasm

<p>Years of work for several people, done in weeks</p>

<!--
Lasm runs Lean (a language for mathematical proofs) in JavaScript and WebAssembly. My estimate: about three years of work for several people, done in about three weeks, built with this pipeline.
Show github.com/Millillion/lasm, ProofScript, and the Fable video tweet: <TWEET URL>
-->

---

<!-- _class: divider -->

<div class="num">06</div>

# Agentic Engineers

<div class="brush"></div>

---

## Jagged intelligence

<svg class="diagram" viewBox="0 0 1088 440" xmlns="http://www.w3.org/2000/svg">
<defs><clipPath id="valleys"><rect x="0" y="200" width="1088" height="200"/></clipPath></defs>
<g font-family="Shippori Mincho, serif" font-weight="600">
<polygon clip-path="url(#valleys)" fill="#b3341f" opacity="0.18" points="40,0 40,260 110,120 170,230 230,80 300,290 360,150 420,60 490,250 550,330 610,170 670,100 740,270 800,140 860,50 930,240 990,130 1048,180 1048,0"/>
<polyline fill="none" stroke="#57524b" stroke-width="2" stroke-dasharray="3 7" opacity="0.8" points="40,200 110,60 170,170 230,20 300,230 360,90 420,0 490,190 550,270 610,110 670,40 740,210 800,80 860,0 930,180 990,70 1048,120"/>
<line x1="20" y1="200" x2="1068" y2="200" stroke="#161412" stroke-width="2" stroke-dasharray="10 8"/>
<polyline fill="none" stroke="#161412" stroke-width="4" stroke-linejoin="round" points="40,260 110,120 170,230 230,80 300,290 360,150 420,60 490,250 550,330 610,170 670,100 740,270 800,140 860,50 930,240 990,130 1048,180"/>
<text x="550" y="370" font-size="26" fill="#b3341f" text-anchor="middle">our opportunity</text>
<g font-size="22" fill="#161412" font-weight="500">
<line x1="150" y1="425" x2="200" y2="425" stroke="#161412" stroke-width="4"/><text x="212" y="433">AI today</text>
<line x1="420" y1="425" x2="470" y2="425" stroke="#161412" stroke-width="2" stroke-dasharray="10 8"/><text x="482" y="433">Human level</text>
<line x1="700" y1="425" x2="750" y2="425" stroke="#57524b" stroke-width="2" stroke-dasharray="3 7"/><text x="762" y="433" fill="#57524b">AI next year?</text>
</g>
</g>
</svg>

<p class="caption">The valleys are where people still have the edge. For how long?</p>

<!--
AI's abilities are jagged: far better than people at some things, surprisingly bad at others.
Peaks: writing, translation, coding, summarizing, recalling facts across every field.
Valleys (examples to choose from): local knowledge and relationships, judgment and taste, trust and accountability, physical work, long tasks with unclear goals, knowing what's worth doing.
The valleys are our opportunity, if we build those skills. But each new model raises the line, and the valleys keep shrinking. How long they last is the open question.
-->

---

## Judging the evidence

<svg class="diagram" viewBox="0 0 1088 380" xmlns="http://www.w3.org/2000/svg">
<defs><marker id="a6" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="9" markerHeight="9" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#161412"/></marker><marker id="a6r" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="9" markerHeight="9" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#b3341f"/></marker></defs>
<g font-family="Shippori Mincho, serif" font-weight="600" text-anchor="middle">
<rect x="444" y="10" width="200" height="90" rx="8" fill="#ece6da"/><text x="544" y="67" font-size="34" fill="#161412">You</text>
<g font-size="24" fill="#f6f2ea">
<rect x="60" y="290" width="160" height="70" rx="6" fill="#b3341f"/><text x="140" y="333">Agent</text>
<rect x="270" y="290" width="160" height="70" rx="6" fill="#b3341f"/><text x="350" y="333">Agent</text>
<rect x="464" y="290" width="160" height="70" rx="6" fill="#b3341f"/><text x="544" y="333">Agent</text>
<rect x="658" y="290" width="160" height="70" rx="6" fill="#b3341f"/><text x="738" y="333">Agent</text>
<rect x="868" y="290" width="160" height="70" rx="6" fill="#b3341f"/><text x="948" y="333">Agent</text>
</g>
<g stroke="#161412" stroke-width="2.5">
<line x1="490" y1="108" x2="150" y2="282" marker-end="url(#a6)"/><line x1="510" y1="108" x2="360" y2="282" marker-end="url(#a6)"/><line x1="530" y1="108" x2="530" y2="282" marker-end="url(#a6)"/>
</g>
<g stroke="#b3341f" stroke-width="2.5" stroke-dasharray="7 6">
<line x1="558" y1="282" x2="558" y2="108" marker-end="url(#a6r)"/><line x1="728" y1="282" x2="578" y2="108" marker-end="url(#a6r)"/><line x1="938" y1="282" x2="598" y2="108" marker-end="url(#a6r)"/>
</g>
<text x="260" y="170" font-size="26" fill="#161412">goals</text>
<text x="830" y="170" font-size="26" fill="#b3341f">evidence</text>
</g>
</svg>

<p class="caption">You decide what to build, and judge the evidence that it's right.</p>

<!--
The job shifts from doing the work to judging the evidence the AI presents. Let the AI do more and more, and present you with evidence. That's how one person scales. It applies to any knowledge work: a contract, a drawing, a budget, a report.
-->

---

<!-- _class: statement -->

# Questions

<p>Ask anything, at any level.</p>

---

## Thank you

<div class="qrrow">
<div><img class="qr" src="images/qr-meetup.svg" alt="QR code for the meetup page"><p>Sign up for the next meetup<br>millillion.org/meetup</p></div>
<div><img class="qr" src="images/qr-slides.svg" alt="QR code for the slides"><p>These slides<br>millillion.org/meetup/slides</p></div>
</div>

<p class="caption">Next time: locals showing how they use AI. Want to present? Talk to me.</p>
