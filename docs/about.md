---
layout: default
comments: true
---

# About EvoAgent
_An evolutionary multi-agent platform based on mesa and NEAT_\
A video of an old version of EvoAgent can be found on youtube:
<iframe width="420" height="315"
src="https://www.youtube.com/embed/pOF1H84xPik">
</iframe>

This is a screenshot from a more recentversion. You can see that the network for the selected network is displayed on the left side, and much more information are shown.
![EvoAgent Main View](/assets/main.png)



## Overview

With this tool you can evolve agents in a simple 2D environments. \
At the beginning, agents are endowed with a simple neural network which is specified by their genome. With time, they'll make children, which will inherit the genome, plus some random mutations. The mutations will add a connetion, a node, or change the weight. The evolutionary system is based on NEAT by Kenneth Stanley ([paper here][1]). However, the main difference between this approach and the classic evolutionary algorithm approach, is the naturalistic approach we are using here. In a classic evolutionary algorithm we would use a fitness function, we would test our agents, and we would use a genetic operator for generating the next generation. We have none of that here. Agents will spawn a new children every `x` time-steps. The more they survive, the more children they'll get. I found this approach much more intuitively valid as will simply respond to the rule: `the more you survive, the more you'll spread your genes`.  This will also allow for generational interactions (as multiple generations will live at the same time), in case one wants to run experiments on family behaviour etc.


## Install

`git clone git@github.com:ValerioB88/EvoAgent.git` 
EvoAgent plots everything in the browser. This is heavily dependent on the [Mesa library][3]. [My fork][4]
To install my fork run `pip install git+https://github.com/ValerioB88/mesa`

There are several examples you can run to check if everything work (see next section). I still need to thoroughly test the installation and testing process, but if you want to try it and you are running into problems, please contact me, I'll be happy to help!


## Examples
There are several examples in the folder `code/evoagent/experiments/`, which should get you started. Most of this is self explanatory. For example, run the file `easy_env_browser.py` and a browser with the _environment view_ should open. Both the model state and the population gets saved (the model state _includes_ the population). You want to use the model state to continue a running simulation with exactly the same parameters, from exactly the same point (the model state _includes_ the population state). Instead, you may want to test an evolved population on a different enviornment: in that case, load the population. Examples of both these cases in `continue_sim.py`  and `load_pop.py`. Model and population get saved every 1000 time steps, or when you press `s`. 

## Environment View
This contains a canvas, information about the selected agent, and some plots. At each points there always be a `selected agents`, for which many info are shown in the text field on the right sidebar. You can change the selected agent by pressing `a` and `d` on your keyboard (in a future version, it will be possible to click on the agent on the canvas to select it). Other info are shown in the following image:
![EvoAgent Main View](/assets/evoview.png)
[Link to a page]({{ site.baseurl }}{% link index.md %})

## Shortcuts
`q` start/stop simulation\
`a/d` previous/next agent\
`k` kill selected agent\
`c` selected agent spawn a child\
`s` save model\
`x` advance the simulation one step


## Agents Behaviour
Agents will have a limited field of view, specified by the parameters `fov` and `max_vision_dist`. You can visualize them by checking `Render FOV` in the environment view. Each agent will have a maximum lifespan of `max_age = 500`, but it can die faster if its energy goes to 0. They have a `energy_depletion` rate of 0.008. An agent will eat a food token when it touches it, getting an energy increase of `0.8` (or whathever established by the current `Epoch`, see later), up to 1. Agent will become fertile after `fertile_age_start = 90` timesteps. At that point, they will spawn a child every `time_between_children = 100` timesteps. For now, reproduction is asexual, so there is no crossover (this will be expanded in a next version).

Agents can only perceive the closest food token, IF it's within their field of view. If the selected agent is perceiving a food token, this will be represented with a red color in the environment view.  Agents' network input will be the linear distance to the perceived food token, the angular distance, and their own energy level. There will be two output units, one defining the forward/backward movement, the other one defining the rotation.

### Epochs
The epochs are interval of times defined by the amount of food in the environment. 
```
epochs = deque([Epoch(2000, [0.8]*200),
                Epoch(2000, [0.8]*100),
                Epoch(6000, [0.8]*75)])
```
                
This means that we have 3 epochs, the first lasting 2000 iteration, the last 6000 iterations. The first will have 200 food tokens, each provigin 0.8 units of energy (recall that `[0.8]*200` generates a list of 200 elements of value 0.8: `[0.8, 0.8, 0.8....]`. By changing the second parametr, you can specify the distribution of food token easily. You can also have "posionous" food: `Epoch(2000, [-0.2]*200)` this will work. However, currently the agents don't have a way to differentiate between "good" and "bad" food, so it doesn't make much sense to use bad food right now. 

The simulation will activate one epoch at the time, starting from the first one. When the last epoch finishes, the simulation stop. You can instead run the simulation indefinitively by setting the epoch duration to `np.inf`. 

## Speed Up Simulation
In the environment view, uncheck `Render Canvas`, then set the `Frames per Second` slider to 0. That's as fast as it can get! You'll probably get even more speed up if you don't use the environment view, and run everything in pure python. Check the `experiments/diffcult_env.py` for and example.

## Known Problems
If you stop the simulation and try to run it again, you'll get the error:\
```OSError: [WinError 10048] Only one usage of each socket address (protocol/network address/port) is normally permitted```\
To fix this, try to change the port in `server.launch(...)`. If it doesn't work, close and open your browser. I know this is annoying, but hadn't have the time to fix it yet.

This has only been tested on Windows 10 and Edge 97. I don't plan to test it on any other configuration. Sorry!

## To Do
&#9744; Add sexual reproduction: find a partner, do crossover\
&#9744; Many agents options should be in a config file\
&#9744; Select an agent by clicking on it with the mouse\
&#9744; Implement data collection - or adapt mesa data collection\
&#9744; Implement more ways to perceive food\
&#9744; Implement ways to perceive other agents\
&#9746; Server port stays open after code stops - which often lead to annoying behaviour. Find a way to fix this - Done. Port is allocated dynamically
&#9746; Examples to run the simulation without the environment view, and print some info in the console
<!--- &#9746; -->




[1]: http://nn.cs.utexas.edu/downloads/papers/stanley.ec02.pdf
[2]: https://www.youtube.com/watch?v=pOF1H84xPik&ab
[3]: https://github.com/projectmesa/mesa
[4]: https://github.com/ValerioB88/mesa


{% if page.comments %}
<div id="disqus_thread"></div>
<script>
    /**
    *  RECOMMENDED CONFIGURATION VARIABLES: EDIT AND UNCOMMENT THE SECTION BELOW TO INSERT DYNAMIC VALUES FROM YOUR PLATFORM OR CMS.
    *  LEARN WHY DEFINING THESE VARIABLES IS IMPORTANT: https://disqus.com/admin/universalcode/#configuration-variables    */
    /*
    var disqus_config = function () {
    this.page.url = PAGE_URL;  // Replace PAGE_URL with your page's canonical URL variable
    this.page.identifier = PAGE_IDENTIFIER; // Replace PAGE_IDENTIFIER with your page's unique identifier variable
    };
    */
    (function() { // DON'T EDIT BELOW THIS LINE
    var d = document, s = d.createElement('script');
    s.src = 'https://https-valeriob88-github-io-evoagent.disqus.com/embed.js';
    s.setAttribute('data-timestamp', +new Date());
    (d.head || d.body).appendChild(s);
    })();
</script>
<noscript>Please enable JavaScript to view the <a href="https://disqus.com/?ref_noscript">comments powered by Disqus.</a></noscript>
{% endif %}
