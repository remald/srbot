translation = {
    "MESSAGES": {

        "help": "Поддерживаемые комманды:\n"
                "Увеличение разрешения изображения с использованием deep learning:"
                "/self_trained_esrgan - с помощью ESRGAN, обученной мной\n"
                "/original_esrgan - с помощью ESRGAN, обученной авторами архитектуры\n\n"
                "ВНИМАНИЕ: Эти модели не предназначены для улучшения качества сильно пережатых изображений, "
                "имеющих артефакты сжатия, зашумленность или иные дефекты, приводящие к существенной потере информации. "
                "Модель только для увеличения разрешения изображений в хорошем качестве."
                "Она работает очень плохо для изображений, использующих значительный уровень сжатия и артефакты"
                ", потому что она очень чувствительна к потерям информации, которые происходит при сжатии JPEG и др. "
                "Так же рекомендуется снять галочку \"Сжать изображения\" при отправке картинки в телеграмм. "
                "Рекомендуется отправлять изображение как документ, а не как фото.",

        "start": "Привет!\nЯ бот, использующий новейшие технологии обработки изображений!\n"
                 "Я использую deep learning для невероятно реалистичного увеличения разрешения!"
                 " Просто отправьте мне изображение и вы увидите магию! Вы можете выбрать одну из двух моделей: "
                 "обученную автором бота и обученную авторами архитектуры ESRGAN."
                 " \nВнимание: максимально поддерживаемое разрешение - 256*256!\n"
                 "Если вы отправите мне фото большого разрешения, "
                 "оно будет автоматически уменьшено до размера 256 * 256 с использованием бикубической фильтрации. "
                 "Используйте /help, чтобы получить более подробную информацию о боте и коммандах.\n",

        "downscaled": "Я уменьшил ваше изображение с помощью бикубической фильтрации "
                      "(256 * 256 - максимально поддерживаемый размер. "
                      "Размер определяется по произведению ширины на высоту)",

        "done": "Готово. Разве не волшебно? 😺",

        "orig_selected": "Выбрана оригинальная модель, обученная авторами ESRGAN!\n",

        "self_selected": "Выбрана самостоятельно обученная модель (Обучена автором бота)!\n",

        "wait_task": "Ваша картинка обрабатывается. Это может занять некоторое время, в зависимости от разрешения.\n",

        "misunderstood": "Я вас не понимаю. Вы говорите мне странное.",

        "look_at_this": "Сейчас я кое-что объясню...",

        "ram_price": "Цены на оперативную память растут изо дня в день. "
        "Финансирования, которое получаю от моего хозяина, мне хватило только на 8 Гб оперативной памяти. "
        "Этого не хватает на обработку картинок, больших чем 256*256 пикселей. "
        "Я мог бы попросить у вас донейт, но мой хозяин запрещает мне это. Он говорит что это неприлично. "
        "Сейчас я преобразую ваше изображение к размеру 255 * 255 пикселей."
    }
}
