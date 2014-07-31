# figure 4 of https://molevol.mbl.edu/images/d/d4/RB_BayesFactor_Tutorial.pdf
from rbg import generate
import rbg.var_transform as vt
from rbg.prob.density import Gamma, Exponential, LogNormal
observations = [1.3, 2.4, 3.4]
m = Gamma(alpha=3.0, beta=1.0).create()
sigma = Exponential(_lambda=1.0).create()
mu = vt.log(m) - vt.power(sigma, 2.0)/2
ln_norm = LogNormal(mu, sigma)
x = [ln_norm.datum(val) for val in observations]
generate(ln_norm, locals(), file_stem=__file__)