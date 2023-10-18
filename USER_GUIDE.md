# Pandos - User Guide

## Installation

Install via pip:

```commandline
$ pip install pandos
```

## Using the Pandos CLI

Once you have pandos installed, you should be able to use the CLI. Test it out via the following commands:
* `pandos version`
* `pandos about`

The following command can also be used for testing:

```commandline
$ pandos hello
```

Arguments can be provisioned as following:
* `pandos hello --name Panda`

### Execution Modes

There are 2 ways of executing a pandos-cli command.

**Option 1**: Direct execution

The direct execution looks as following: `pandos <command> <arguments>`


```commandline
$ pandos hello --name Panda
```

**Option 2**: Indirect excution  

The indirect execution passes through the `execute` command and adds additional execution metadata info. For example:

```commandline
$ pandos execute hello --name Panda
```


## Module Guide: `pandos.exceptions`

The pandos-exceptions module contains 2 key components used to manage exceptions:
* `ExceptionEnumBuilder` class: this is an utility class that facilitates creating the an exception-based enum class.
* `PandosException` class: this is a custom exception class that inherits from the build-in `Exception`. 
  All of the pandos exceptions inherit from this custom class and are implemented via the `ExceptionEnumBuilder` utility
  class in the `enums` classmethod.

You can register new custom exceptions by modifying the `enums` classmethod and adding a key-value as following:
* Key: The exception name that will be used as identifier for the enum (e.g., `MY_CUSTOM_EXCEPTION`)
* Val: The creation of the actual exception via the `cls.custom` classmethod (e.g., `cls.custom(exception_name="MyCustomExc")`)

```python
...
    @classmethod
    def enums(cls):
        return ExceptionEnumBuilder.members(
            name="PandosExceptionCatalog",
            # Register exceptions here:
            PANDOS_BUILTIN_CUSTOM_EXCEPTION=cls.custom(
                exception_name="PandosBuiltInCustomException",
                default_message="This is an example custom exception - you should not find this error message in prod",
            ),
            MY_CUSTOM_EXCEPTION=cls.custom(
                exception_name="MyCustomExc",
            ),
        )
```

All exceptions are available as enums in the `pandos_exceptions` variable that you can import via the following pattern:

```python
from pandos.exceptions import pandos_exceptions
```

This facilitates pattern matching:

```python
from pandos.exceptions import pandos_exceptions, PandosException

def something():
    # FYI Pandos exceptions can be "raised" via the ".throw()" method!
    pandos_exceptions.PANDOS_BUILTIN_CUSTOM_EXCEPTION.throw()

# Example 1:
try:
    something()
except PandosException as e:
    match pandos_exceptions(type(e)):
        case pandos_exceptions.PANDOS_BUILTIN_CUSTOM_EXCEPTION:
            print("You should see this message.")
        case pandos_exceptions.MY_CUSTOM_EXCEPTION:
            print("This message shouldn't be shown.")
        case _:
            print("Neither this message.")

# Example 2:
try:
    something()
except pandos_exceptions.PANDOS_BUILTIN_CUSTOM_EXCEPTION.value:
    print("You should see this message, again.")
# ...
```


## Module Guide: `pandos.monads.either`

This module contains a simplified implementation of the `Either` monad in python. The idea is design an Abstract Data Type
(i.e., `Either` monad) that follows a sum-pattern capable of representing 2 different scenarios:
* Scenario 1: `Right` used to represent the correct/expected value.
* Scenario 2: `Left` used to wrap an exception and represent an error in the program.


```python
from pandos.monads.either import Either, Left, Right

# Consider we have a float value 5.0; we can wrap this value into the Either context.
example_a = Either.from_value(x=5.0)

# You can use map/flat_map to operate with the inner value
example_b = example_a.map(lambda a: a + 1)  # Gets you an Either (Right) with the value 6.0
example_c = example_a.flat_map(lambda a: example_b.map(lambda b: a + b))  # Either (Right) with the value 11.0

match example_c:
    case right if isinstance(right, Right):
        pass
    case left if isinstance(left, Left):
        pass

```

You can yank the inner value of an Either Context by calling `resolve`. Nonetheless, consider that this will trigger
the raise exception if a `Left` is encountered.

```python
from pandos.monads.either import Either

example_1 = Either.from_value(x=5)
example_2 = example_1.map(lambda x: x + 1)
example_3 = example_2.map(lambda x: x / 0)

example_2.resolve()  # This will return an int: 6
example_3.resolve()  # This will raise an exception (div by zero)
```
* You can keep your code safe by sticking to the `Either` context.

### Either Monad Composition

There are several ways you can combine either-monad instances. Consider the following example with
`either_a` (Right) with a value of `5` and `either_b` (Right) with a value of `10`:

```python
from pandos.monads.either import Either

either_a = Either.from_value(x=5)
either_b = either_a.map(lambda x: 2 * x)
```

**Challenge**: Create an `either_c` with the sum of `either_a` & `either_b`.

**Option 1:** a first approach might be resolving both the `either_a` and `either_b` monad so that we
gain access to the inner value. This approach is **not recommended** since we need to guard our code to consider any
exception being hold by an either-left.

```python
# Doing this might faid:
either_c = Either.from_value(x=either_a.resolve() + either_b.resolve())

# Therefore, we need to add a try-except statement:
try:
    either_c = Either.from_value(x=either_a.resolve() + either_b.resolve())
except Exception as e:
    either_c = Left(exception=e)
```

**Option 2:** to avoid using the `try-except` block, we can check if the instances correspond to the `Right` or `Left` cases.
This approach is not recommended since you need to branch-out your implementation to consider all the relevant combinations.

```python
match either_a:
    case right_a if isinstance(right_a, Right):
        match either_b:
            case right_b if isinstance(right_a, Right):
                either_c = Right.from_value(x=right_a.value + right_b.value)
            case left_b if isinstance(left_a, Left):
                either_c = left_b
    case left_a if isinstance(left_a, Left):
        either_c = left_a
```
* It's clear that this implementation is not scalable; you'd need to exponentially write more code when working with more either instances.

**Option 3:** We can use the `map/flat_map` methods to access the inner values via functional transformations.
* The `map` method allows us to use an `A -> B` function.
* The `flat_map` method allows us to use an `A -> Either[B]` function.

```python
either_c = either_a.flat_map(lambda a: either_b.map(lambda b: a + b))
```

**Option 4:** the `Either` implementation allows is to enter the `either` context via an iterator-pattern. This means
that we can "iterate" over the inner value and maintain the `Either` context on the results.

```python
either_c = Either.comprehension(
    a + b
    for a in either_a
    for b in either_b
)
```

As you can notice, the `Option 3` & `Option 4` approaches facilitate working with either-monad composition. We recommend
using any of those two approaches. Consider that `Option 3` could start to become more complex when adding more monad
instances while using the either-comprehension approach maintains simplicity.

Example: Create an `either_d` that contains the sum of `either_a`, `either_b`, and `either_c`.

```python
# Sol.1 Using map/flat_map implementation
either_d = either_a.flat_map(
    lambda a: either_b.flat_map(
        lambda b: either_c.flat_map(
            lambda c: a + b + c
        )
    )
)
```

```python
# Sol2. Using either-comprehension
either_d = Either.comprehension(
    a + b + c
    for a in either_a
    for b in either_b
    for c in either_c
)
```

## Module Guide: `pandos.future`

This is a simple & naive implementation of Python lightweight concurrent futures with functional composition.

```python
import time
from pandos.futures import Future

def add(a: float, b: float) -> float:
    time.sleep(5)
    return a + b

future_a = Future(function=add, a=5, b=3)
future_a.wait()
```

You can also enable futures by decorating a python function:

```python
import time
from pandos.futures import Future

@Future.decorator()
def add(a: float, b: float) -> float:
    time.sleep(5)
    return a + b

output_now = add(5, 3)  # Blocking function call
output_later = add.future(5, 3)  # Non-blocking function call
```

### Future Composition

