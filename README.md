# Pizza Delivery Tracking System

---

### Description

This repository contains python code in the `delivery_tracker` directory
which can process dispatcher inputs (^, <, >, or v) and calculate the total
number of houses which had pizzas delivered to them.

The `public` and `src` directories contain a Svelte web application which allows
users to upload a file of commands or type in a list of commands. The browser will
call the python backend and return a 2d graphic showing the delivery paths.

The web app is still a WIP. The plan is to have this hosted on AWS Lambda using the 
serverless framework if I have the time. If not, it should work locally.

The python code will work as the backend, but it can also be called from the command
line (see instructions for this below).

### Installation

To install python requirements:

```bash
pip install -r requirements.txt
```

To install javascript requirements:

```bash
npm install
```

### Usage

Once you have all dependencies installed, you can run the `delivery_tracker.py` script using any
one of the following commands:
```bash
python delivery_tracker/delivery_tracker.py # will prompt user to type in moves
python delivery_tracker/delivery_tracker.py --agents 2 # same as above but with 2 agents
python delivery_tracker/delivery_tracker.py --agents 3 --moves-file test.txt # loads moves from input.txt file and tracks 3 agents
```

There is also another python script called `animate.py` which can be run to produce a plot of the
deliveries made. To try out the plotting functionality run the following command:
```bash
python delivery_tracker/animate.py
```
Then open the `animation.png` file which is created to see the result.

*Feel free to play around with the variables in the script or change the input file to
see how it all works.
