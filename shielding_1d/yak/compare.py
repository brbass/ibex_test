import numpy as np

vals = [5, 10, 100, 500]
phivals = []
for i in vals:
    phivals.append(np.loadtxt("phi_average_1000_{}.txt".format(i)))

bench_ind = -1
for i in range(len(vals)):
    print("num points: {}".format(vals[i] * 1000))
    phi_err = phivals[bench_ind] - phivals[i]
    l2_err = [np.sqrt(np.sum(np.power(phi_err[:, i], 2)) / np.sum(np.power(phivals[bench_ind][:, i], 2))) for i in range(2)]
    linf_ind = [np.abs(phi_err[:, i]).argmax() for i in range(2)]
    linf_err = [phi_err[linf_ind[i], i] / phivals[bench_ind][linf_ind[i], i] for i in range(2)]
    print(linf_ind, linf_err)
    print(l2_err)
    
