import torch
from torch import nn
from torch.nn import functional as F
from typing import List, Callable, Union, Any, TypeVar, Tuple
Tensor = TypeVar('torch.tensor')

import pdb

class VAE(nn.Module):

    def __init__(self, args):

        super(VAE, self).__init__()
        
        self.args = args
        self.latent_dim = args.vae_k

        self.fc1 = nn.Linear(args.oppo_hidden_dim, args.oppo_hidden_dim//2)
        self.fc2 = nn.Linear(args.oppo_hidden_dim//2, args.oppo_hidden_dim//4)

        self.fc3 = nn.Linear(self.latent_dim, args.oppo_hidden_dim//4)
        self.fc4 = nn.Linear(args.oppo_hidden_dim//4, args.oppo_hidden_dim//2)
        self.fc5 = nn.Linear(args.oppo_hidden_dim//2, args.oppo_hidden_dim)


        self.fc_mu = nn.Linear(args.oppo_hidden_dim//4, self.latent_dim)
        self.fc_var = nn.Linear(args.oppo_hidden_dim//4, self.latent_dim)


    def encode(self, input: Tensor) -> List[Tensor]:
        """
        Encodes the input by passing through the encoder network
        and returns the latent codes.
        :param input: (Tensor) Input tensor to encoder [N x C x H x W]
        :return: (Tensor) List of latent codes
        """
        result = F.relu(self.fc1(input))
        result = self.fc2(result)
        
        result = torch.flatten(result, start_dim=1)

        # Split the result into mu and var components
        # of the latent Gaussian distribution
        mu = self.fc_mu(result)
        log_var = self.fc_var(result)

        return [mu, log_var]

    def decode(self, z: Tensor) -> Tensor:
        """
        Maps the given latent codes
        onto the image space.
        :param z: (Tensor) [B x D]
        :return: (Tensor) [B x C x H x W]
        """
        z = F.relu(self.fc3(z))
        z = F.relu(self.fc4(z))
        z = F.tanh(self.fc5(z))
        return z

    def reparameterize(self, mu: Tensor, logvar: Tensor) -> Tensor:
        """
        Reparameterization trick to sample from N(mu, var) from
        N(0,1).
        :param mu: (Tensor) Mean of the latent Gaussian [B x D]
        :param logvar: (Tensor) Standard deviation of the latent Gaussian [B x D]
        :return: (Tensor) [B x D]
        """
        std = torch.exp(0.5 * logvar)
        eps = torch.randn_like(std)
        return eps * std + mu

    def forward(self, input: Tensor, **kwargs):
        mu, log_var = self.encode(input)
        z = self.reparameterize(mu, log_var)
        recons = self.decode(z)

        loss = self.loss_function(recons, input, mu, log_var, self.args.kld_weight)

        return  recons, z, input, mu, log_var, loss

    def loss_function(self, recons, input, mu, log_var, kld_weight) -> dict:
        """
        Computes the VAE loss function.
        KL(N(\mu, \sigma), N(0, 1)) = \log \frac{1}{\sigma} + \frac{\sigma^2 + \mu^2}{2} - \frac{1}{2}
        :param args:
        :param kwargs:
        :return:
        """

        kld_weight = kld_weight # Account for the minibatch samples from the dataset
        recons_loss =F.mse_loss(recons, input)


        kld_loss = torch.mean(-0.5 * torch.sum(1 + log_var - mu ** 2 - log_var.exp(), dim = 1), dim = 0)

        loss = recons_loss + kld_weight * kld_loss
        return loss

    def sample(self,
               num_samples:int,
               current_device: int, **kwargs) -> Tensor:
        """
        Samples from the latent space and return the corresponding
        image space map.
        :param num_samples: (Int) Number of samples
        :param current_device: (Int) Device to run the model
        :return: (Tensor)
        """
        z = torch.randn(num_samples,
                        self.latent_dim)

        z = z.to(current_device)

        samples = self.decode(z)
        return samples

    def generate(self, x: Tensor, **kwargs) -> Tensor:
        """
        Given an input image x, returns the reconstructed image
        :param x: (Tensor) [B x C x H x W]
        :return: (Tensor) [B x C x H x W]
        """

        return self.forward(x)[0]