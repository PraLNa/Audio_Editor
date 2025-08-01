# Модуль для работы с аудио загрузка медиафайла и воспроизведение и наложение эффектов

import os
from typing import Optional

import self
from pydub import AudioSegment
import simpleaudio as sa

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

    def play(self) -> None:
        '''
        Воспроизводит загруженный ауиофайл
        Если уже идет воспроизведение, с начала останавливаете
        :return:
        '''
        if self.play_obj is not None and self.play_obj.is_playing():
            self.play_obj.stop()
        if self.audio:
            # ПОлучаем байты для передачи в simlpe audio
            data = self.audio.raw_data
            
        # Надо получить "сырые" байты аудио. Сделать проверку, что аудиофайл загружен.
        # Почитать как запустить буферное воспроизведение


def stop(self) -> None:
    """
            Останавливает воспроизведение, если оно запущено.
            """
    # Реализовать метод по остановкке аудио, сделать проверку,
    # что если аудио не запущено выдавать сообщение


def reversed(self) -> None:
    """
            Применяет эффект реверса (звук задом наперёд).

            :raises: RuntimeError, если аудио не загружено
            """

# По читать про reverse библеотеки pydub. Сделать проверку типу если аудио не загружено,
# то выдовать сообщение
