---
layout: post
author: Chung
date: 2026-09-19
title: "The Token Isn't the Business"
description: "Why blockchain utility almost never makes a token valuable — a back-of-envelope reality check."
permalink: /the-token-isnt-the-business/
---

<p style="font-family:'IBM Plex Mono',ui-monospace,Menlo,monospace;font-size:.78rem;line-height:1.65;color:#8d9298;border-left:2px solid #2743d6;padding-left:1rem;margin:0 0 2.2rem;">Written with AI assistance (Claude). The thesis and reasoning are mine — the AI helped me draft, structure, and stress-test them.</p>

*Why blockchain utility almost never makes a token valuable — a back-of-envelope reality check.*

## Contents

- [The uncomfortable math](#the-uncomfortable-math)
  - [The wire is laid. The current is missing.](#the-wire-is-laid-the-current-is-missing)
- [Why usage doesn't translate into price](#why-usage-doesnt-translate-into-price)
- [The Cisco lesson](#the-cisco-lesson)
- [Real technology is exactly what makes it dangerous](#real-technology-is-exactly-what-makes-it-dangerous)
  - [The imagination test — and why blockchain keeps failing it](#the-imagination-test--and-why-blockchain-keeps-failing-it)
  - [The exception that proves it: stablecoins](#the-exception-that-proves-it-stablecoins)
  - [A regulation for the casino, not the product](#a-regulation-for-the-casino-not-the-product)
  - [So what does this add up to?](#so-what-does-this-add-up-to)
- [Watch it happen in real time: the DTCC case](#watch-it-happen-in-real-time-the-dtcc-case)
- [The NVIDIA (Verifiable Compute) case: why "sounds huge" and "moves the token" are different things](#the-nvidia-verifiable-compute-case-why-sounds-huge-and-moves-the-token-are-different-things)
- [What actually escapes the trap](#what-actually-escapes-the-trap)
- [What would falsify this](#what-would-falsify-this)
- [The takeaway](#the-takeaway)

---

I was a crypto bull. I started investing about ten years ago, early enough to catch the thing before most people were paying attention.

And the pitch was intoxicating. Programmable money. A decentralized, peer-to-peer financial system that cut out the middlemen, disrupted the banks, and handed control back to individuals — and that was only supposed to be the beginning. Back then I was content to own the *promise*. It was still early, so I could rest on potential instead of demanding hard proof of value creation. "Give it time" was a complete argument. And my timing was good — I caught the hype train right before it took off, which felt less like luck than confirmation. Rising prices have a way of validating whatever conviction you brought to them.

Roughly ten years have passed. In technology, ten years is an eternity — long enough for AI to go from research curiosity to something my parents use. And yet: no decentralized revolution to be seen. The middlemen are still here. The banks are fine.

From a pure investment standpoint, Bitcoin remains my single best position to date. But notice what Bitcoin actually claims to be: a store of value and a proof of concept — nothing more. It doesn't promise to *do* much, and its cult status as the original gives it a kind of value that, whatever you make of it, is at least internally coherent. The bold claims belong to everything *else* — the thousands of tokens promising to be the settlement layer of the new economy. Ten years ago, I took them on faith. Ten years later, having learned a thing or two about investing, it's time for an honest look — not the look of a believer waiting to be proven right, but the one question an investor should have asked from the start: *if all of this works exactly as promised, does the token in my wallet actually capture any of the value?*

Which brings me to Hedera. I keep coming back to it as a test case, because it makes some of the boldest claims in the space — technological superiority, enterprise-grade performance, a council of blue-chip corporations. If any "utility token" should have a clean link between real usage and token value, it ought to be this one. And yet I could never understand the *economics* underneath — how all that enterprise activity was supposed to translate into value for someone holding HBAR. This article is my attempt to answer that honestly, using Hedera as the worked example. The conclusion turned out to apply to almost every utility token on the market.

Start with a simple question: what would it actually take, in fundamental terms, to justify its price? Not hype, not momentum — actual economic value flowing to the token. Working through it carefully upends the way most people think about the entire Layer 1 category.

## The uncomfortable math

Hedera is a genuinely capable network. Enterprise-grade, fast, cheap, governed by a council that includes Google and IBM, with real projects in AI auditing and asset tokenization. This is not a story about bad technology.

And this is not a straw man, either. Hedera itself calls HBAR a "utility token" and describes its two jobs plainly: it is the *fuel* that pays for every transaction, and the *stake* that helps secure the network. In Hedera's own words, HBAR's value is tied to its utility and adoption. So asking "does usage actually translate into value for the holder?" isn't imposing a foreign standard — it's taking Hedera's own promise at face value and checking whether it delivers.

Now the numbers. HBAR's market capitalization sits around $3 billion. The network's annual fee revenue — the money users actually pay to use it — is roughly $1–2 million. You could call that a price-to-fees ratio of over 1,000x and move on, but that framing is a trap, and it's worth being precise about why. A high multiple is not itself proof of overvaluation — Bitcoin, which has a legitimate claim to value discussed below, has *no* fees and *no* cash flow at all, an infinite multiple. So the problem with HBAR is not that its fee multiple is high. The problem is more specific: how much of that revenue ever reaches the person holding the token — and whether the revenue is anywhere near big enough to matter.

### The wire is laid. The current is missing.

Here is where a fair look surprised me. It's tempting to say HBAR has *no* mechanism that connects usage to holder value. That isn't true — and it's worth getting right, because the truth is more interesting.

Every fee paid on Hedera is split automatically by the software. Roughly 80% goes to the Hedera treasury, which funds the network's development. About 10% goes to the node operators — the companies running the computers. And about 10% flows into a **staking rewards pot**, which pays out to anyone who has "staked" their HBAR — that is, locked it up to help secure the network. Think of that pot as a sealed jar with a slot on top: fees drip in automatically, rewards drip out to stakers, and — this is the important part — the jar has no key. No one can reach in and take money out, not even the Hedera council. So the plumbing from usage to holder genuinely exists, it runs on autopilot, and it's tamper-proof.

So why doesn't it move the price? Because almost nothing flows through it. Ten percent of $1–2 million is $100,000–200,000 a year. The staking rewards actually being paid out are many times larger than that — they are funded, overwhelmingly, by a separate reserve the treasury put into the jar at the start, not by real fees. Today, genuine usage covers well under 1% of what stakers receive. The rest is a subsidy. And a subsidy has an end date: on current trends, the reserve runs down within roughly a year. When it does, staking rewards fall toward whatever the fees alone can pay — which, at today's volume, is close to nothing.

The wire is laid, in other words. There just isn't any current.

How much current would it take? Run the exercise backwards. For fees alone to fund a meaningful staking yield — and to support today's price on a generous multiple — the network would need on the order of $65–100 million in annual fees, roughly 50 to 100 times what it earns now. What that means in *transactions* depends entirely on what kind: at a fraction of a cent for a simple transfer, it's hundreds of billions of them a year; at a dollar for a smart-contract operation, it's a few hundred thousand a day. The lesson is that raw transaction counts are the wrong thing to watch. Dollars of revenue are the right thing — and those are two orders of magnitude short.

So the honest statement is not "holders get nothing." It is: *holders have a small, automatic claim on network revenue, and that revenue is currently too small to matter — with the clock running on the subsidy that hides the gap.*

## Why usage doesn't translate into price

The mechanism generalizes far beyond one token. There are four structural reasons why network usage fails to drive token prices on most chains:

**Fee payment mostly passes through — it doesn't pile up.** A business buys tokens just-in-time and pays the fee. Most of that fee ends up with people who have real-world bills in dollars: node operators with servers and staff to pay, and a treasury that spends on grants and development. So a large share of what comes in goes back out onto the market. Not all of it, and not immediately — the treasury releases its share on a schedule over months and years, and the staking pot holds its slice until rewards are paid. Delay does help: while usage is *growing*, more tokens sit in that pipeline than come out, and that supports the price. But once usage levels off, the pipeline is full and the effect stops. The only things that take tokens off the market *permanently* are destroying them (a "burn") or locking them for real yield. Delay is a weaker version of that, and Hedera has no burn at all.

**Cheap fees mean cheap demand.** You can move $10,000 in stablecoins across a modern network for a fraction of a cent. A billion dollars of stablecoin volume creates a few hundred dollars of fee demand. The value flows *through* the network without sticking to the token.

**Dollar-priced fees mean usage buys a fixed amount of dollars, not a growing amount of token.** On Hedera, fees are set in dollars and paid in HBAR. That's good for businesses — their costs are predictable. For the token, it means a given level of usage generates a fixed dollar amount of buying, no matter where the price is. That's not bad; it's steady demand. But compare it with a design where fees are set in the token itself: there, a rising price would make every transaction worth *more* dollars of buying, which feeds back into the price. Hedera's design deliberately switches that feedback loop off. Usage supports the price; it doesn't accelerate it.

**Velocity kills holding demand.** XRP's bridge-currency thesis is the cleanest example: even if banks routed billions through XRP, they would hold it for seconds. High velocity means large volumes require only a small, liquid float — not accumulation.

## The Cisco lesson

There is an obvious objection: "But the technology is genuinely useful — tokenization, 24/7 settlement, immutable audit trails. Surely real adoption must lift the token." It's the strongest case the bulls have, and it deserves a real answer.

Here the dot-com era offers a useful analogy — with one honest caveat. Cisco's routers were essential infrastructure for the internet, yet buying Cisco at its 2000 peak was a poor way to bet on the internet's growth: the stock took over a decade to recover even as the internet exploded. But note the caveat, because a careful reader will raise it — Cisco was a *real business* that captured real value; it just couldn't capture enough to justify a bubble price, and much of the surplus flowed to the companies *using* the internet rather than the ones supplying its plumbing. Hold both halves of that. Infrastructure can be a genuine business *and* still be a bad investment when it's overpriced and when most of the value it enables is captured downstream. A token is a harder case than Cisco, not an easier one: Cisco at least had earnings and a claim on them. Most fee tokens have neither.

Blockchains solve business problems: settlement gets faster, audits get cheaper, assets become tradable around the clock. But that value is captured by the bank that saves costs, the issuer that reaches new investors, the platform that operates the product. The token is necessary for the system to run — but necessity is not scarcity, and scarcity is not a claim on cash flows. You need electricity to run the internet too; that never made utilities a leveraged bet on tech.

## Real technology is exactly what makes it dangerous

There's a reflex, when someone questions a token, to answer: "But the technology is real." Tokenization is real. On-chain settlement is real. AI audit trails are real. The reflex assumes that conceding the technology ends the argument in the token's favor. It does the opposite — and seeing why requires two ideas that sit at the center of how markets actually price things.

The first is the gap between value and price. The *value* of an asset rests on earning power — what the underlying business or technology can actually produce. The *price* rests on psychology: how people feel, on a given day, about that earning power. The tell is that price swings far more violently than any business's fortunes ever do. A company's real prospects do not change by 5% between Tuesday and Wednesday, yet its stock routinely does. That gap between slow-moving value and fast-moving price is where both opportunity and danger live. And for an asset whose link between usage and holder carries almost nothing — the entire subject of this article — price is left resting on *almost pure* psychology, which is exactly why token swings are so extreme in both directions. There is little earning-power anchor to pull the price back.

The second idea is Howard Marks's, from his December 2025 memo *Is It a Bubble?* Not all bubbles are alike. Some — the South Sea Company, subprime mortgages — are *mean-reversion* bubbles: manias with nothing durable underneath, which inflate, burst, and leave only losses. Others form around genuine turning points — railroads, the internet, now AI — which Marks calls *inflection* bubbles. These are built on something real; the technology does change the world. And here is the trap he names: an inflection bubble can *still* destroy the capital of the people who funded it, even as it transforms society. The mania has a social function — without irrational sums flooding into chip fabs, data centers, and infrastructure, that infrastructure wouldn't get built — but the investors who foot the bill are frequently not the ones who profit. Marks's question is whether you end up a *winner* of the future, or merely the *fuel* that powers the transition.

Now the two ideas combine into something sharper than either alone. Marks's split describes *technologies*. But a token is not a technology — it is a financial instrument bolted onto one. So blockchain-the-technology could be a genuine inflection, as real as the internet, *and the token could still behave like a mean-reversion vehicle* — because the value accrues to the enterprises, operators, and consortiums using the rails, not to the token that fuels them. Grant the maximal bull case in full: none of it tells you whether the token holder is a winner or the fuel. The railroad remade the world; most railroad investors were wiped out. The internet remade the world; the median dot-com share went to zero. Being real is not the same as paying you.

### The imagination test — and why blockchain keeps failing it

If captured imagination is what inflates a bubble, it's worth asking what *captures* it. The answer is legibility: a tangible, first-person demonstration a person can grasp in seconds. AI had that moment. ChatGPT let anyone type a sentence and feel the magic instantly — no explanation required. That visceral, universal, self-evident demonstration is precisely what fires the imagination of infinite possibility that Marks describes. The technology is real, the demonstration is real — and yet the *investments* may still be irrational, because "this is real and astonishing" tells you nothing about what returns it will earn or who captures them. Real, astonishing, and unpriceable can all be true at once. That is the AI situation in one line.

Blockchain has never had that moment — and its very design suggests it may not get one. Its core promise is a *backend* property: removing intermediaries, reconciling ledgers without a trusted middle. But nobody has a spine-tingling experience watching a settlement layer avoid a middleman. You cannot demo decentralization the way you can demo a chatbot. The value, such as it is, happens invisibly, in the plumbing, in a mechanism most people can neither see nor explain. A technology that operates in the background, resists intuitive explanation, and offers no legible "wow" at first contact is poorly equipped to capture mass imagination — and mass imagination is the fuel a durable, sustained re-rating would require.

Be precise about the claim, because it's easy to overstate. Blockchain has certainly had *speculative* imagination moments — the 2017 ICO frenzy, the 2021 NFT mania. What it has never had is a *utility* moment: a mainstream, legible demonstration of everyday usefulness. And that distinction is itself the evidence. The manias it has produced were financial, not functional — which is exactly the signature of a mean-reversion bubble rather than an inflection one. The excitement attached to the *instrument*, not to any experience of the *technology*.

### The exception that proves it: stablecoins

There is one genuine counterexample, and it's worth meeting head-on, because it ends up strengthening the case rather than weakening it. Blockchain does have one clear killer app: stablecoins. For someone in Argentina, Turkey, or Nigeria, holding digital dollars is viscerally, immediately useful — real product-market fit, felt in the first ten seconds, the closest thing the space has to its own ChatGPT moment.

And it is precisely the case where the underlying chain's token captures *nothing*. You transact in dollars; the network's token earns a dust-level fee that passes straight through. Recall the Open USD consortium — Visa, Mastercard, BlackRock, Stripe and more than a hundred others — structured so the *members* collect the reserve yield. Blockchain's one undisputed success is the sharpest possible illustration of this article's thesis: enormous real utility, delivered on-chain, with essentially none of the value flowing to the token the chain is sold on. The killer app exists — and it kills the investment case rather than making it.

### A regulation for the casino, not the product

Regulation fits the same pattern. Take the CLARITY Act — the big US bill meant to give crypto a proper rulebook. It passed the House in 2025 and, as of this writing, is still working its way through the Senate. Bulls have treated its progress as validation. But look at what it would actually do. It decides *which regulator* oversees a token and under *which label* — security or commodity — based largely on how decentralized the network is and how the token was originally sold. It is a rulebook for how tokens are classified, traded, held in custody, and disclosed.

Notice what is entirely absent: any requirement that a token deliver value, generate revenue, or return anything to the people who hold it. It regulates the *market in tokens*, not the *usefulness of tokens*. It would make trading safer, more legitimate, and better-plumbed — a genuine gift to exchanges and traders — while saying nothing about whether any of these instruments actually does something. There's even a perverse twist: because a token would earn lighter-touch treatment by appearing sufficiently *decentralized*, the law quietly rewards the *appearance* of decentralization over its substance — which matters, because a look under the hood of most "decentralized" networks finds control far more concentrated than the story admits.

### So what does this add up to?

Put the pieces together and the shape of the risk becomes clear. Tokens carry the profile of a mean-reversion bubble wearing an inflection costume: a financial instrument that's easy to trade, resting on a technology whose real value is unproven, largely invisible, and — crucially — barely captured by the instrument itself. That combination can absolutely produce a spectacular ascent when enthusiasm peaks; thin anchors don't cap upside, they remove the brake. But the same thinness cuts the other way. A stock has earnings to fall back on; gold has thousands of years of habit; a fee token with near-zero revenue reaching holders has neither — so when sentiment turns, there is very little underneath to say "this is too cheap." That doesn't make a crash *certain*. It makes the price fragile: quick to rise on belief, and with no natural floor when belief fades. The rise and the fall are symptoms of the same missing thing.

## Watch it happen in real time: the DTCC case

If that still sounds theoretical, here is the Cisco lesson playing out right now, at the very heart of the financial system.

DTCC is a company most people have never heard of, yet almost every US securities trade passes through it. It is the post-trade plumbing of Wall Street — the institution that actually records who owns which share, custodying assets worth tens of trillions of dollars. When DTCC moves, it is not a pilot project; it is the market itself.

And DTCC is now moving decisively into tokenization. Its new Tokenization Service, developed with more than fifty major firms, puts traditional securities on blockchain rails in live production: the tokenized asset carries the same identifier and the same legal rights as its traditional twin, and it can move between participants around the clock. For the tokenization *trend*, there is no stronger validation imaginable.

Now look at the choices they made — because this is where the token thesis dies quietly:

**Which blockchains?** DTCC built its own permissioned chain on Hyperledger Besu — free, open-source software with **no token at all** — and added connections to two institutionally-oriented networks. None of the famous "enterprise blockchain" tokens that retail investors hold made the list. The most important tokenization initiative in finance runs, at its core, on rails with no public token in the value chain.

**Who keeps the economics?** DTCC and its member firms. The tokenized securities carry the same rights and fee structures as before. Blockchain here is a better database, not a wealth transfer to token holders.

**And read the feature list:** DTCC's tokens come with built-in powers to force-transfer, claw back, pause and freeze assets. This is regulated finance wearing blockchain clothes — the exact opposite of the censorship resistance that crypto tokens sell as their core value. Institutions did not adopt crypto's rules; they took the technology and left the tokens behind.

So when you read headlines that "Wall Street embraces tokenization" and feel the urge to buy the tokens of "enterprise blockchains" — pause. Wall Street *is* embracing tokenization. It is simply doing it in a way that routes around those tokens entirely.

## The NVIDIA (Verifiable Compute) case: why "sounds huge" and "moves the token" are different things

No example tests this article's argument better than the one crypto headlines love most: Hedera, NVIDIA, and AI.

Here's the setup. A company called EQTY Lab, working with NVIDIA and Intel, built something called Verifiable Compute. The problem it solves is real and increasingly urgent: as AI systems make more decisions — approving loans, guiding medical tools, running government services — regulators and courts want proof of what an AI actually did. Which model ran? On what data? Did anyone tamper with it? New laws like the EU AI Act are starting to *require* this kind of accountability.

Verifiable Compute answers that by turning the AI chip itself into a notary. When an AI model runs on a supported NVIDIA or Intel chip, the hardware generates a cryptographic "certificate" — a tamper-proof receipt of exactly what was computed. That receipt is then timestamped and recorded on Hedera, creating a permanent, unalterable audit trail. Think of Hedera here as a public register office: it doesn't perform the AI work, it stamps and files an entry proving the work happened, and when.

Why Hedera for this? There are real reasons, to its credit. It settles records in seconds at a fixed, sub-cent cost, so an enterprise can budget its compliance bill without it spiking when the network gets busy. Its underlying design produces trustworthy timestamps — which matters enormously when the whole point is proving *when* a computation happened. And it's governed by a council of large corporations rather than an anonymous crowd, which makes regulators and government buyers comfortable. But note the ceiling on that praise: the actual trust is rooted in NVIDIA's and Intel's hardware — the chip does the cryptographic heavy lifting. Hedera is the filing cabinet where the receipts are kept. A well-built filing cabinet, chosen for good reasons — but a filing cabinet, and one that a vendor could swap for another (as DTCC did with its own no-token chain).

This is genuinely impressive, and it's moving into real deployments — NVIDIA's newest Blackwell chips, pilots with Accenture, demonstrations for government use. When you read "NVIDIA + AI + Hedera," the excitement is understandable. If every AI computation on Earth had to be notarized on Hedera, surely HBAR must go to the moon?

Here's where you have to separate two questions that feel like one: *Is this a big deal for the world?* and *Does this force value into the HBAR token?* They have different answers.

Recall what HBAR does in this picture. Recording each AI receipt on Hedera requires a small payment, and that payment is made in HBAR — HBAR is the postage stamp on that filing. And this is the cheapest letter the network sends: a plain receipt costs a fraction of a cent. That's HBAR's entire job here. It isn't the AI, isn't the chip, isn't the data — it's just the stamp used to file the record.

Now do the arithmetic. Suppose this became a global standard and notarized an almost unimaginable **one trillion** AI operations per year. At the network's fee of roughly $0.0008 per receipt, that's about **$800 million** a year in fees — a trillion stamps at a fraction of a cent each. A staggering-sounding number, until you remember three things from earlier in this article.

First, that $800 million is a *yearly flow*, which works out to roughly $2 million of token-buying per day — against HBAR trading volume that already runs many times higher. It would be a ripple inside normal daily churn, not a wave.

Second, engineers build systems to *avoid* generating that many fees. You don't file a trillion separate entries; you bundle thousands of computations together and file one combined fingerprint. Real-world designs are built to minimize exactly the transaction count the bullish case needs to be enormous.

Third, and decisively: remember where that fee money goes. Most of it lands with node operators and the treasury, who spend or sell it over time. Only about a tenth drips into the staking pot for holders — and even that is capped by how much the network pays stakers. Nothing is burned. The token passes through the register office; a small slice stays behind for stakers, and the rest comes back out.

So the honest verdict: Verifiable Compute is real, important, and a genuinely strong story for Hedera's relevance. It may well drive the *price* — by making the narrative irresistible to investors, exactly as this article describes. What it does *not* do is mechanically force value into the token through usage. The world gets a notary for AI. NVIDIA sells more chips. EQTY and Accenture win contracts. And HBAR holders get what they always get: a more exciting story to be long of.

## What actually escapes the trap

To be fair, not everything fails this test equally:

**Tokens with real burn or buybacks.** Ethereum destroys part of every fee, so heavy usage mechanically reduces supply. Some protocol tokens use revenue for buybacks — the closest crypto gets to a shareholder-like claim. The transmission mechanism exists, even if valuations still price in enormous growth.

**Bitcoin — by refusing to play the game.** Bitcoin makes no utility claim at all. Its thesis is monetary: fixed supply, no company, no council, no treasury, sixteen years of survival. You can reject that thesis, but it is internally consistent in a way "fee token as growth stock" is not. The DTCC case even sharpens it: if institutional blockchains are freezable and clawback-able by design, an asset nobody can freeze becomes *more* distinct, not less. Notably, it is the same logical structure as the case for gold — scarcity against monetary debasement — without the industrial floor and without five millennia of track record.

**Isn't Bitcoin "just a story" too?** A fair reader will ask this, and it deserves a straight answer, because this article has leaned hard on the word "story." Yes — Bitcoin's value rests on a shared belief. So does gold's. So does every currency's, and most of the value of every stock above its liquidation price. Almost everything people hold wealth in is, at bottom, a story people agree on. So "it's a story" can't be the criticism. The real question is: *how durable is the story — and who has the power to break it?*

A durable story is one that no single party can change and that doesn't depend on a promise still waiting to be kept. Bitcoin's story is "21 million coins, ever, and no one can alter that." It's tied to the structure of the thing, not to anyone's future performance. Nobody has to deliver anything for it to stay true. A fragile story is one that depends on future results and sits under someone's control. HBAR's story is "enterprise adoption will create value for holders" — a promise that still has to be fulfilled, running through rules a council can revise. That is the difference. It isn't that Bitcoin has a *better* story; it's that its story is harder to break and needs no one to keep it alive. Judged by the same yardstick, the two come out in different places.

## What would falsify this

An argument that no evidence could refute is not an argument — it's a mood. So it's worth being concrete about what would break this thesis, because a fair reader deserves to know it's falsifiable.

The thesis fails if HBAR's price appreciates *durably* while real revenue to holders rises with it. And there is now a clean way to watch for that. Take the fees that actually flow into the staking pot from genuine usage, and divide by the staking rewards actually paid out. Call it the **reward-coverage ratio**: it tells you what share of holders' rewards is earned by the network versus subsidized from a reserve. Today it sits well under 1%. If that number climbs steadily toward 100% over the next one to two years — driven by fees, not by cutting rewards — the wire is carrying real current and this article's core claim is wrong.

Two supporting signals sharpen the picture. First, watch *dollar* fee revenue by type: are the high-value operations (smart contracts, tokenized-asset settlement, at up to a dollar each) growing faster than the sub-cent logging? A real business emerges from the expensive transactions, not the cheap ones. Second, watch the reserve that currently subsidizes rewards. It is draining, and on current trends it runs low within about a year. That gives the question a deadline: either fees rise by roughly a hundredfold to take over, or staking yields fall toward zero. Whichever happens, both sides of this debate will find out.

The strongest exhibit here deserves its own honest qualifier. The trend of institutions routing around public tokens is real *so far*, but it is not a law of nature. Some tokens are visibly moving toward value capture — Ethereum burns fees, and a handful of newer protocols buy back and burn from real revenue. The spectrum runs from "pure story" to "genuine cash-register claim," and each token belongs on it individually rather than lumped under three examples. The argument is about where *most* of today's utility tokens sit, and about HBAR specifically — not that value capture is impossible for any token, ever.

## The takeaway

For most utility tokens, the honest summary is this: the price is set almost entirely by investment and speculative flows, because the revenue that reaches holders is too small to matter yet. The link between network usage and token value isn't absent — it's thin, and it carries almost nothing. Real adoption makes the *story* more credible, and the story attracts capital. That can absolutely produce spectacular returns in a cycle.

But know which game you are playing. When you buy a fee token, you are not buying the cash register. You are buying the story about the cash register — and stories are repriced by belief, not by earnings.

Ask two questions before buying any token. First: *if this network succeeds beyond all expectations, what is the mechanism that carries value to this specific asset — and how much would it actually carry?* Second: *how durable is the story, and who can break it?* If the honest answer to the first is "a trickle," and to the second is "a promise that still has to be kept, under someone else's control," then you are speculating. That is a legitimate activity — as long as you size it, and name it, accordingly.

---

*This article reflects my personal analysis and is not investment advice.*

---

## Sources and further reading

**Howard Marks, *Is It a Bubble?* (Oaktree Capital, December 9, 2025)** — the mean-reversion vs. inflection bubble distinction and the "fuel vs. winner" framing.
- Memo: https://www.oaktreecapital.com/insights/memo/is-it-a-bubble
- Full text (PDF): https://www.oaktreecapital.com/docs/default-source/memos/is-it-a-bubble.pdf

**DTCC tokenization** — the securities-tokenization service, its multi-chain approach, and the SEC no-action relief.
- DTCC Digital Assets — Tokenization: https://www.dtcc.com/digital-assets/tokenization
- DTCC advances tokenization service, convenes 50+ firms (May 4, 2026): https://www.dtcc.com/news/2026/may/04/dtcc-advances-development-of-new-tokenization-service
- DTCC authorized to offer tokenization service — SEC No-Action Letter (December 11, 2025): https://www.dtcc.com/news/2025/december/11/paving-the-way-to-tokenized-dtc-custodied-assets
- DTCC + Digital Asset on the Canton Network (December 17, 2025): https://www.dtcc.com/news/2025/december/17/dtcc-and-digital-asset-partner-to-tokenize-dtc-custodied-us-treasury-securities
- DTCC connects tokenization service to Stellar (May 27, 2026): https://www.dtcc.com/news/2026/may/27/tokenization-service-to-connect-with-stellar-public-blockchain-as-dtc-advances-multi-chain-strategy

**EQTY Lab / NVIDIA / Intel — Verifiable Compute** — the AI-notary framework anchored on Hedera.
- Verifiable Compute overview (EQTY Lab): https://vcomp.eqtylab.io/
- Launch announcement (Business Wire, December 18, 2024): https://www.businesswire.com/news/home/20241218897420/en/EQTY-Lab-Intel-and-NVIDIA-Unveil-Verifiable-Compute-A-Solution-to-Secure-Trusted-AI
- Deployment on NVIDIA Blackwell, with Accenture and Hedera (EQTY Lab, July 10, 2025): https://www.eqtylab.io/blog/blackwell-announcement
- Hedera's own writeup: https://hedera.com/blog/eqty-labs-verifiable-compute-brings-trust-to-ai-with-hedera/

**Hedera fee distribution and staking** — the automatic 80/10/10 fee split and the keyless staking-rewards account.
- Network accounts (Hedera docs): https://docs.hedera.com/hedera/core-concepts/accounts/network-accounts
- Staking program (Hedera docs): https://docs.hedera.com/learn/core-concepts/staking/staking
- HIP-1259, Fee Collection Account: https://hips.hedera.com/HIP/hip-1259.html
- Native Staking Phase 1 (Hedera blog): https://hedera.com/blog/introducing-native-staking-phase-1-on-the-hedera-network/

**CLARITY Act (Digital Asset Market Clarity Act of 2025, H.R. 3633)** — the US market-structure bill classifying tokens by decentralization and sale. Passed the House July 2025; pending in the Senate at the time of writing.
- Bill text (Congress.gov): https://www.congress.gov/bill/119th-congress/house-bill/3633/text
- Congressional Research Service overview: https://www.congress.gov/crs-product/IN12583

**Open USD (OUSD)** — the multi-partner stablecoin consortium referenced on stablecoin value capture.
- Coverage varies; see reporting on the Open Standard / Open USD launch for consortium structure and reserve-yield sharing.

*Note: some of these initiatives are evolving; dates and details reflect reporting available at the time of writing. Verify the latest status before relying on any specific figure.*
