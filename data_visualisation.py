from matplotlib import pyplot as plt

with open('output/11/output.log') as f:
    content = f.readlines()

i, score, deviance, diff_socre, diff_deviance = [], [], [], [], []

for line in content:
    lst = line.split()
    i.append(int(lst[0]))
    if len(lst) == 5:
        score.append(float(lst[1]))
        deviance.append(float(lst[2]))
        diff_socre.append(float(lst[3]))
        diff_deviance.append(float(lst[4]))
    else:
        score.append(0)
        deviance.append(0)
        diff_socre.append(0)
        diff_deviance.append(0)
    
score_plt, = plt.plot(i, score, '-r', label='score')
deviance_plt, = plt.plot(i, deviance, '-b', label='deviance')
diff_score_plt, = plt.plot(i, diff_socre, '-g', label='diff_score')
diff_deviance_plt, = plt.plot(i, diff_deviance, '-y', label='diff_deviance')

plt.legend(loc='upper right')

plt.show()
