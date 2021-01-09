from model import ESRGAN
import torch


def load_esr_model(file, device='cpu'):
    net = ESRGAN().to(device)
    net.load_state_dict(
        torch.load("weights/esr.pth", map_location=device)['state_dict'])

    return net
