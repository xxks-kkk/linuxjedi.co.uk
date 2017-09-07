title: [Paper Reading] Crowdsourcing / Human Computation [01]
date: 2017-09-07 12:30 
Category: Crowdsourcing & Human Computation
Tags: crowdsourcing, papers
Summary: CS 395T Human Computation / Crowdsourcing week 01 papers

[TOC]

## Intro

In the following years, I may spend majority of my time reading papers. I figure why
not put my comments here as blog post. I probably need them somewhere and in fact, some
comments are used to facilitate my paper discussion with classmates and reading group members.
I think blog is a nice place to provide fast access and easy archive. Let's get started!

## "The Human Processing Unit (HPU)"

!!!note
    [The Human Processing Unit (HPU)](http://users.soe.ucsc.edu/~orazio/papers/DavisACVHL_CVPR10.pdf) Davis, J. et al. (2010). Computer Vision & Pattern Recognition (CVPR) Workshop on Advancing Computer Vision with Humans in the Loop (ACVHL). 8 pages.

This paper looks interesting because it tries to develop a hybrid framework that, at least conceptually, allows integration between manpower (i.e., 
HPU) and computer power (i.e., CPU). I think the biggest accomplishment this paper has achieved is providing a new perspective to evaluate old 
problems. By directly comparing human with the computer, the authors essentially take a retrospective view on the development of "computer" term, 
which starts out as a way to describe an occupation and then gradually evolved into a term for a specific type of machine. They suggest that it is 
time to view "computer" as a human-integrated electronic device in order to solve the problems that cannot be solved perfectly by the CPU-driven 
computer alone. Their idea of applying old terms in a new context really makes me think whether this paradigm can be applied to other fields of 
research.

However, there are several concerns I want to raise when I read through the paper. One of the contributions claimed in the paper is that 
"characterizing the HPU as an architectural platform". I think the statement is too aggressive. For example, when the authors use color labeling 
task as a way to demonstrate the accuracy between HPU and CPU, I find that essentially they outsource the task that should be done by machine 
learning algorithms to human and CPU just perform some basic statistical work. It seems that the paper suggests us to abandon the use of machine 
learning algorithms for certain tasks and let HPU do the work. I think HPU is a way to improve machine learning algorithms from 90% accuracy to 100% 
accuracy. We still want the CPU-based algorithms to play the major role in the system because the CPU-based algorithm is proved to be stable and low 
latency in a well-tuned production system. In addition, some characterization of HPU cannot be generalized, which prevents people from benchmarking 
HPU against CPU in a straightforward way. For example, the paper shows an empirical study of cost versus accuracy on a specific task, which cannot 
be fully generalized to other scenarios. This makes authors' claim on crowdsourcing as a new architecture for production systems vulnerable because 
there is no clear way to estimate the performance of HPU. Furthermore, many critical questions related to securities and performance need to be 
addressed before we can use HPU in a production system. For example, what would happen if the task sent to the HPU contains confidential information 
and this piece of information is critical for people finishing the task? How do we design the task to workaround this problem? How do we handle the 
problem that HPU can take several minutes, several hours or even several days to finish a certain task? How can we ensure the quality of HPU 
computation result?

## "Soylent: A Word Processor with a Crowd Inside"

!!!note
    [Soylent: A Word Processor with a Crowd Inside](http://projects.csail.mit.edu/soylent/)
    Bernstein, M. et al., UIST 2010. Best Student Paper award. Reprinted in Communications of the ACM, August 2015.

Overall, I think this paper can be treated as a concrete example to support the HPU paper's idea because Soylent uses crowdsourcing to carry out a 
complex but meaningful task: editing, which goes beyond the commonly-seen crowdsourcing task: labeling the training data for machine learning 
algorithms. The tool shows an example of how powerful crowdsourcing can become once we get the HPU and CPU (i.e., word processor) fully integrated. 
One example I really like is about crowdsourced proofreading. Unlike the clueless Microsoft Word message "Fragment; consider revising", with the 
help from the crowd, we can get the meaningful explanation of the mistakes for different errors we make in the writing. This example also surprises 
me because I'm wondering how many crowd workers will take much effort writing out the explanation of the errors. Unlike usual crowdsourcing task, 
which is about clicking several buttons for the survey, writing the explanation can be much more demanding. In addition, I really like the "related 
work" section of the paper because it lists several crowdsourcing examples and I actually want to try some of them: for instance, the HelpMeOut tool 
for debugging code through collecting traces. 

There are a couple of questions and thoughts I want to list out when I read through this paper. One is that I'm wondering how effective the 
Crowdproof will be if we do not pay out any money at all? In HPU paper, the authors use shirt color task as an example to show that there is no 
strong correlation between how much you pay for the crowd and the accuracy you can get from the task. I'm wondering if this statement will hold 
under crowdsourced proofreading setting. In addition, I want to learn more about The Human Macro because one of the design challenges, as pointed 
out in the paper, is to define the task scope for crowd worker. However, from the paper, it seems that all of the responsibility falls on the user's 
shoulder. Is there any way from the system-side that can help the user better tailor their task for the crowd worker? When the authors talk about 
how to prevent the worker from being lazy on the task, they cite a paper by Kittur et al. that says adding "clearly verifiable, quantitative 
questions". I am wondering how can they do that in their system because if they use this methodology, then they must use a way to automate the 
question generation because once the writer triggers the Soylent, the crowdsourcing tasks should be triggered automatically, which requires the 
question gets automatically generated. Question generation can be hard because it needs some level of text comprehension and I am really curious 
what is the type of method the authors use in their system. Also, similar to HPU paper, this paper does not dive into the details of how we can 
tackle the privacy (security) and the latency issues in order to make the system robust in real production.

## "Crowd-based Fact Checking"

!!!note
    Crowd-based Fact Checking. An T. Nugyen.

The big picture of this paper is clear to me. The author wants to automate the process of determining the correctness of claims, which referred as 
fact-checking in the field. Initially, I was confused about how the fact-checking works in reality. However, after browsing through some websites 
listed in the paper, for example, Politifact, the goal that the author tries to achieve becomes clear to me. In addition, I can tell how the author 
knits the crowdsourcing with the machine learning algorithms to develop a hybrid method. Basically, there are two sets of training data that the 
author leverages: one has the journalist label and the other has the label from crowdsourcing. Then the data with journalist label is for the 
off-line scenario, which does not require the machine learning algorithm gives the real-time fact-checking result. Crowdsourcing data is used as a 
way to approximate the journalist "gold standard" in the online scenario, where we trade some level of accuracy for the performance of 
fact-checking. This paper also links to the Soylent paper in the sense that this paper also mentions how to prevent "lazy worker" scenario from 
happening. Specifically, inside "Crowdsourced labels collection", the author requires workers to give an explanation to their label.

My questions for this paper majorly come from the technical perspectives. I have some basic understanding of PGM and BN but clearly, that is not 
enough for this paper. EM algorithm, Gibbs sampling, Variational Inference, softmax are concepts that confuse me the most. In addition, the 
unfamiliarity of the field makes me wonder what exactly is the "independent models" that the author refers to when he talks about the baseline for 
his new model. Those questions lead to a bigger and more generic question regarding research and this course: how should we approach the 
mathematical-dense paper like this in the early phase of the graduate study (i.e., first semester of graduate school)? Hopefully, during the lecture 
this week, we can have some time to talk about this question. In addition to those technical questions, I'm wondering how good the variational 
method works. As mentioned in the "Results" section, the difference between the variational method and the baseline diminishes as more crowd labels 
get collected. This makes me wonder if the new model is really as good as the author claims. Are we paying too much price (i.e., time and 
computational cost) to pursue a mediocre complicated model when a simple model can deliver the similar performance? 



## "Improving Twitter Search with Real-Time Human Computation"

!!!note
    [Improving Twitter Search with Real-Time Human Computation](https://blog.twitter.com/engineering). Edwin Chen and Alpa Jain. [Twitter Engineering Blog](https://blog.twitter.com/engineering). January 8, 2013.

This article is interesting because it offer a real world example on how we can integrate crowdsourcing into the real production system. 
The problems associated with crowdsourcing are usually relate to the performance and latency. Performance often refers to the accuracy
of tasks that crowd workers finish and latency usually measures the amount of time that takes from the tasks start to finish. In the papers
I have read so far, researchers merely come up with good solutions to tackle these two issues and thus, the architecture or the product
that they come up cannot be directly applied in the real world. That's why this article looks interesting because Twitter actually use
crowdsourcing in their production system. The way that Twitter handles these two issues are centered around the people. Quite often, when
there is a crowdsourcing task, people immediately think about Amazon Mechanical Turk or Crowdflower. However, what Twitter does is that
they use these third-party platforms as backups and they mainly use "custom pool", which contains a group of crowd workers (or "judges") that
are highly specialized to Twitter product scenarios. This solution may look expensive initially because "for many of them, this is a full-time job" 
and thus, I hardly think Twitter just pay around 0.07 dollars for tasks these people finish. However, I think this solution saves a lot of
economics cost. For example, as pointed out in this article, those judges are recruited to handle the short-term search query spike and annotate
the new trend of search query. This means the latency is the key here: it is not acceptable for a crowdsourcing task spends several hours or days
to finish, which are commonly-seen for standard crowdsourcing tasks through those third party platforms. In addition, we devote a lot of
statistical methods or human intervention to improve the quality of crowdsourcing jobs, which may seem unnecessary for Twitter settings because
those peole in the pool are highly-trained professionals. If we think from Twitter perspective, any mistake has the potential to cost multi-million 
advertisement revenue and thus, it is no hard to imagine why Twitter chooses to use their own in-house "turkers".

!!!note
    There is also an article called [Moving Beyond CTR: Better Recommendations Through Human Evaluation](http://blog.echen.me/2014/10/07/moving-beyond-ctr-better-recommendations-through-human-evaluation/), which comes
    from one of the author from above article, is also worth checking out.