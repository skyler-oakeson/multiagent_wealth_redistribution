"""
This project is an implementation of the paper Local Wealth Redistribution
Promotes Cooperation in Multiagent Systems: https://arxiv.org/pdf/1802.01730.

Authored by Flavio L. Pinherio and Fernando P. Santos.
"""

from dilemma import Prisoners, StagHunt

def main():
    """ Programs entry point """
    p = Prisoners(4, 3, 2, 1)

main()
