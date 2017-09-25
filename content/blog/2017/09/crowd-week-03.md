title: [Paper Reading] Crowdsourcing / Human Computation [03]
date: 2017-09-25 12:30 
Category: Crowdsourcing & Human Computation
Tags: crowdsourcing, papers
Summary: CS 395T Human Computation / Crowdsourcing week 03 papers

!!!note
    [An introduction to crowdsourcing for language and multimedia technology research](http://doras.dcu.ie/17876/3/pws_crowdsoucing_final.pdf).
    Gareth Jones. PROMISE Winter School 2012. Springer, pp. 132-154.

This paper is centered around using crowdsourcing as a way for data collection. Specifically, it targets 
at language and multimedia technology research, which majorly involves natural language processing and 
computer vision respectively. The paper provides extensive examples of how crowdsourcing can be utilized 
as a way for gathering the data. There are several good points made in this paper. First of all, the 
author provides examples on the definition of crowdsourcing. Crowdsourcing can be applied in various 
fields. Quite often, I have a hard time to come up examples that do not belong to crowdsourcing. The 
example provided by the author is the crowd management at a sports event, in which recruiting more members 
from the crowd is not ideal. The paper also shows the recurring principles in crowdsourcing task design: 
"identify an activity which is amenable to being broken into small elemental tasks". Lastly, the paper 
provides many pointers to the crowdsourcing resources and the papers that focus on the specific area of 
crowdsourcing task design (i.e., Payment and Incentives), which are good for future in-depth study.

There are several questions I want to ask after reading through the paper. I'm still confused about the 
exact mechanism of the quality control of the crowdsourcing task. In the paper, the author states that 
"Once the quality of the work has been checked, the requester then has the option to accept the work and 
make payment to the worker, or to reject it, in which case payment is not made." I'm wondering if the 
requester can exploit this checking-submission mechanism to gather the data while not paying out the 
money. Since the work can be checked, the requester can duplicate the work result and rejected the work. 
Certainly, this will damage the requester's reputation in the long run, but the requester can use this 
mechanism as a way to do budget control. Another question regarding quality control is how we can check 
the quality of the work without traversing all the submission. The paper does not show how RSR task 
handles this issue. One way the author suggests to do quality control is to come up the "honey pots" 
questions, which have known answers to the requester. I'm wondering what fraction of the work that 
contains "honey pots" questions will cause the false positive. Based on my experience with CrowdFlower, I 
feel some "honey pots" questions are too hard to get right. Then, under this situation, how we can 
distinguish between spammers and the workers that actually put the effort into the task.