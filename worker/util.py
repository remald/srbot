from model import RRDBNet, ESRGAN
import torch


def load_models(device='cpu'):
    net1 = RRDBNet(3, 3, 64, 23, gc=32).to(device)
    net1.load_state_dict(
        torch.load("./weights/RRDB_PSNR_x4.pth", map_location=device))

    net2 = ESRGAN().to(device)
    dump = torch.load("./weights/PSNRV1_1PreTrained.pth", map_location=device)
    net2.load_state_dict(dump['state_dict'])
    print(dump['iteration'])

    return net1, net2
