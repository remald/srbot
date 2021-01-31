translation = {
    'MESSAGES': {
        "help": "Supported commands:\n"
                "/self_trained_esrgan - deep neural network for image super resolution, trained by me\n"
                "/original_esrgan - esrgan pretrained by authors\n\n"
                "NOTE: This model is NOT for low-quality image quality improvement. "
                "This is for resolution increase only."
                "It works in a really bad way with compressed images, because it is sensitive to any"
                " information losses caused by image compression like JPEG. "
                "It's recommended to unset the \"Compress Images\" checkbox when sending the photo. "
                "Please send it as a document, not as a photo.",

        "start": "Hi!\nI'm a newest AI system!\nI use deep learning to do some magic!"
                 " Give me a photo and the magic will happen! \nNOTE: max supported pix resolution is 256*256!\n"
                 "Though you still can sand me a larger photo, "
                 "it will be resized to 256 * 256 size using bicubic filter. "
                 "For more information, type /help\n",

        "downscaled": "Downscaled image after bicubic resize (256 * 256 is max supported size)",

        "done": "I did some magic 😺",

        "orig_selected": "Original model is selected!\n",

        "self_selected": "Self-trained model is selected!\n",

        "wait_task": "Your picture is being processed now! This may take a while depending on the pic size.\n",

        "misunderstood": "You told me something weired",

        "look_at_this": "Well, look at this...",

        "ram_price": "RAM price is growing day by day. "
        "I am not getting enough funding from my Master to have enough memory to handle such large pictures. "
        "I could ask you to donate, but my Master forbids me. He says it's indecent. "
        "Now I will resize your image to fit 256 * 256 size."
    }
}
