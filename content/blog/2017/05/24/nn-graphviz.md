Title: Drawing a Neural Network through Graphviz 
Date: 2017-05-23 22:20
Category: tools
Tags: ml, graphviz
Summary: Use NN as an example to show graphviz tricks

## Preface

[Graphviz](http://graphviz.org/) is a language (called DOT) and
a set of tools to automatically generate graphs. It is widely used
by researchers to do visualizations in papers. Essentially, you just
need to provide a textual descritption of the graph regarding its topological
structure (i.e. what nodes are, how they are connected, etc) and Graphviz will
figure out the layout of the image by itself. Usually, the generated layout works
out well but quite often, like this [post](https://hbfs.wordpress.com/2014/09/30/a-quick-primer-on-graphviz/)
mentioned, can be a "finicky beast". So, I decide to share some tips I learned about
Graphviz.

Specifically, in this post, I'll demonstrate how we can draw the Neural Network shown in the 
[last post]({filename}/blog/2017/05/21/andrew-ml-nn.md) and use this as an example
to show some tricks in Graphviz to tweak the layout [^1]. Let's get started!

[^1]: Of course, Graphviz is not the only tool that can produce beautiful pictures. 
[TikZ](http://www.texample.net/) is another popular tool. You can check out 
[its NN example](http://www.texample.net/tikz/examples/neural-network/) for comparison.

## Draw a neural network

If you do a quick search regarding "graphviz neural network example", you'll highly
likely see the below picture:

![]({filename}/images/multiclass_neural_network_example.png) 

This is probably the most simplest Graphviz demonstration on Neural Network. The
code for this picture can be obtained [here](https://gist.github.com/thigm85/5760134).

However, when I'm preparing my last post, I'm not quite satisified with the example above.
I want to clearly label all the nodes in all layers and make distinction among feature
input, bias term, hidden units, and output units. So, I decide to draw one on my own.

Here is the [code](https://github.com/xxks-kkk/Code-for-blog/blob/master/2017/graphviz-drawings/nn3.dot)
that generates the [my blog NN picture](http://zhu45.org/images/nn2.png) [^2]. Let me briefly
highlights some key points in the code:

[^2]: Technically, the code used to generate the blog NN picture is 
[this one](https://github.com/xxks-kkk/Code-for-blog/blob/master/2017/graphviz-drawings/nn2.dot)
but the code I explained above is much more concise.

```{C}
rankdir = LR;
splines=false;
edge[style=invis];
```

1. `rankdir=LR` makes the directed graphs drawn from top to bottom.
2. `splines=false` controls how the edges are represented and in this case, edges 
are drawn as line segments.
3. `edge[style=invis]` forces edges to become invisible. This is a common trick to tweak
graphviz layout. I'll talk more about it in the next section.

```{C}
{
  node [shape=circle, color=yellow, style=filled, fillcolor=yellow];
  x0 [label=<x<sub>0</sub>>]; 
  a02 [label=<a<sub>0</sub><sup>(2)</sup>>]; 
  a03 [label=<a<sub>0</sub><sup>(3)</sup>>];
}
```

1. `node[...]` sets the default node property: specify the node shape, node color. This
node property will apply to three nodes: `x0`, `a02`, `a03`.
2. `x0 [label=<x<sub>0</sub>>]` specify the text label for node `x0`. The text for label
is specified in [HTML-like](http://www.graphviz.org/doc/info/shapes.html#html) and this is 
how we write subscript and superscript in Graphviz.
3. `{...}` specifies the scope of the node property. This code chunk as a whole shows
how we can specify several nodes at the once with the same node property [^3].

[^3]: Check out 
[this SO post](https://stackoverflow.com/questions/28853898/groups-of-nodes-with-the-same-attributes-in-graphviz-file)
for more examples on grouping nodes with the same attributes.

```{C}
{
  rank=same;
  x0->x1->x2->x3;
}
```

## Graphviz tweaks











https://stackoverflow.com/questions/7374108/graphviz-node-placement-and-rankdir

https://stackoverflow.com/questions/27091591/graphviz-dot-vertical-alignment-of-nodes


