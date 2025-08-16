# Модуль для работы с аудио загрузка медиафайла и воспроизведение и наложение эффектов

import os
from typing import Optional

import self
from pydub import AudioSegment
import simpleaudio as sa
from pydub.utils import which

# ЯВНО указываем путь к ffmpeg/ffprobe, если они в PATH — which найдёт сам
# AudioSegment.converter = r"C:\ffmpeg\bin\ffmpeg.exe"
# AudioSegment.ffprobe   = r"C:\ffmpeg\bin\ffprobe.exe"


"""
    Класс AudioManager отвечает за всю логику обработки аудио:
    - Загрузка файлов
    - Воспроизведение и остановка
    - Эффекты: реверс, изменение скорости, громкости
    - Обрезка (trim)
    - Сохранение результата в файл
    """


class AudioManager:
    def __init__(self):
        self.audio: Optional[AudioSegment] = None
        self.play_obj: Optional[sa.PlayObject] = None
        self.file_patch: str = ""

    def load(self, path: str) -> None:
        """
                      Загружает аудиофайл из указанного пути.

                      :param path: файловый путь к аудио (wav, mp3, flac, ogg и т.п.)
                      :raises: исключение, если файл не удалось загрузить
                      """
        # Сохраняет путь для возможной повторной загрузки медиафайла
        self.path = path
        self.audio = AudioSegment.from_file(path)
        # Использовать pydub для чтение файла и сохранить в отдельную переменную путь для
        # будущего сохранения

        if not os.path.isfile(path):
            raise FileNotFoundError(f"Файл не найден: {path}")

    def play(self) -> None:
        '''
        Воспроизводит загруженный ауиофайл
        Если уже идет воспроизведение, с начала останавливаете
        :return:
        '''
        if self.play_obj is not None and self.play_obj.is_playing():
            self.play_obj.stop()
        # if self.audio:
        #     # ПОлучаем байты для передачи в simlpe audio
        #     data = self.audio.raw_data
        #     # Создаем новый объект PlayObject для воспроизведения
        #     self.play_obj = sa.play_buffer(data, num_channels=self.audio.channels,
        #                                    bytes_per_sample=self.audio.sample_width,
        #                                    sample_rate=self.audio.frame_rate)
        # если аудио загружено — запускаем новое воспроизведение
        if self.audio:
            # получаем "сырые" байты для передачи в simpleaudio
            raw_data = self.audio.raw_data
            # частота дискретизации
            sample_rate = self.audio.frame_rate
            # количество каналов (1 — моно, 2 — стерео)
            num_channels = self.audio.channels
            # количество байт на сэмпл
            bytes_per_sample = self.audio.sample_width
            # создаём и запускаем PlayObject
            self.play_obj = sa.play_buffer(raw_data, num_channels, bytes_per_sample,
                                               sample_rate)
        else:
            print('Аудиофайл не загружен')

        # Надо получить "сырые" байты аудио. Сделать проверку, что аудиофайл загружен.
        # Почитать как запустить буферное воспроизведение


    def stop(self) -> None:
        """
                Останавливает воспроизведение, если оно запущено.
                """
        if self.play_obj is not None and self.play_obj.is_playing():
            self.play_obj.stop()
            self.play_obj = None
        else:
            print('Воспроизведение не запущено')
        # Реализовать метод по остановкке аудио, сделать проверку,
        # что если аудио не запущено выдавать сообщение


    def reverse(self) -> None:
        """
                Применяет эффект реверса (звук задом наперёд).

                :raises: RuntimeError, если аудио не загружено
                """
        if self.audio is None:
            raise RuntimeError("Аудиофайл не загружен")

        if self.audio:
            self.audio = self.audio.reverse()


        # По читать про reverse библеотеки pydub. Сделать проверку типу если аудио не загружено,
        # то выдовать сообщение

    def change_volume(self, db: float) -> None:
        """
                Изменяет громкость аудио.

                :param db: изменение громкости в децибелах (положительное значение увеличивает
                громкость,
                        отрицательное - уменьшает)
                :raises RuntimeError: если аудио не загружено
                """
        if self.audio is None:
            raise RuntimeError("Аудиофайл не загружен")

        self.audio = self.audio + db


    def trim(self, start_time: int, end_time: int) -> None:
        """
            Обрезает аудио до указанного диапазона времени.

            :param start_time: начальное время обрезки в миллисекундах
            :param end_time: конечное время обрезки в миллисекундах
            :raises RuntimeError: если аудио не загружено
            """
        if self.audio is None:
            raise RuntimeError("Аудиофайл не загружен")

        self.audio = self.audio[start_time:end_time]


    def save(self, output_path: str) -> None:
        """
                Сохраняет измененный аудиофайл в указанный путь.

                :param output_path: путь для сохранения файла
                :raises RuntimeError: если аудио не загружено
                """

        if self.audio is None:
            raise RuntimeError("Аудиофайл не загружен")

        self.audio.export(output_path, format=os.path.splitext(output_path)[1][1:])
