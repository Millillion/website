---
title: "Formally Verify All Software"
date: 2026-10-31
description: "Why building correct software is so difficult, how testing goes from examples to properties to formal verification, and Lasm, my project that allows Lean to run almost anywhere that JavaScript or WebAssembly runs today."
adaptedFrom:
  label: "episode 2 of the Millillion podcast"
  href: "/podcast/002-formally-verify-all-software/"
---

Today I want to tell you about my recently launched project called [Lasm](/projects/lasm/). The name is a combination of Lean, an amazing programming language, and WebAssembly, an amazing portable bytecode format that is shortened to Wasm. First, though, let's talk a little bit about software development in general.

## Software is complex, and complexity is hard to tame

Software development is very difficult. You write out lines upon lines upon lines of instructions, and every line or statement is a specific instruction telling the computer to do something. Software is running many or most aspects of our lives. Whenever you interact with probably most machines, there are computers processing to make it all run safely and securely.

The problem with this absolutely outrageous amount of complexity is that it's complex, and complexity is hard to manage and hard to tame. The more moving parts you have, and the more pieces that need to fit together in certain ways, the easier it is for that thing to fall apart if we don't understand it very well and build it correctly. So building correct software that always functions exactly as we desire it to function is very difficult.

I think everyone kind of knows this. We all know the term bug. Sometimes a bug is just annoying, like some little thing wrong with the UI in my Instagram or Twitter app. That's okay. But what if it's something with your bank balance? That's a little bit more worrisome. What if you have a medical device like a pacemaker running inside of your body, or you're in the middle of a surgery that is only possible because of machines, including computers? Writing software and verifying its correctness is incredibly important. It depends on the type of software, and you don't need absolute assurance for everything.

## How we try to make software correct

In the age before AI, at least, the first technique is the human mind reasoning through the code, and a lot of these techniques do flow into the world of using AI agents to write software. Software engineers usually don't try to write code that is wrong. You use your own cognition to come up with a model in your mind of what should happen when your code runs. Those models, generally speaking, are incomplete and flawed.

So you do your best. You do your best thinking, you review it multiple times, you really clean it up, and once you believe you've done it correctly, you create a pull request. I love Git and GitHub. Then you ask another human on your team to review your PR. That's built into the engineering process. It's not like "hey, can you do this?" You must do this. It's part of how we work.

The reviewer has to come up with their own independent model of what's happening. Every person has a different brain, and they bring different strengths and weaknesses, so that usually helps to wring out even more bugs as you think about things from different angles.

You also write tests. There are many different methodologies for testing software, but the core concept is that you write a small program that executes the program under test, looks at its result, and checks that the result is correct.

## Example-based tests give you evidence

The simplest form of testing is probably example-based testing. Let's say you have a little function that takes the birth date of a user and returns their age. You contrive a user born on October 31st, 1996. I'm recording this on Halloween, so that person would be turning 30 today, I believe, and the function should return 30. You write a test that passes in that birth date and checks the result. That is one example-based test.

In my experience there's a lot of example-based testing out there, in open source projects and elsewhere. Hopefully you can see that it's a little bit limited. What you're trying to show is that your functionality is correct no matter the input that comes into it, that for all inputs a certain behavior holds. With example-based testing you're never actually proving that. You're just generating evidence. With 10 examples you have evidence of 10 examples. Add 10 more that try to cover weird edge cases, and now you have 20. That's getting better, and we're gaining more confidence that the function is correct, but there's no mathematical proof and no logical proof, just evidence.

You can always generate more examples, but that takes a lot of human effort. And even with AI, you cannot generate infinite examples.

## Property-based testing gives you much more evidence

So what if, instead of writing out one test case per example, you created a function that generates random inputs of the shape of the parameter of the function under test? For our age function, that would be a function that generates random birth dates, from 4000 BC to 2026, or even millions of years back to millions of years in the future. In a loop, you generate a birth date and call the function.

You can't check that each result is correct against a hard-coded example, because that's what we're trying to get away from. Instead you check properties that should hold, claims or propositions that should be true whenever you calculate an age. For example, the age of a person should never be less than zero.

With a random generator you can generate millions and billions of inputs really cheaply. We still do not have a proof, but we can generate way more evidence and start to emulate a mathematical proof, getting as close as possible. It's asymptotic, though. We'll never actually get there, and there are not enough computational resources to run it for that long. This is called property-based testing. I love property-based testing. It's really awesome. But there's something better.

## Formal verification

There actually is a way to mathematically prove that certain properties hold for all inputs. That is called formal verification. I guess I'm not an expert in formal verification, but to me it is an amazing concept that I've followed for years, and I'm now really diving into it because AI now makes it practical to begin to formally verify software that would have been outrageously difficult to formally verify before.

With enough cognitive effort, hopefully you can come up with a set of properties, or propositions, that are individually necessary and collectively sufficient to characterize the intended behavior of your functionality. I think that is the core thing to understand.

Imagine being able to formally verify all of our software. Not just mathematical calculations, cryptographic primitives and low-level protocols like TCP, but front-end code like HTML, CSS and JavaScript, back-end code with SQLite and Postgres, HTTP endpoints, and the file system. That is my dream, and with AI it becomes a possibility.

I believe that with AI, what was previously impossible, or seemingly impossible, or impractical, is now possible. The tasks that just seemed outrageous before are where we need to set our sights. The easy tasks from before are now trivial, the hard tasks from before are now easy, and the impossible tasks from before are now hard.

So I want to formally verify all software. I feel like that is now my mantra, and it's what I'm after.

## Lean

There are certain languages and tools that allow you to formally verify things, and my favorite is called Lean. Lean is a general purpose programming language, and it's also a functional programming language. I'm in love with functional programming and have been for a long time, but I've never really tried to adopt a truly functional programming language, because languages like Haskell and F# have felt impractical to me and aren't super mainstream. I preferred to stay in the mainstream with TypeScript and Rust.

Lean is amazing because it is a general purpose functional programming language with formal verification built in. You can write functions in Lean, and you can prove propositions about those functions right there in the Lean code, in the same language. I don't know if you've seen, but the major AI labs have been heavily using Lean to prove crazy mathematical things. In some ways, formal verification is exploding right now.

I think moving to formally verify everything is really the next evolution of software engineering and programming languages. It's going to allow us to generate massive amounts of code, much more code than we've ever had before, and allow the AIs and the humans to ensure that it is correct. I think this is possibly the only way that we can move forward and scale the amount of code that we're generating.

In Lean, you write propositions and you write a proof, and you combine that with a name into a theorem. Lean will check the proof for you automatically. If it doesn't compile, the proof is wrong. If it compiles, the proof is right. So you can have AI generate the proof in whatever way, and the proof doesn't have to be pretty. You know that the proof is correct, more or less, though there could be bugs in the Lean proof checking kernel and things like that. You can also have the AI reason about the claims, the propositions. I feel like it'll probably do a pretty good job, but that's possibly an area where human expertise is maybe still very valuable.

Personally, I'm super excited about this for my test suites at work, which are just growing and take 20 or 30 minutes to run. I'm hoping I can shrink that a lot with just a compilation check with Lean.

## Lasm

Lasm allows Lean to run almost anywhere that JavaScript or WebAssembly runs today. That means the web browser, Node.js, and serverless platforms like Netlify, Vercel and Cloudflare Workers, as well as other edge platforms. We have some Bun and Deno support as well. I have been pushing the AI to very thoroughly test it and ensure that we support many, many platforms.

The project is now launched. You'll find it in the [Millillion GitHub organization](https://github.com/Millillion/lasm), and on npm, where you can search for `@lasm/cli` to find it. You basically npm install it, and the only dependency is Node. It takes care of everything else: the Lean toolchain, Clang, LLVM, Emscripten, Binaryen, and all the crazy stuff that gets the Lean C code to compile into Wasm. It's all done for you behind the scenes.

I've been testing it out a little bit myself, with a little Claude Code CLI help, and so far it works. There's a crazy test suite you can check out in the repo, and all kinds of benchmarks. I think we have things for cold starts, memory, requests per second and binary size. I booted up an actual HTTP server in Lean running in Node on my computer, and I was able to curl into it, which is crazy.

I'll be continuing to hone the project, and I plan to add all kinds of different testing methodologies, including working towards formal verification of Lasm itself. It's still a new project that just launched, so open issues if there are problems. I'm going to continue to use it and hopefully begin to adopt it, starting with personal projects, and maybe professionally at the place I work now if it makes sense.

The idea is that you can write your Cloudflare Workers in Lean, or your Express application or your Hono app, and formally verify certain parts of those applications. I'm not super familiar yet with the extent to which you can formally verify them. We have to think about all the asynchronous and concurrent and opaque code, because you can call into JavaScript. When you call from Lean into a JavaScript library like Hono, your formal verification stops at that barrier. But I believe you can pull your authentication code, your business rules and that kind of thing out into pretty pure functions, and then write propositions for those and prove them. The actual HTTP handler code doing the input and output, I don't think you can, though you could verify that to some extent, I believe. I haven't really touched the front end yet, but the AI has told me it's currently an Elm-like architecture. We'll see. I'll be exploring a ton of this to find out the limits and then figure out how to remove them.

I'm super excited. Lean is open for business on many more platforms, where it would have been very difficult to do before.

## How to try it

You just need Node and npm on your machine to get going. I'd probably recommend VS Code and the Lean 4 extension if you want to dive into proof checking on your own, or you can just go for it fully. You could call that vibe coding if you want, but I call it agentic engineering if you are probing the AI and asking it clarifying questions.

When you're doing the formal verification, what you should probably do is really discuss the propositions that Lean has created. Learning the syntax is probably a good idea so you can understand the propositions natively, but I'm not sure it's strictly necessary. You can ask the AI to list out the propositions in plain English and go over them. You could have it triple check, and bump the reasoning up, to make sure the intended behavior is characterized appropriately, with each proposition being individually necessary and the set collectively sufficient.

Join me on this journey. Start learning Lean, start using Lasm, and let's begin to formally verify all software.
