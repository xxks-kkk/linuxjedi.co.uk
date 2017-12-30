title: [Paper Reading] Crowdsourcing / Human Computation
date: 2017-12-30 12:30 
Category: Crowdsourcing & Human Computation
Tags: crowdsourcing, papers
Summary: CS 395T Human Computation / Crowdsourcing papers reading

[TOC]

## Intro

This post contains reflections for part of the papers I have read in Prof. [Matt Lease](https://www.ischool.utexas.edu/~ml/)'s 
[Human Computation course](http://courses.ischool.utexas.edu/Lease_Matt/2017/Fall/INF385T/).
To get a full list of papers, see the [course schedule](https://docs.google.com/document/d/1f4jN-Cnk9ceVSIyMMvf8yMRu3j6aBxEyemilLvVcBSU/edit).

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

[Back To Top]({filename}/blog/2017/09/crowd-week-01.md)

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

[Back To Top]({filename}/blog/2017/09/crowd-week-01.md)

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

[Back To Top]({filename}/blog/2017/09/crowd-week-01.md)

## "Improving Twitter Search with Real-Time Human Computation"

!!!note
    [Improving Twitter Search with Real-Time Human Computation](https://blog.twitter.com/engineering). Edwin Chen and Alpa Jain. [Twitter Engineering Blog](https://blog.twitter.com/engineering). January 8, 2013.

This article is interesting because it offers a real world example of how we can integrate crowdsourcing into the real production system. 
The problems associated with crowdsourcing are usually related to the performance and latency. Performance often refers to the accuracy
of tasks that crowd workers finish and latency usually measures the amount of time that takes from the tasks start to finish. In the papers
I have read so far, researchers merely come up with good solutions to tackle these two issues and thus, the architecture or the product
that they come up cannot be directly applied in the real world. That's why this article looks interesting because Twitter actually uses
crowdsourcing in their production system. The way that Twitter handles these two issues is centered around the people. Quite often, when
there is a crowdsourcing task, people immediately think about Amazon Mechanical Turk or Crowdflower. However, what Twitter does is that
they use these third-party platforms as backups and they mainly use "custom pool", which contains a group of crowd workers (or "judges") that
are highly specialized to Twitter product scenarios. This solution may look expensive initially because "for many of them, this is a full-time job" 
and thus, I hardly think Twitter just pay around 0.07 dollars for tasks these people finish. However, I think this solution saves a lot of
economics cost. For example, as pointed out in this article, those judges are recruited to handle the short-term search query spike and annotate
the new trend of the search query. This means the latency is the key here: it is not acceptable for a crowdsourcing task spends several hours or days
to finish, which are commonly-seen for standard crowdsourcing tasks through those third party platforms. Furthermore, even the crowd workers fair
quickly, the accuracy of the task result can hardly be guaranteed because crowd workers can possibly misunderstand the meaning of the query due
to the sudden appearance of the trend. From the quality control perspective, we devote a lot of
statistical methods or human intervention to improve the quality of crowdsourcing jobs in a standard setting, which may seem unnecessary for Twitter settings because
those people in the pool are highly-trained professionals. If we think from Twitter perspective, any mistake has the potential to cost multi-million 
advertisement revenue and thus, it is not hard to imagine why Twitter chooses to use their own in-house "turkers".

!!!note
    There is also an article called [Moving Beyond CTR: Better Recommendations Through Human Evaluation](http://blog.echen.me/2014/10/07/moving-beyond-ctr-better-recommendations-through-human-evaluation/), which comes
    from one of the author from above article, is also worth checking out.

[Back To Top]({filename}/blog/2017/09/crowd-week-01.md)

## "Platemate: crowdsourcing nutritional analysis from food photographs"

!!!note
    [Platemate: crowdsourcing nutritional analysis from food photographs](http://www.eecs.harvard.edu/~kgajos/papers/2011/noronha-platemate-uist11.pdf) 
    Noronha, Jon, Eric Hysen, Haoqi Zhang, & Krzysztof Gajos. UIST 2011 pp. 1-12.

The paper is interesting from several perspectives. First, the problem described in the paper is important to tackle. There are plenty of food tracking applications online but many of them 
require the tedious manual logging, which requires a fair amount of effort from the User. Can we make the whole process easier to people? In addition, many HIT design tricks have been mentioned 
in the paper. For instance, when we ask the crowd workers to identify food items in a photo, we may want to provide several examples to them to guide their work. Another trick mentioned is that 
we may need to pay attention to the subtlety of the task design in the sense that we want to break the task into its atomic form. For example, when the authors ask the workers to identify the 
food inside the database, the workers have two tasks mentally: identify the food and locate the food in the database. We want these two tasks carried out separately by different groups of 
Tuckers. One trick to my amusement is to disable keyboard quick selection, which is quite important to prevent "lazy worker" but easy to forget during the task design.

There are also several questions I want to ask. Latency is still a big issue for human computation. Specifically for this paper, the nutrition estimates will return to the user within a few 
hours. In the evaluation section, the average time takes to finish analysis is 94.14 minutes, which is quite long. In addition, this service costs $1.40 per photo, which can cost $1533 per year 
(i.e., three meals per day for 365 days). Given the cost and performance of the tool, I can hardly imagine this application will become popular to a wide audience. This leads to the problem 
caused by the methodology of research. This paper puts heavy weights on the human computation and less on the computer-based algorithmic approach. This is confirmed by the author inside the 
discussion section of the paper. To me, Kitamura et al. really gets close to solving the problem: they can successfully identify whether the photo contains food and the categories of food. The 
major piece left out is to identify the specific foods and the actual intake. I think the former one can be done with computer approach as well and the latter one may invoke crowd sourcing. Doing 
this way may improve the performance of the whole application and reduce the cost of invoking too many crowdsourcing tasks. Furthermore, inside the "Step 1: Tag", the authors mention that "a 
combination of machine and human computation is used to select the better box group" without actually mentioning the exact methodology they use. I'm wondering what exactly the method is. In 
addition, the paper has limitation rooted in Amazon Mechanical Turk. The problem is that only the Americans can use this platform and thus, inevitably, a certain bias will introduce to the 
research. In particular, this paper states that "We chose to require American Turkers due to the unique cultural context required for most elements of the process." In other words, PlateMate is 
only applicable to the food that is well-understood by the American culture, which is partially confirmed by the evaluation photos that the authors use. All those photos contain the food that is 
commonly-seen in the United States. What about the food from other countries with a dramatically different cultural background? Can the component of the food be still easily understood by the 
American-based crowd? In my opinion, the answer is probably no and the nutrition estimate accuracy may drop significantly if we use the tool from different parts of the world. The limit of Amazon 
Mechanical Turk, which seems to be the de-facto standard for crowdsourcing research nowadays, poses the constraint on the research result as well. How do we accommodate this issue is worth to 
think about.

[Back To Top]({filename}/blog/2017/09/crowd-week-01.md)

## "An introduction to crowdsourcing for language and multimedia technology research"

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

[Back To Top]({filename}/blog/2017/09/crowd-week-01.md)

## "ImageNet Large Scale Visual Recognition Challenge"

!!!note
    [ImageNet Large Scale Visual Recognition Challenge](https://arxiv.org/pdf/1409.0575.pdf).

Latency is a big problem in crowdsourcing. Usually, the crowdsourcing tasks will take several days or weeks to finish. Is there any way to speed up the whole process and reduce the latency of the response without sacrificing much on the quality of the tasks? One idea is to build a cache between the application and the crowdsourcing platform, which using the machine learning techniques to identify the similarity between two given tasks and using the crowd to do the optional verification of the two tasks to make sure those tasks are indeed similarly or even the same. Then, we can reuse the task result from the previous to speed up the whole crowdsourcing process. 

ImageNet is a legendary example of crowdsourcing. There is a plenty of media coverage on this challenge. The paper shows how the team from the Stanford compose this benchmark dataset and how this dataset changes the landscape of the computer vision. The essential task of benchmarking dataset is that it has to provide sufficient accuracy so that researchers can use it to train and evaluate their learning algorithms. This necessarily poses a big challenge to the designing of the crowdsourcing task: how do we collect 1,461,406 images and correctly annotate them for different computer vision task? 

One principle is to design the crowdsourcing tasks that targets at specific goals. There are three goals for this dataset: image classification, single-object localization, and object detection. For image classification dataset annotation, we can utilize the voting system for crowdsourcing task. However, for single-object localization annotation, we may want to apply different crowdsourcing principles by making the tasks “as simple as possible” and “has a fixed and predictable amount of work”. In addition, insights from the goal may help us to design the crowdsourcing task better. One example is the authors find out that “different categories require different levels of consensus among users.” For example, the number of crowd workers required to verify cat images is less than the number of crowd workers required for Burmese cat images. This can save the researchers a decent amount of the budget on crowdsourcing tasks. Another example on this matter is the hierarchical algorithm they developed for multi-class annotation. In addition to those details, I find some interesting papers for my future reading on this topic: “Crowdsourcing annotations for visual object detection” and “Scalable multi-label annotation” are interesting to check out. Lastly, the authors compare the machine-based algorithm with the human annotators and show that how human can still beat the computer in the computer vision task. I think it is a strong evidence in showing how good the HPU can be.

For a survey paper like this, some details get omitted but are interesting to ask from crowdsourcing perspective. When the authors evaluate the image classification dataset annotation, they “manually checked 1500 ILSVRC 2012-2014 image classification test set images”. My question is how do they sample those 1500 images? How do they translate 5 annotation errors from those images into “99.7% precision”? In addition, they “visually” check the accuracy of bounding box for single-object localization dataset, I’m wondering if this checking procedure is rigorous enough? Computer is known for its human-unmatched level of accuracy. The bounding box may be good in terms of human eyes but may not be true from computer’s perspective.

[Back To Top]({filename}/blog/2017/09/crowd-week-01.md)

## "Visual Dialog"

!!!note
    [Visual Dialog](https://arxiv.org/pdf/1611.08669.pdf).

Visual Dialog is extremely similar to usual chatbot except that the chat is centered around the images provided. Unlike VQA, visual dialog focuses on the dialogue which requires a list of chat history regarding the picture that both the bot and the human talks about. I play around the live demo of this paper online, and I find that the bot is extremely good at image caption. I uploaded a cat picture looks like below and the bot immediately captions the picture with the title “a cat is standing in a window sill”. However, in terms of the details of the image, the bot seems not really good at it. One question I asked is “what’s inside the sill?” and the bot replied “orange and white”. Then, I asked “How many cats are there?” the bot replied “2”. To me, the bot has difficulty to do object detection correctly and it is really hard for me to keep the conversation going.
One thing I find this paper is really cool is their AMT task design. Before reading this paper, my idea is limited in terms of what kinds of the task that can be performed on Amazon Turk. I have never thought of “hosting a live two-person chat on AMT” and the authors even build their own “backend messaging and data-storage infrastructure based on Redis messaging queues and Node.js”. The interface they design is quite clean and can meet their goal. However, I think they can make this into a game to motivate people to actively get involved in the conversation. Besides the task design, I get a sense of what we should talk about when we collect some data for the paper. Basically, we need to give out the statistics and analysis of the data set by listing out the components of the data set, the distribution of the questions we asked or collected, the answers we got, and so on.

[Back To Top]({filename}/blog/2017/09/crowd-week-01.md)

## "VQA: Visual Question Answering"

!!!note
    [VQA: Visual Question Answering](https://arxiv.org/pdf/1505.00468v6.pdf)

VQA is an AI task that combines the Computer Vision (CV) with the Natural Language Processing (NLP). The user can ask the questions that are best answered based on the image provided. The paper has several interesting points. The first is their crowdsourced task design. The researchers try to pose the questions in a way that can “elicit the most interesting and diverse questions”. One sentence I really like in their “smart robot” interface is “Your task is to stump this smart robot!” I certainly want to come up tricky questions that can beat the researchers’ “evil” robot. From this, I learned that the instruction text also impacts the quality of the crowdsourcing tasks. The goal to the crowdsourcing in this task is to get as many diverse questions as possible. Carefully crafting instruction text is one way, and the other way is to better design the questions appeared in the survey. One trick the researchers use is “when writing a question, the subjects were shown the previous questions already asked for that image to increase the question diversity”. One important idea I learned from this paper is doing the question analysis of the dataset. In the paper when the researchers come up the question answers for the crowdsourcing task, they employ the machine learning technique to compose their “18 candidate answers”. For example, they “gather additional answers from nearest neighbor questions using a bag-of-words model”. In addition to the question analysis, the researchers also study the impact of the task interface design on their data set collected. In Appendix I, the researchers study the spatial relationship between the text and the image. These design practices make me think if there is a way to decide the good strategy of the task design. Statistically speaking, what’s the effective way to design a survey (i.e. crowdsourcing task).

[Back To Top]({filename}/blog/2017/09/crowd-week-01.md)

## "Zooniverse: observing the world's largest citizen science platform"

!!!note
    [Zooniverse: observing the world's largest citizen science platform](http://wwwconference.org/proceedings/www2014/companion/p1049.pdf). Robert Simpson et al., WWW 2014 companion, pp. 1049-1054. 

Zooniverse project looks both similar and different from the crowdsourcing platforms that we have seen so far in the semester. The similarity comes from both the Zooniverse and Amazon Mechanical Turk, for example, involve the data collection. On both platforms, the crowd can “identify, classify, mark, and label” the data. However, Zooniverse is different from AMT in the sense that they “brand” their platform as a place to perform “citizen science”, which can bring much more potential from the crowd than AMT, which is perceived as a place to perform the job and get the money. One example is the “Mutual Muses” project that the crowd is asked to “transcribe Correspondence by  Critic Lawrence Alloway and Artist Sylvia Sleigh”. Surely, on AMT, requesters can still post the tasks that are the same to this. But, branding the data collection process as a citizen science project can make the crowd much more attentive to the work they do. Unlike other crowdsourcing platforms, the Zooniverse takes a holistic approach to the crowd. The projects I have browsed so far do not have “quiz mode” but well-crafted tutorials. The interface design is much more modern and the project itself is “cooler” than the tasks found on the AMT or Crowdflower. One thing I notice that is on the Zooniverse, people are told about the mission of the project but on the AMT, the crowd is barely informed what the data is used for, which makes the platform feel like a place to earn some extra cash not a place to help with research.
The architecture introduction of the Zooniverse platform is uninteresting from the crowd perspective but is definitely worth reading for people who want to build a platform for large-scale crowdsourcing tasks. One point I really like is that the authors are well-aware of “The creation of engaging user experiences is essential to getting the best from volunteers online”, which makes me much appreciated after working with Crowdflower and AMT platforms. Zooniverse’s smooth working process and the mission of the projects make me forget that most of the work I do on the platform is actually without compensation. Near the end of the paper, the authors discuss the potential of the data visualization. I think it is really a great idea especially when the platform treats the crowd not as “workers” but as “researchers”.

[Back To Top]({filename}/blog/2017/09/crowd-week-01.md)

## "Practical Lessons for Gathering Quality Labels at Scale"

!!!note
    Alonso, O. (2015). [Practical Lessons for Gathering Quality Labels at Scale](http://dl.acm.org/ft_gateway.cfm?id=2776778&type=pdf). 38th International ACM SIGIR Conference on Research and Development in Information Retrieval (pp. 1089-1092). 

Alonso (2015) gathers the practical lessons for designing large-scale crowdsourcing task. There are many good tips mentioned inside the paper that are invaluable resources for the crowdsourcing task design. For example, besides the instruction rules, showing examples is a good way to make the crowd worker productive with a meaningful result. Also, the HIDDEN structure proposed in the paper answers my doubts about how to check the performance of the workers if the gold set is missing. In addition, the “honey pots” strategy is mentioned inside the paper and the author uses it as a way to remove incapable workers at the beginning of the task and to perform random checks during the task execution.
Some questions are also worth asking. For example, I am very glad to see that the bias problem gets mentioned by the author in his “data-worker-task” debugging framework. However, how we can handle those bias is a totally different issue and somehow the author does not dive into details. I think that is may be due to the complexity of the issue and the detailed discussion may not fit into the whole framework. However, without some concrete suggestions on how to handle the bias, the proposed framework does not look concrete for me. Another question comes from the comparison between inter-rate static and the percentage agreement. Specifically, I’m wondering what is the drawback of using the percentage agreement statistic? How can we measure whether an inter-rater static is good or bad? Overall, I really like this paper as it provides a very crucial overview on the crowdsourcing task design and it gives a list of questions that we researchers may want to ask during the task design.

[Back To Top]({filename}/blog/2017/09/crowd-week-01.md)

## "Crowdsourcing user studies with Mechanical Turk"

!!!note
    Kittur, A., Chi, E. H., & Suh, B. (2008, April). [Crowdsourcing user studies with Mechanical Turk](http://kittur.org/files/Kittur+2008_CrowdsourcingMechanicalTurk.pdf). In Proceedings of the SIGCHI conference on human factors in computing systems (pp. 453-456).

Kittur et al., (2008) perform an actual user study on the crowdsourcing. Like Alonso’s paper, many tips for crowdsourcing task design give out in the paper: integration of the verifiable questions, minimization of the effort gap between spammers and the good workers, and various ways of detection of the suspect responses. However, the authors in “Crowdsourcing user studies with Mechanical Turk” also carry out the tips they list into two experiments. I'm really surprised to learn how significant the crowdsourcing task design can be on the end result. In addition, the authors also provide some measurements of the crowd we are facing on the platform. Specifically, instead of commonly-believed “widespread gaming”, only a small fraction of people are actually spammers. The rest of the crowd do not have the incentive to finish the task carelessly at the very beginning but might become eventually due to the ill-design of the crowdsourcing task. This observation of the crowd further confirms the importance of the crowdsourcing task design.

[Back To Top]({filename}/blog/2017/09/crowd-week-01.md)

## "Automan: A platform for integrating human-based and digital computation"

!!!note
    [Automan: A platform for integrating human-based and digital computation](http://cacm.acm.org/magazines/2016/6/202648-automan/fulltext).
    Barowy, Daniel W., Charlie Curtsinger, Emery D. Berger, and Andrew McGregor.  Communications of the ACM 59, no. 6 (2016): 102-109.

This paper takes a different angle to look at the crowdsourcing task design, which involves designing a programming language that wraps the crowdsourcing tasks details under function calls. The greatest benefit in doing so is that it provides a unified interface to the programmer so that the programmer does not need to worry about the underlying crowdsourcing task design too much, which makes the whole program portable. In other words, we can tune the configuration of AUTOMAN to make the whole application works for different goals using different crowdsourcing platforms. Another benefit provided by the crowdsourcing programming language abstraction is the better task design experience. Normally, without the abstraction, we may need to design both the task content and also comes up the mechanism to perform the quality control. However, now, with the benefit of function call implementation of the crowdsourcing, we can put all our effort on the crowdsourcing task content design (i.e., Specific questions to the crowd) instead of designing the whole workflow from the beginning to the end, which can save people’s a fair amount of time.
There are still some questions worth asking about the programming language implementation. For example, for the free-text input, the current implementation uses the pattern matching to verify the worker input and perform the probability analysis for the quality. However, there seems no semantic analysis of the response provided by the worker. This reflects one of the shortcomings for the paper’s programming language implementation for the crowdsourcing task: some parts of the crowdsourcing tasks cannot be fully automated as part of the system. In other words, for the free-text input, people still need to go into the actual text to see the semantic meaning of the response. This is especially important when the programming language supports quality control mechanism. Without understanding the meaning of the response, one can hardly assess its quality.

[Back To Top]({filename}/blog/2017/09/crowd-week-01.md)

## "Beyond Mechanical Turk: An Analysis of Paid Crowd Work Platforms"

!!!note
    Donna Vakharia and Matthew Lease. [Beyond Mechanical Turk: An Analysis of Paid Crowd Work Platforms](http://www.ischool.utexas.edu/~ml/papers/donna-iconf15.pdf). In Proceedings of the iConference, 2015. 

The paper provides a detailed comparison among seven crowdsourcing platforms. One noticeable phenomenon I observed in the papers we have read so far is that all of them perform their work on AMT. That makes AMT a de-facto standard for crowdsourcing and human computation research. One possible motivation for researchers using AMT for the work is that AMT is well-understood by the research community. The limitation and functionality of the platform is known to the community and the researcher do not have to go through the platform introduction before jumping into their actual contribution. However, as suggested in the paper, using AMT solely can problematic. One consequence is that the diversity of the research will be limited due to the constraint posed by the platform.  Thus, in order to encourage the community to adopt various crowdsourcing platforms for the research, a survey of existing crowdsourcing platforms is a must and I’m very happy that I can read a paper like this one. Survey of the existing platforms can also provide a practical guide for researchers to pick the platform that is best suited for their goals. For example, we do not have to reinvent the wheels by building some fancy infrastructure for complex tasks on AMT if other platforms like WorkFusion and CloudFactory have already built the tools that can be used out-of-box. However, I think the paper can encourage the researchers to try out different platforms more if it can provide some typical usage scenarios that are best suited for each platform. Some platform like CloudFactory can be quite different from the AMT in the sense that CloudFactory puts more emphasis on the enterprise users than the individual requesters. 

[Back To Top]({filename}/blog/2017/09/crowd-week-01.md)

## "Instrumenting the crowd: using implicit behavioral measures to predict task performance"

!!!note
    [Instrumenting the crowd: using implicit behavioral measures to predict task performance](http://jeffrz.com/wp-content/uploads/2010/08/fp359-rzeszotarski.pdf). Jeffrey Rzeszotarski and Aniket Kittur. ACM UIST Conference, pp. 13-22, 2011.

In the paper, the authors talk about how we can utilize the meta information about MTurk tasks to predict the quality of the work done by the crowd. This is very useful for quality control because we always want to remove the lazy workers from our workforce. That is why we study different quality control techniques throughout the semester. In the paper, the authors think by logging interface data (i.e., mouse, keystrokes, response time), we can predict the quality of the work using machine learning techniques. There are a couple of questions with this method. First, there is a natural latency in making prediction for the quality control purpose. In the paper, the logging data is uploaded via an opt-in button near the end of the task and then they perform all the data mining work backend. However, the spammers are unlikely to submit their logging data to the remote and the data mining work takes time to finish. During the time, the good workers may switch to other tasks. In the paper, the authors think that one prediction model trained for one task can be applied towards the similar tasks. I think it can remove the latency to some degree but it is hard for requesters to distinguish when the direct application of models can work and when the pre-trained models can introduce unseen errors. Second, we cannot remove the bad workers solely based on the prediction result. There is a false positive risk that we may remove the good workers due to the data inaccuracy caused by the “cross-browser compatibility” issue. So, I think the prediction model still belongs to the post-hoc class and it seems ineffective to me that instead of targeting at the work the workers done, we focus on study how each worker behave. However, I think the models proposed in the paper is useful when we handle the data generated by certain workers that fall onto the borderline of deciding whether the work is good or bad.

[Back To Top]({filename}/blog/2017/09/crowd-week-01.md)

## "MmmTurkey: A Crowdsourcing Framework for Deploying Tasks and Recording Worker Behavior on Amazon Mechanical Turk"

!!!note
    [MmmTurkey: A Crowdsourcing Framework for Deploying Tasks and Recording Worker Behavior on Amazon Mechanical Turk](http://arxiv.org/abs/1609.00945).
    Brandon Dang, Miles Hutson, and Matthew Lease. In 4th AAAI Conference on Human Computation and Crowdsourcing (HCOMP): Works-in-Progress Track, 2016. 3 pages. arXiv:1609.00945. 

In the second paper, the authors propose a framework called MmmTurkey that is built on top of the Mechanical Turk, which allows the requesters to easily customize their tasks and at the same time logging the workers’ behaviors. I find the framework looks particularly promising especially for the requesters who want to deeply customize their HIT tasks while keeping track of the workers’ behaviors to perform quality control. I’m curious how exactly the framework works under the hood? Can it replace AMT completely in the sense that I can post the HIT tasks from MmmTurkey interface and wait for the result? I see the paper seems to agree with my thinking but I’m just wondering if there are any corner cases I need to be aware of?

[Back To Top]({filename}/blog/2017/09/crowd-week-01.md)

## "AMAZON'S TURKER CROWD HAS HAD ENOUGH"

!!!note
    MIRANDA KATZ. [AMAZON'S TURKER CROWD HAS HAD ENOUGH](https://www.wired.com/story/amazons-turker-crowd-has-had-enough/). WIRED: BACKCHANNEL. August 23, 2017.

In the first article, the author describes the MTurk and crowdsourcing in general from the workers’ perspectives. The idea is simple: the workers will deliver their best work given a good compensation and transparent communication. The message characterizes the future of the crowdsourcing industry in that MTurk is still has its advantages and the platform will dominate the industry if it can take much more of the workers and make the communication clearer. In addition, the article argues that simply replicating the MTurk with some minor additions to the functionalities will not sustain long in the industry. I agree with the author in that building a reliable platform has to be organization and community driven. This is not saying that academia effort like Daemo is worthless. Academia is very good at building innovative prototypes. However, in order for the platform to be scalable and robust, some large community or organization effort has to come in. From this perspective, MTurk has the clear edge over the other competitors.

[Back To Top]({filename}/blog/2017/09/crowd-week-01.md)

## "The Future of Work: Caring for the Crowdworker Going It Alone"

!!!note
    [The Future of Work: Caring for the Crowdworker Going It Alone](http://www.psmag.com/business-economics/the-future-of-work-caring-for-the-crowdworker-going-it-alone) (blog post). Mary Gray (Microsoft Research), Pacific Standard, August 21, 2015.

The second article shares the big picture with the previous one. On one hand, they focus on the traditional crowdsourcing platforms with microtasks. On the other hand, they expand the crowdsourcing term more broadly to the on-demand sharing economy, which includes Uber, Airbnb as well. This article specifically describes the future of the crowdsourcing platform, which should center around the workers. Compensation is not the only factor that the future crowdsourcing platforms should take care. Third-party registry that allows the workers build their resume and healthcare should be also valued just like the regular 40-hour employees.

## "The Good, The Bad and the Ugly: Why Crowdsourcing Needs Ethics"

!!!note
    [The Good, The Bad and the Ugly: Why Crowdsourcing Needs Ethics](http://www.researchgate.net/profile/Florian_Schmidt12/publication/261126823_The_Good_The_Bad_and_the_Ugly_Why_Crowdsourcing_Needs_Ethics/links/02e7e537c5e2662206000000.pdf). Schmidt, F. A. (2013, September). In Cloud and Green Computing (CGC), 2013 Third International Conference on (pp. 531-535). IEEE.

This paper reminds me of the HPU paper we read very early in the semester. HPU tends to think the crowd like machines, which can work like CPU. However, framing the crowd like this inevitably injecting the impression that the crowd can be treated cheaply. This impression is exactly what the paper tries to address. The paper categorizes the crowdsourcing behaviors based on the crowd’s incentives. Then, the paper studies some platforms and show how they try to exploit their workers’ incentives and treat them cheaply. These three readings make me think that we cannot treat crowdsourcing as a way to get the task done cheaply. We also need to take care of people that make all those great contributions to the advancement of civilization. 

[Back To Top]({filename}/blog/2017/09/crowd-week-01.md)

## "Information Extraction and Manipulation Threats in Crowd-Powered Systems"

!!!note
    Lasecki, Walter S., Jaime Teevan, and Ece Kamar. [Information Extraction and Manipulation Threats in Crowd-Powered Systems](https://github.com/ipeirotis/Mturk-Tracker/). CSCW 2014. 

In this paper, the authors talk about different forms of threats specifically on extracting information from the crowd-based systems and manipulating the systems’ outcomes. One example of information extraction is that the workers can extract the sensitive information (i.e., credit card number) from given picture for an image labeling task. Another example is that if the workers collaboratively mislabel the images, the machine learning algorithm based on the crowdsourced training data can lead to the wrong output. In the paper, the authors present several ways of preventing data leakage. One approach is the division of a task into micro-tasks. The idea is that we do not want each worker to see too much information. However, there can be a consequence of this approach is that the workers may get manipulated by the requesters to do the things that violate their will. One example mentioned by Caverlee is that Iran’s leaders use workers to cross-reference the faces of the citizens with those of photographed demonstrators. The authors further subdivide the information extraction threats into exposure, exploitation, and reconstruction. In addition, they classify the answer manipulation into classic manipulation, disruption, and corruption. Those threats are viewed from the requester's’ perspective. This paper makes me appreciate the importance of the quality control more and we need to pay extra attention to the sensitive information presented in the images. I think we somehow need to run the preliminary check of the data that are put onto the crowdsourcing platform.

[Back To Top]({filename}/blog/2017/09/crowd-week-01.md)

## "Exploitation in Human Computation Systems"

!!!note
    Caverlee, James. Exploitation in Human Computation Systems. In Springer Handbook of Human Computation, pp. 837-845, 2013. 

In this paper, the author surveys the exploitation of the human computation system from three perspectives: workers, requesters, and the system itself. There are many surprising points mentioned in the paper. For example, the division-and-conquer strategy of a task can manipulate workers’ will because each worker cannot see many contexts of the task they work on. In some cases, this can prevent workers leak the sensitive information from the task. For example, if we only allow each worker see three digits number and they cannot infer that they are actually working on the credit card information. However, as mentioned in the paper, people can help the government perform surveillance tasks that against workers’ will. In addition, I’m surprised to know how smart people can utilize the crowdsourcing platform. One example is to use the crowdsourcing platform to manipulate the political views. Another example is that workers can be hired and work collaboratively to manipulate certain task results which hurt their employer’s competitors. Another important issue is also related to the exploitation of the crowdsourcing system. For example, people can organize the workers to post the fake news on the social media to manipulate the public opinions. People spend a lot of effort on detecting the fake news and thanks to this paper, I start to think about how those fake news can be massively spread over different social media platforms in such a quick fashion.

[Back To Top]({filename}/blog/2017/09/crowd-week-01.md)

## "Dirty Deeds Done Dirt Cheap: A Darker Side to Crowdsourcing"

!!!note
    Harris, Christopher G. [Dirty Deeds Done Dirt Cheap: A Darker Side to Crowdsourcing](http://cs.oswego.edu/~chris/papers/harris_c08.pdf). In Privacy, security, risk and trust (passat), 2011, pp. 1314-1317. IEEE.

In this paper, the author talks about the potential that the crowdsourcing system can be used for the unethical purpose. One interesting issue first posed by the paper is how to define unethical. As shown in the paper, different demographic group views the unethical behavior differently. This poses the challenges of policing ethical behavior on the internet. However, I’m very interested to know more how the author might want to model the different unethical behaviors. Another interesting point made by the author is the mention of social engineering. The motivation for social engineering mentioned in the paper is financial gains and identity theft. However, I think this is a big issue especially if we consider the government can utilize the crowdsourcing platform to perform surveillance against the nation’s citizens. This matters people’s privacy and human rights. That leads to another question: How can we prevent the crowdsourcing platform being used to hurt people’s rights. One suggestion made in the paper is by law by stating certain crowdsourcing behavior illegal. However, I think the platform needs to ban out certain tasks to be performed and put those forbidden tasks in the user’s agreement. At the same time, certain supervising needs to perform by the staff members from the platform.

[Back To Top]({filename}/blog/2017/09/crowd-week-01.md)