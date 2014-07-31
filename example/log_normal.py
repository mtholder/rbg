# figure 4 of https://molevol.mbl.edu/images/d/d4/RB_BayesFactor_Tutorial.pdf
from rbg.prob.density import Gamma, Exponential, LogNormal
from rbg import generate, Monitor, MCMC
from rbg.moves import ScaleMove
import rbg.var_transform as vt
import sys

observations = [1.3, 2.4, 3.4]
m = Gamma(alpha=3.0, beta=1.0).create()
sigma = Exponential(_lambda=1.0).create()
mu = vt.log(m) - vt.power(sigma, 2.0)/2
ln_norm = LogNormal(mu, sigma)
x = [ln_norm.datum(val) for val in observations]

moves = []
moves.append(ScaleMove(sigma, size=0.5, tune=True, weight=4.0))
moves.append(ScaleMove(m, size=0.5, tune=True, weight=4.0))

monitors = []
monitors.append(Monitor(freq=10, separator=' | ', stream=sys.stdout))
monitors.append(Monitor(freq=10, file_name='output/simple_ln_mcmc.log'))
mcmc = MCMC(burnin=10000,
            tuning_freq=1000,
            generations=40000)
# generate the rev language file with the same name, but with .Rev extension
generate(mu,
         moves,
         monitors,
         mcmc,
         locals(),
         file_stem=__file__)