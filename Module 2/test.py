import torch

X = torch.tensor([[0, 1, -1],
                  [0, 2, -1],
                  [2, 1, -1]])

X_masked = torch.masked.MaskedTensor(X, mask=X >= 0)

print(X_masked)

# Create a tensor
tensor = torch.tensor([[0.,0.2, 1.1]])

# Find the index of the first occurrence of 1
#first_index = torch.nonzero(tensor == 1)[0][1].item()
first_index = torch.nonzero(tensor == 1)[0]

print("First index of value equal to 1:", first_index, bool(first_index))