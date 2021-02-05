from .model import RRDBNet, ESRGAN
import torch


def load_models(device='cpu'):
    net1 = RRDBNet(3, 3, 64, 23, gc=32).to(device)
    net1.load_state_dict(
        torch.load("./weights/esr1.pth", map_location=device))

    net2 = ESRGAN().to(device)
    dump = torch.load("./weights/netG_4x_checkpoint.pth", map_location=device)
    net2.load_state_dict(dump['state_dict'])
    print(dump['iteration'])

    return net1, net2