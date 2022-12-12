---
# This template is licensed under a Creative Commons 0 1.0 Universal License (CC0 1.0). Public Domain Dedication.

title: "Mosaik: connecting live coding, e-textile and movement"
author:
  - name: Author one
    affiliation: University of Live Coding
    email: one@livecode.mx
  - name: Author two
    affiliation: University of Bricolage Programming
    email: two@onthefly.ca
  - name: Author three
    affiliation: University of Creative Coding
    email: three@creative.uk
abstract: |
  Replace this text with a maximum 300 word abstract. You'll find it in the
  'metadata block' at the top of your markdown document), be sure that
  each line of the abstract is indented.
fontsize: 11pt
geometry: margin=2cm
fontfamily: libertine
fontfamily: inconsolata
mainfont: Linux Libertine O
monofont: Inconsolata
bibliography: references.bib
...

# Introduction

This paper introduces our collective work "Patterns in between intelligences", a performance piece that builds an improvisational practice between live coding sounds and coding through dance, mediated and shaped through e-textile sensors (do we write about sheffield performance? or the otehr prototypes as well? the sheffield one is not using costumes at all - alex: I guess we can draw on everything we've done so far?), feeding into a networked system of which both live coded processes and human bodies are part.

The project was innitiated as a responce to the funding call by LINK masters to produce an artistic work using Artificial Intelligence. Our multi descipline team: Choreographers and performers, live coders and e-Textile makers gathered together for the attempt to think together how AI could play a role in artistic work, both conceptually and as creative tools.

Through this project we look to challenge mainstream ideas of AI that attempt to emulate human neural pathways as the method of creating new intelligences. Instead, we take a collective view of intelligence. Through a ritualist frame, the spiritual and social dimension of AI is questioned, and machine learning reconnected with ancient patterning techniques. (I am not sure how much we should center the narrative about AI, or creating AI, as our prototypes are not really focusing on that yet -- I think we can describe the aim of our project as this, a non-traditionalist approach to using AI in performance)

The group, initially working under the moniker "Pattern In Between Intelligences" was formed in (September 2020 - is this right?). Through a phase of prototyping, various ideas were trialled which fell under the idea of 

A first iteration of the live performance was debued at No Bounds Festival, Sheffield. The initial grouping of 

[Add an image that shows the project here]


In this performance, 





## Live data flows and time travel

As collaborating performance, textile and live coding artists, working together required us to establish meaningful dataflows and protocols for collaboration. A core problem was how to connect moving bodies with comparatively static actions of live coders, typing at their laptops. With battery-powered, textile-embedded sensors capturing movements, and wireless networking acting as conduit, several problems around how to interpret and respond to the data flows remained.

We focussed on our technological constraints as creative material, and one such constraint was *latency*. Due to our use of machine learning in reducing the sensed dimensions, and other processing delays in our system, there could be a delay approaching half a second before a live coder's work could could connect a sensed movement into a sound triggered by it. We worked with this delay in several different creative ways. [todo: ref https://ccrma.stanford.edu/~cc/shtml/ensDelay.shtml ]

++ is "latency" or "delay" coming from ML? I thought it was mainly from Tidal cycle not using the incoming data as it comes in. >> but use of Tidal is our unique property, so we had to find a way to work with it.

One approach was not to try to reduce the delay, but counterintuitively, to increase and compound the delay. This relied on ideas of patterned repetition and resonance that were already a recurring theme in our discussions. For example, where the piece worked within a metric cycle of 1.4 seconds, and we found a latency of 0.4 seconds, to keep everything in time, we simply had to delay the signal for an additional 1 second. We added additional data 'echoes' of additional cycles, by applying a cycle-length delay line to the data signal, with feedback. As a result, repetitive movements, fit to the metric cycle built up and dissipated over time with the introduction and breaking of the repetition.

++ ah, I actually did not know how it was working inside. nice to know!

## E-textile Sensors: Design decisions
E-Textiles could be used to create soft and flexible sensors that can be worn on body to sense movements. In this performance, we explored textile pressure sensors made of eeontex resistive material to sense bend and stretch of skin or garment as a result of body movements, and capacitive sensor to detect touch or fold of fabric sourface. 
In early prototypes, we forcusted more on pressure sensors palced proximate to body to detect bend/stretch movements of the performers. We used Bela mini board which allows maximam 8 analog sensors per unit. We used them as : 1) direct trigger of a sound, 2) data for Machine Learning to reduce dimentions and use for certain synthesis parameters. 
In the later prototypes, we moved to conductive thead mbroidered capacitive touch sensors on large textile surace (140cm x 280cm, 140cm x 140cm). We used them as 1) direct trigger of a sound, 2) to create data pattern that influence live coding pattern (** Alex, you need to clarify this). When used in this way, it is not about capturing exact motion, but to capture relative positions of the textile surface with the body and motion. 
The proximate pressure sensors are good in capturing prisice movements and produces repeatable data, although for the performers the bend sensors creates the notion of "activation points" and tend to become unwanted framework when choreographing new movements. 
In later prototypes, we moved away from these bend sensors and tried out embroidered capacitve sensors, as they offer more abstract ways to map the data to outcomes. When used with data pattern making, it gave some interesting results, although we notice for the outlooker to map the correspondance between movements and outcome becomes moredifficult and it tend to fall into random. 
Currently we are evaluating each of these e-textile sensor design approeach to decide on the final design including how we would use the data in live coding process.

--I can also include images of pressure/bend sensors from different prototype phase to show variations of design dicisions
-- and maybe image of embroidered line on big textile??

## Establishing rituals


## What is "artificial intelligence" to pattern-makers?

The term "Artificial Intelligence" is notoriously problematic. The word 'artificial' suggests that a human-made machine creates artifice, but in that case, why don't we say that a fan motor creates an 'artificial breeze'? If we consider a heritage technology such as a floor looms for handweaving, they are so culturally situated that you would never say that the textile produced using such a machine is 'artificial'. As a group incorporating creative live coders, likewise we would never say that the work from our collaboration is in any way 'artificial'. The word 'intelligence' is perhaps even more problematic, when the history of measurements of intelligence (IQ tests) is wrapped in the racist ideology of the eugenics movement. While we should be careful in over-romanticising the history of handcrafts, we nonetheless argue that situating intelligence in craft practices demands a less dualistic approach, rather seeing intelligence of mind as inseparable from the intelligence of the body and indeed the collective intelligence of a community of practice.

So while we encorporate contemporary tools in our systems that overtly describe themselves as AI and ML (machine learning) technologies, like dimensional reduction algorithms, pattern recognition systems and neural audio synthesis, our main conceptual interest in AI is in its relation to the heritage algorithms of traditional pattern-making. >> really? I did not notice that we were working on this?!

In essense, many traditional approaches pattern-making are a form of computational creativity. For example in weaving, the tie-ups of shaft looms combine binary sequences through matrix muliplication to create complex, three dimensional structures from simple treddling patterns. This creates very rich creative ground, supporting a traditional and continually evolving practice that still finds new structural techniques despite the technological development over millennia. This human-driven, computational pattern generation is a clear analogue to pattern recognition techniques in AI. The challenge for our collaboration that brings together dance, textile and code artists/technologists is to find ways to develop new technology that is respectful and (to some extent) literally interwoven with such heritage technologies, to create a properly grounded approach to AI.

A definition of artificial intelligence might be useful.. 

I remember scientist that I interviewed sometime ago said "it is a system that can adjust its behavior according to its environment", and I feel I heard this type of explanation few times. Though, I do not know if there is a literatue that we can refer to for the definition.

Maybe we could all have a short reflection on what artificial intelligence means/could mean for our disciplines ++ what we see to be "intelligent" behaviour of a machine/computer/spirit? 

difficulty of working with AI in artistic works >> is it a tool? or a theme/subject matter?
- as a theme/subject matter >> AI is widely discussed/critisized in our society, and we have certain expectation in AI technology (more in SF sense), it is not easy to stage AI if you do not want to "fake" the technology, especially in non-text based (no theater, no narrative) perfromance piece.
- AI tools accessible for creative coders are limited. but also, we do not want to make the piece as cutting edge technology demo. it is not about newest AI technology showcase >> how do we meet the expectation of what we imagine as AI?
- fighting with expectation of "stage magic" >> for spectators, everything that happens on a stage is a spectacle. how do we show/not show the technology behind, especailly when technology is a subject matter?


## Technical Implementation (Rename section) of the Sheffield Prototype (or should we go over all the prototypes?)

The digital print image on the touch sensitive textile were produced using the *disco diffusion* AI image generator. Although textile designer can input prompts, reference styles and initial image to inform compositions and color scheme, the main "drawing" of the pattern was made by AI. Often Ai generated images made mistakes in continuity of the space or giometory which appears as unexpected compositions. Sometimes it generates strange associations of image, that gives us a sensation of looking at a mirror that reflects our interpretations and associations of things. These AI image generation tools can produce many variations of images in relatively short time and can inspire the creative process. But at the end, a human designer needs to create her own interpretations and compositons for these images to work as an artistic piece. In this sense one can say "artificial intelligence" is a powerful tool that supports human creative process but it does not create on its own.

In our first prototype, we used multiple E-textile bend/pressure sensors on each performers body, streaming data sponteneously, for example every 40 miliseconds in our first prorotype. This raw data is very hard to use as control parameters as one needs to monitor many sensors at a time to make sense of these information. Using Machine Learning algorithms to reduce the data dimentions to amount of controll data one needs.  E-textile sensors tend to have historisis and wear-and-tear that one needs to make fine adjustments as the performance proceeeds. Instead, assigning posture as pattern of data and training the Machine Learning tool reduces the necessity of fine tuning and one can expect smoother and more intuitive interaction when controlling parameters. Artificial Intelligence/ Machine learning can provide an intuitive filter for E-Textile sensor interactions.


The sound that was made during the performance was done primarily using the TidalCycles software (McLean 20), for creating music using computer code as the artistic medium. The live coders- Alex and Lizzie- were listening and responding live to the sounds created and updating their codes in response to each other. 

In the opening, before the arrival of the drone, face sensor data was used sending via the zmq protocol. In this, the sensors’ were thresholded so that the movement of the face would lead to different sounds being triggered. Each performer had a set of sounds associated with their sensor. These sounds were generated from an AI model (a Neural Audio Synthesis model called RAVE) that was trained based on the performers recordings of their voices and reconstructed by the model. 

During the performance, live vocals were also used to pass to a real-time version of the model (implemented in the PureData software), which allowed us to manipulate the voice of a human performer and reconstructed as a synthetic voice.  

We also received the data from Mika’s textiles on Alex and my computers via the zmq protocol. This data from the textile was then used in different ways. Both Alex and Lizzie used the data from the textiles separately, to control different parts of the sounds. For example, the touch of the textile could be used as a variable within the code, to control the speed or pitch at which sounds were played back, making the relationship between sound and gesture apparent to the audience.

## Sheffield prototype: content 
(if we refer to this prototype particularly, we could explain the rough outine of the performence?)
- 4 performers with a face sansor each. mouth movements triggering one voice sound.
- scored movement by 2 performers
- drone - narrative of choosing fabric, oracle?
- scored movement, a performer "reading" the fabric
- scored movement, a performer moving in pattern with touch sensor fabric
- speach/ glitch
- rave, climax of the performance, burst of movements by 2 performers and live coded sound, improv (?)
- recede to the end.


## Collective intelligence: Cross-displinary and Collaborative Working

How can interaction with textile work as live coding? 
One of the challenge in this project is how to connect live data input from multiple performers in the live coding process and still make sense as a performance. We tried several approach to explore what makes it feel intuitive and expressive for performers involved, live coders on the real-time production side, and the spectators who do not have the knowledge of the technology behind.

In this project, we encountered issues of how live stream of movement data could be imcorporated in live coding processes. (ok, i notice I can not just write nice sentences... so I make bullet points instead...)
- live input from performer >> timing issue, one does not know if what they are doing is effecting something, 
- is this sensor working? >> feeling of delay or randomness. how do one understand the mapping of interactive systems
- tech demo? or aesthetic? >> obvious interaction vs. complex interaction. how do we make balance between so it stays poetic but understandable?
- chicken or egg? >> who gives the cue to creative decisions? rules given by coders/ design of interface/  choreography and physical performance/ improvisation and liveness. how do we all contribute with creativity as one coherant piece? 

we try to discuss how we cope with these issues in our prototype performance process, or afterthoguths on these... and how we plan to proceed for the final piece production. (ok, this will be great, if we could do this)

## Live coding and Realtime data: Who is coding live?



## Toward a  collective view of intelligence
- comparison to swarm intelligence, like flocking algorithms. >> Neural network is also a type of swarm intelligence (**can we say this?), each participatns of the performance, the performers, live coders, sensor makers collectively create data patterns that emerge. it is up to us to define if this unique pattern is an intelligence or a mear random dots.
- we see the current AI technology and narrative around AI being top-down and technocentric approeach. we use the esotericism/ occultism as our narrative vihecle to critically jaxtapose the two AI approeaches.
- the question still remains: how do one work with technology like AI in artistic context, so that it is understandable and meaningful to their audience? How can one even propose alternative idea or criticism in technology topic? (here, i need some reference or research I feel)

## Acknowledgments

At the end of the Conclusions, acknowledgements to people, projects, funding
agencies, etc. can be included after the second-level heading “Acknowledgments”.


# References
