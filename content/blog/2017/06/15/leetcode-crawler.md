Title: Python case study: leetcode scraper
Date: 2017-06-15 21:22
Category: programming languages
Tags: python, scraping, beautifulsoup, regex
Summary: a record of python usage appears in the leetcode scraper

It has been many years since 
[last time](http://pages.cs.wisc.edu/~zeyuan/projects/notes/diveintopython/diveintopython.html) 
I touched python. Things get very rusty. Recently, I have been practicing
my algorithm skills on leetcode and I keep all my solutions in a 
[github repo](https://github.com/xxks-kkk/shuati). I want my source file have consistency
formatting shown below.

```
/*
 * [Source]
 * 
 * https://leetcode.com/problems/same-tree/
 *
 * [Problem Description]
 *
 * Given two binary trees, write a function to check if they are equal or not.
 * 
 * Two binary trees are considered equal if they are structurally identical 
 * and the nodes have the same value. 
 *
 * [Companies]
 */

 // Source code begins here ...
```

However, there is one thing keeps annoy me: I have to manually add this header comment
every single time when I finish a problem. So, I ask myself if there is a better way
to make the whole process as much automatic as possible. Python and its famous
[beautifulsoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) library [^1] immediately
comes into my mind.

[^1]: Here is [a good tutorial](http://web.stanford.edu/~zlotnick/TextAsData/Web_Scraping_with_Beautiful_Soup.html) on beautifulSoup.

In this post, I'll highlight some python usage appeared in the script, which costs
me quite some time on googling. Please leave your comment if you find any non-pythonic 
usage. The code script is available 
[here](https://github.com/xxks-kkk/shuati/blob/master/scraper.py). I'll use
[92. ReverseLinkedList II](https://leetcode.com/problems/reverse-linked-list-ii/#/description)
as a demonstration example.

```python
#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
```

The very first thing is "shebang". This is important for our task because
the web page is often written in the unicode (i.e. mathematical symbols).
This shebang will help us avoid unicode & ascii madness. 

```python
from bs4 import BeautifulSoup
import requests
import sys
```

We use a lot of libraries through `import`. If I use *import module*, I have to use quantifier
for any module function call (i.e. `sys.exit()`). By the contrast, I can directly
call the module function if I do *from module import*. This brings a question on
when to use which. Here, I want to quote the explanation from 
[Dive Into Python](http://www.diveintopython.net/object_oriented_framework/importing_modules.html)

> When should you use *from module import*?
>
> - If you will be accessing attributes and methods often and don't want to type the module name over and over, use "*from module import*".
> - If you want to selectively import some attributes and methods but not others, use "*from module import*".
> - If the module contains attributes or functions with the same name as ones in your module, you must use "*import module*" to avoid name conflicts.
>
> The author makes extra remark: Use *from module import \** sparingly, because it makes it difficult to determine where a particular function or attribute came from, and that makes debugging and refactoring more difficult.

```python
script, url = sys.argv
print('url is {:s}'.format(url))
```

I used to really like Python2.7 and not a big fan of Python3. However, with python2.7 EOS,
change must be made. the `print` statement is how we do format printing in python3.

```python
r = requests.get(url)
data = r.text
soup = BeautifulSoup(data, "lxml")
```

Here, I use [requests](http://docs.python-requests.org/en/master/user/quickstart/#make-a-request)
library to fetch the content of the `url` and then feed it into our `BeautifulSoup`
with parser `lxml`.

The next step is to actual scrap the data from leetcode page. The first thing I 
do is to get the question title. Leetcode page has the following structure 
for the question title

```html
   <div class="question-title clearfix">
      <div class="row">
        
        <div class="col-lg-4 col-md-5 col-sm-6 col-sm-push-6 col-md-push-7 col-lg-push-8" id="widgets">
          <div class="like-and-dislike">
            <div id="question-like"></div>
          </div>
          <div class="add-to-list">
            <div id="add-to-favorite"></div>
          </div>
        </div>
        <div class="col-lg-8 col-md-7 col-sm-6 col-sm-pull-6 col-md-pull-5 col-lg-pull-4">
          <h3>
            92. Reverse Linked List II
          </h3>
        </div>
        
      </div>
    </div>
```

As you can see, the question title ("92. Reverse Linked List II") is wrapped around
by the `<div>` tag with class name `question-title`. 

```python
title_corp = soup.find_all("div", class_="question-title")
title_raw = title_corp[0].h3.get_text()
```

So, we invoke [find_all](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#calling-a-tag-is-like-calling-find-all)
method from beautiful soup to find all the `<div></div>` tags with class name `question-title`.
Fortunately, `question-title` class appears only once in the whole html page. 
That allows us to directly access its using `title_corp[0]`. In addition, as you can see
from html source code above, `<h3></h3>` appears only once and it wraps our
problem title. So, we can directly access the content of `<h3></h3>` tags by 
`title_corp[0].h3.get_text()`.

!!!note
    `find_all` returns a "ResultSet" object in beautifulSoup. This object contains
    a set of tags that match with `find_all` function argument criteria. In our case,
    our criteria is `<div></div>` tag with class name `question-title`.

Now, once we have the title string, we want to process it into our desired form.
Our scraper script will go into the 
[leetcode directory of the shuati repo](https://github.com/xxks-kkk/shuati/tree/master/leetcode)
and create the question directory with the format 
"[question number]-[question title in mixed case with the first letter of each internal word capitalized]"
For example, "92. Reverse Linked List II" will lead to a directory 
`./leetcode/92-ReverseLinkedListII`. The source file name is similar to the 
directory name: `reverseLinkedListII.c`. That's what following code chunk tries to achieve

```python
    title_lines = title_raw.split('\n')
    title_lines = list(filter(operator.methodcaller('strip'), title_lines))
    title_rdy = title_lines[0].lstrip(' ').replace(".", "-").split(' ')
    title = "".join(title_rdy)

    path = "./leetcode/" + title
    os.mkdir(path)
```

`title_lines = title_raw.split('\n')` will split the whole text into a list 
of strings with each string being a line of code. In our case, this will give
`['', '            92. Reverse Linked List II', '          ']`.

As you can see our result contains empty string, string with multiple leading
whitespaces, and string with only whitespaces. We need to do some cleanup to keep
only the question title. The first thing we do is to take out the empty string and
the string with only whitespaces. This is done by 
`title_lines = list(filter(operator.methodcaller('strip'), title_lines))` [^2].
[filter](https://docs.python.org/2/library/functions.html#filter) 
creates a list of elements for which a function (the 1st argument of `filter`) 
returns true. `operator.methodcaller('strip')` uses 
[methodcaller](https://docs.python.org/3/library/operator.html#operator.methodcaller),
which applies `strip` function to each element of `title_lines`. The function will
return true only when our string has some characters in it. This will lead to
`['            92. Reverse Linked List II']`.

!!!note
    Here is an example of `methodcaller`: After
    `f = methodcaller('name', 'foo', bar=1)`, the call `f(b)` returns `b.name('foo', bar=1)`.
    In our case, `filter` will apply `operator.methodcaller('strip')` on `title_lines`, which
    is basically `title_lines.strip()`.

Now, we will work on our title string. 
`title_rdy = title_lines[0].lstrip(' ').replace(".", "-").split(' ')` removes
leading whitespace (`lstrip(' ')`) and replace `.` with `-`, and then `split`
our string into words: `['92-', 'Reverse', 'Linked', 'List', 'II']`. We are ready
to form our directory by `join` the words together (`title = "".join(title_rdy)`)
and get `92-ReverseLinkedListII`.

[^2]: This line is found from 
[this SO post](https://stackoverflow.com/questions/8449454/remove-strings-containing-only-white-spaces-from-list). 

Our file name should look like `reverseLinkedListII.c`. This invloves a use of 
regular expression to get rid of `92-` and convert the first character of the rest 
of string into lower case. The code is below

```python
extension = ".c"
pat = re.compile(r"^(\d+)-")
m = re.search(pat, title)
filename=title[:m.start()] + title[m.end():]
filename=filename[0].lower() + filename[1:]
target = open(path+"/"+filename+extension, "w")
```

The regular expression is best illsutrated from a snippet taken from 
[re](https://docs.python.org/3/library/re.html) library

```python
>>> email = "tony@tiremove_thisger.net"
>>> m = re.search("remove_this", email)
>>> email[:m.start()] + email[m.end():]
'tony@tiger.net'
```

`^` matches the beginning of the string and `\d` means numeric digits and `+`
means at least once appearance (of `\d`). Just like official doc snippet above,
`filename=title[:m.start()] + title[m.end():]` removes, for instance, `92-` and
leaves us `ReverseLinkedListII` [^3]. One thing to notice right now is that our
`filename` has object type `str`, which is immutable. This means that we cannot
edit the variable itself. `filename=filename[0].lower() + filename[1:]` is 
a typical way to handle immutable `str` object, which, in our case, lower the 
first character case and append it back to the rest of string.

[^3]: I do a [quick summary](http://pages.cs.wisc.edu/~zeyuan/projects/notes/diveintopython/chap7.html) of
regular expression in python.

The last point needs to notice is `line = line.replace("\r", "").replace("\n", "")`,
which removes carriage return character (`^M`) and linux newline character.

That's it for the leetcode scraper. This is actually the first scraper I have
ever written. It doesn't look hard as it sounds. I think that's majorly because of
the powerful python language and its libraries.