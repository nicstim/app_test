from typing import Optional

from django.contrib.auth.models import User
from django.db import models


class AbsTTitle(models.Model):
    title = models.CharField("Заголовок", max_length=130)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class Test(AbsTTitle):

    class Meta:
        verbose_name = "Тест"
        verbose_name_plural = "Тесты"


class TestQuestion(AbsTTitle):
    test = models.ForeignKey(Test, verbose_name="Тест", related_name="question", on_delete=models.CASCADE)
    description = models.TextField("Описание")

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = 'Вопросы'


class Answer(models.Model):
    question = models.ForeignKey(TestQuestion, verbose_name="Вопрос", related_name="answer", on_delete=models.CASCADE)
    answer = models.CharField("Ответ", max_length=130)
    is_success = models.BooleanField("Верный", default=False)

    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = 'Ответы'

    def __str__(self):
        return f"{self.id}| {self.answer}"


class UserTest(models.Model):
    user = models.ForeignKey(User, verbose_name="Пользователь", related_name='test', on_delete=models.CASCADE)
    test = models.ForeignKey(Test, verbose_name="Тест", related_name="user_test", on_delete=models.CASCADE)
    answer = models.ManyToManyField(Answer, related_name='user_answer', blank=True)

    @property
    def test_result(self) -> dict:
        result = {
            "success_answer": self.answer.filter(is_success=True).count(),
            "wrong_answer": self.answer.filter(is_success=False).count(),
            "total_success_answer": Answer.objects.filter(question__test=self.test, is_success=True).count(),
            "total_answer": self.answer.count()
        }

        return result

    @property
    def last_question_id(self) -> Optional[int]:
        try:
            return self.answer.last().question_id
        except AttributeError:
            return None

    @classmethod
    def get_user_test(cls, user_id: int, test_id: int):
        try:
            user_test = cls.objects.get(user_id=user_id, test_id=test_id)
            return user_test
        except cls.DoesNotExist:
            return cls.objects.create(
                user_id=user_id,
                test_id=test_id
            )




