import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt

data = [3,4,2,0,4,2,4,5]

# Fit a normal distribution to
# the data:
# mean and standard deviation
mu, std = norm.fit(data)

# Plot the histogram.
plt.hist(data, bins=8, density=True, alpha=0.6, color='b')

# Plot the PDF.
xmin, xmax = plt.xlim()
x = np.linspace(xmin, xmax, 100)
p = norm.pdf(x, mu, std)

plt.plot(x, p, 'k', linewidth=2)
title = "Fit Values: {:.2f} and {:.2f}".format(mu, std)

print(mu, std)
#plt.title(title)
plt.xlabel("Years After Recession to Dividend Announcement (1994 - 2022)")

plt.show()

