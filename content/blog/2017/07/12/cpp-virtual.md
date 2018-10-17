Title: Virtual methods and polymorphism in C++
Date: 2017-07-12 23:11
Category: programming languages
Tags: cpp
Summary: virtual, pure virtual, constructors, abstract base class

[TOC]

Surprisingly, even I work with the product that is written majorly in C++, I don't have to deal
with the stuff that differentiate C++ from C. However, I'm now working on a defect that
forces me to simplify C++ objects in order to get the root cause of the problem. That's the place
where I have to really need to know how exactly C++ class is structured. 

One question I asked myself several years ago: "What is virtual method in C++?" I believed, at that time,
I got the answer but I was too lazy to record it somewhere. Now, I have to pay the price by wasting my effort
again to dig out the answer. So, I'd better save it at someplace this time and the following is just
a simple example to partially show the answer to the question. I know C++ is a monster and I'll definitely
need to rewrite the post some day in the future when I know more about the language. However, this answer
is good enough for me now.

## Virtual methods

Let's consider the following code snippet: we have a base class called `Animal` and its subclass called `Dog`

```c++
#include <iostream>
using namespace std;

class Animal{
public:
  void getFamily() { cout << "We are animals" << endl; }
  void getClass() { cout << "I'm an Animal" << endl;}
};

class Dog: public Animal{
public:
  void getClass() { cout << "I'm a Dog" << endl;}
};

int main()
{
  Animal *animal = new Animal;
  Dog *dog = new Dog;

  animal->getClass();
  dog->getClass();
}
```

Now, inside the `main`, we call `animal->getClass()` and `dog->getClass()`. We compile our code 
using `g++ -std=c++11 a.cpp` and run the program and get

```
I'm an Animal
I'm a Dog
```

As you can see, each object calls their `getClass` method respectively.
Now, let's add a function called `whatClassAreYou()` to our code above 

```c++
void whatClassAreYou(Animal *animal)
{
  animal->getClass();
}
```

and in our `main` function, we call our newly-added function with

```c++
whatClassAreYou(animal);
whatClassAreYou(dog);
```

and the output looks like below

```
I'm an Animal
I'm a Dog
I'm an Animal
I'm an Animal
```

As you can see `whatClassAreYou()` only calls the `getClass()` method of our base class `Animal` even when we pass in 
`Dog` class object. Ideally, we want our `whatClassAreYou()` method call the right `getClass()` method depending on
what class object we pass into. In other words, if our `Dog` class implements its own `getClass()` method, we want
our `whatClassAreYou()` method be aware of this fact and call it instead of calling `getClass()` of our base class `Animal`.
That's why we want to add `virtual` keyword to the `getClass()` of our base class. We are essentially telling the compiler
that our base class `getClass()` method might be overridden by its subclass and be aware of this fact when some other method
wants to call it.

Now our code looks like below

```c++
#include <iostream>
using namespace std;

// Virtual Methods and Polymorphism
// Polymorphism allows you to treat subclasses as their superclass and yet
// call the correct overwritten methods in the subclass automatically

class Animal{
public:
  void getFamily() { cout << "We are animals" << endl; }

  // When we define a method as virtual we know that Animal
  // will be a base class that may have this method overwritten
  virtual void getClass() { cout << "I'm an Animal" << endl;}
};

class Dog: public Animal{
public:
  void getClass() { cout << "I'm a Dog" << endl;}
};

void whatClassAreYou(Animal *animal)
{
  animal->getClass(); // use "virtual", proper getClass() method will be called depending on
                      // the exact type of Animal* animal get passed in (i.e. base class Animal
                      // or subclass Dog)
}

int main()
{
  Animal *animal = new Animal;
  Dog *dog = new Dog;

  // If a method is marked virtual or not doesn't matter if we call the
  // method directly from the object
  animal->getClass();
  dog->getClass();

  whatClassAreYou(animal);
  whatClassAreYou(dog);
}
```

and the output is

```
I'm an Animal
I'm a Dog
I'm an Animal
I'm a Dog
```

The reason behind this scenario is what we called **polymorphism**, which means "many form" in Greek. Here is how this
concept get explained in [C++ Primer](https://www.amazon.com/Primer-5th-Stanley-B-Lippman/dp/0321714113):

> We speak of types related by inheritance as polymorphic types, 
> because we can use the “many forms” of these types while ignoring the differences among them. 
> The fact that the static and dynamic types of references and pointers can differ is the cornerstone of how C++ supports polymorphism.

> When we call a function defined in a base class through a reference or pointer to the base class, 
> we do not know the type of the object on which that member is executed. 
> The object can be a base-class object or an object of a derived class. 
> If the function is virtual, then the decision as to which function to run is 
> delayed until run time. The version of the virtual function that is run is the 
> one defined by the type of the object to which the reference is bound or to 
> which the pointer points. On the other hand, calls to nonvirtual functions are 
> bound at compile time. Similarly, *calls to any function (virtual or not) 
> on an object are also bound at compile time*. 
> The type of an object is fixed and unvarying—there is nothing we can do to 
> make the dynamic type of an object differ from its static type. 
> Therefore, calls made on an object are bound at compile time to the version defined by the type of the object.

!!!Note 
    Virtuals are resolved at run time only if the call is made through a *reference* or *pointer*. Only in these cases is it possible for 
    an object’s dynamic type to differ from its static type.

To see the final note of the above quote, let's take a look an example

```c++
#include <iostream>
using namespace std;

class Animal{
public:
  void getFamily() { cout << "We are animals" << endl; }
  virtual void getClass() { cout << "I'm an Animal" << endl;}
};

class Dog: public Animal{
public:
  void getClass() { cout << "I'm a Dog" << endl;}
};

void whatClassAreYou(Animal *animal)
{
  animal->getClass(); 
}

void whatClassAreYou2(Animal animal)
{
  animal.getClass();
}

int main()
{
  Animal *animal = new Animal;
  Dog *dog = new Dog;

  animal->getClass();
  dog->getClass();

  whatClassAreYou(animal);
  whatClassAreYou(dog);

  Animal animal2;
  Dog dog2;

  whatClassAreYou2(animal2);
  whatClassAreYou2(dog2);
}
```

In this example, we define another method `whatClassAreYou2` calls on object instead of pointers. Now, we apply this method
to our newly created objects `animal2` and `dog2` and we get

```
I'm an Animal
I'm a Dog
I'm an Animal
I'm a Dog
I'm an Animal
I'm an Animal
```

As you can see, even we have virtual function in our base class, `whatClassAreYou2()` invokes only the base class's `getClass()`
method and ignores the subclass overrides. 

Aside note, you may notice that we use two ways to initialize our objects. The first way is through `Animal *animal = new Animal;`
and the second way is through `Animal animal2;`. Initialization is quite complex in C++. These two ways are essentially the same:
we use **default constructor** [^1] to initialize the objects. The only difference is that the first way gives us a pointer to 
the object and the second way gives object directly. To obtain the pointer to the object, we can do `Animal *ptrAnimal = &animal2`.
Another way to initialize object is through value initilialization [^2]. For example:

```c++
string *ps1 = new string;   // default initalized to the empty string
string *ps = new string();  // value initialized to the empty string
int *pi1 = new int;         // default initialized; *pi1 is undefined
int *pi2 = new int();       // value initialized to 0; *pi2 is 0
```

[^1]: See Section 7.1.4 Constructors (p.262) of C++ Primier (5th edition) for details.
[^2]: See Section 12.1.2 Managing Memory Directly (p.459) of C++ Primier (5th edition) for details.

## Pure virtual function & abstract base class

Another important concept related with **virtual** is called **pure virtual**. The difference between this concept
is that, as stated in wikipedia:

> A virtual function or virtual method is a function or method whose behavior can be overriden within an inheriting class
> by a function with the same signature. A pure virtual function or pure virtual method is a virtual function that
> is required to be implemented by a derived class that is not abstract.

In short, virtual function can be overriden; pure virtual function must be implemented. Let's take a look a example

```c++
#include <iostream>
using namespace std;

// An abstract data type is a class that acts as the base to other classes
// They stand out because its methods are initialized with zero
// A pure virtual method must be overwritten by subclasses

class Car
{
public:
  virtual int getNumWheels() = 0;
  virtual int getNumDoors() = 0;
};

class StationWagon : public Car
{
public:
  int getNumWheels() { cout << "Station wagon has 4 wheels" << endl; }
  int getNumDoors() { cout << "Station wagon has 4 doors" << endl;}
  StationWagon() {}
  ~StationWagon();
};

int main()
{
  // Create a StationWagon using the abstract data type Car
  Car *stationWagon = new StationWagon();

  stationWagon -> getNumWheels();

  return 0;
}
```

Here, we have a base class called `Car` and a class that derives from the `Car` class called `StationWagon`.  `Car`
is a lot similar to our `Animal` class in the sense that both classes have methods that have keyword `virtual`. However,
`Car` class's methods have `=0`. This is exactly how we identify **pure virtual**: we specify that a virtual function 
is a pure virtual by writing `=0` in place of a function body (i.e., just before the semicolon that ends the declaration).

!!!note
    1. Unlike ordinary virtuals, a pure virtual function does not have to be defined.
    2. `=0` may appear only on the declaration of a virtual function in the class body.

A class like `Car` that contains (or inherit without overriding) a pure virtual function is an **abstract base class**. An
abstract base class defines an interface for subsequent classes to override. We cannot (directly) create objects of a
type that is an abstract base class.

## Key terms summary

Here, I summarize terms appeard in this post as a quick index for future reference:

- **virtual**: Member function that defines type-specific behavior. Calls to virtual made through 
a reference or pointer are resolved at run time, based on the type of the object to which the reference 
or pointer is bound.

- **pure virtual**: Virtual function declared in the class header using `=0` just before the semicolon. A pure
virtual function need not be (but maybe) defined. Classes with pure virtuals are abstract classes. If a 
derived class does not define its own version of an inherited pure virtual, then the derived class is abstract as well.

- **polymorphism**: As used in object-oriented programming, refers to the ability to obtain type-specific behavior
based on the dynamic type of a reference or pointer.

- **static type**: Type with which a variable is defined or that an expression yields. Static type is known at compile time.

- **dynamic type**: Type of an object at runtime. The dynamic type of an object to which a reference refers or to which
a pointer points may differ from the static type of the reference or pointer. A pointer or reference to a base-class type
can refer to an object of derived type. In such cases the static type is reference (or pointer) to base, but 
the dynamic type is reference (or pointer) to derived.

- **abstract base class**: Class that has one or more pure virtual functions. We cannot create objects of an 
abstract base-class type.