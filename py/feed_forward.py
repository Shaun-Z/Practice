import torch
from torch import nn as nn

from labml_helpers.module import Module

class FeedForward(Module):
    def __init__(self, d_model: int, d_ff: int,
                 dropout: float = 0.1,
                 activation=nn.ReLU(),
                 is_gated: bool = False,
                 bias1: bool = True,
                 bias2: bool = True,
                 bias_gate: bool = True):
        
        super().__init__()
        self.layer1 = nn.Linear(d_model, d_ff, bias=bias1)
        self.layer2 = nn.Linear(d_ff, d_model, bias=bias2)
        self.dropout = nn.Dropout(dropout)
        self.activation = activation
        self.is_gated = is_gated
        if is_gated:
            self.linear_v = nn.Linear(d_model, d_ff, bias=bias_gate)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        g = self.activation(self.layer1(x))

        if self.is_gated:
            x = g * self.linear_v(x)
        else:
            x = g
        x = self.dropout(x)
        x = self.layer2(x)
        return x
    
if __name__ == '__main__':
    ff = FeedForward(512, 2048, is_gated=True)
    x = torch.randn(10, 512)
    y = ff(x)
    print(y.shape)  # Should print torch.Size([10, 512])
    print(ff)
    print(ff.is_gated)

    