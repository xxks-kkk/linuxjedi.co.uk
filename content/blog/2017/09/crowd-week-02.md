title: [Paper Reading] Crowdsourcing / Human Computation [02]
date: 2017-09-16 12:30 
Category: Crowdsourcing & Human Computation
Tags: crowdsourcing, papers
Summary: CS 395T Human Computation / Crowdsourcing week 02 papers

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