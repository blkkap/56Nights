import torch


x = torch.rand(100,10)
w = torch.rand(10,1)

y = x@w 
print('works')
