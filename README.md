# Design
Apropos is an attempt to solve a problem that every developer runs into eventually. You want to use a web API but the API is confusing or has almost no documentation.
You know what you want but you can't get it without difficulty. Wouldn't it be nice to have a common language to access any sort of data?

This is what Apropos solves.

Apropos takes a JSON input and returns a JSON output with exactly what you want in a standard format.

All outputs are in [SI](https://en.wikipedia.org/wiki/International_System_of_Units) units.

Example JSON input:

    {

    "action": "weather",

    "input": {

        "city": "Boston"

    },

    "output": {

        "temperature": "int"

    }

    }

Example JSON output

    {

    "temperature": 279.19

    }


![Layout](http://i.imgur.com/a9DR1pk.png)
