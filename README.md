It’s been a year since I embarked on this journey, I remember sat here the same time last year just starting this. It’s been a while ride for me the last year both personally and professionally. I have learned a hell of a lot. I have met some great people who have aided in the development of this. Kudos to them. You know who you are. Some great work went into this. I’ve had to deal with threats from the community, Idiots, general backlash. But your getting the base of a free automated trading system so stop complaining. 

For the anniversary edition, Not much will change. The only thing is left to do is “tweaks” to get the best out of it. But the default settings work great. I always had a vision, This code is NOT a “get rich quick” scheme however It has been ultimately profitable for me and others.

- Use of Masked arrays and masked functions such as mstats.theilslopes to take account of any corrupt data returned from the API, Not that this happens just a nice to have.

- IQR vs MAD function, You decide which is best. Please test and report your findings. 

- Pull epic's directly from IG rather than relying on external files, This allows for greater trade opportunities across ALL major and minor markets. You pick the markets you want to trade. More trading opportunities. 

- Completely self contained, Not reliant on external files, cron jobs or any external programs other than python libraries used. 

- Default looks back 28 weeks, This prevents "Whipsaw trading"

- Much cleaner code base

You will need …

- An active IG account, Demo/Live supported.


- Something to run this on, RPi will work fine but a lot of people run this on a lowend VPS, Think Linode. It will also run on a Windows machine but the idea is that you leave it on 24/5. 


- Keen Interest in Python/Stock trading.

Whilst this code is fully automated and will run on anything from a Raspberry Pi to a Supercomputer, I have not managed to get it running on a washing machine yet. 

Please feel free to put your own ideas in, fork it, share it. If you sell it I wills sue your arse. 

There is a discord. 

I have created a twitter account which tweets all my trades. 

## **Usage:**

*This will run giving it a highest CPU priority and generate a log file stored in the logs folder. You can then view this with tail -f. nohup keeps it running when you have exited your terminal session.* 

    nice -n -20 nohup python3 -u trading_bot.py > logs/stocks_live.log &
    nice -n -20 nohup python3 -u trading_bot.py > logs/stocks_demo.log &


