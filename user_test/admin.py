from django.contrib import admin

from user_test.forms import AnswerInlineFormSet
from user_test.models import Test, TestQuestion, Answer, UserTest


@admin.register(UserTest)
class UserTestAdmin(admin.ModelAdmin):
    pass


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    pass


class AnswerInline(admin.TabularInline):
    model = Answer
    classes = ['collapse']
    extra = 0
    min_num = 2
    formset = AnswerInlineFormSet


@admin.register(TestQuestion)
class TestQuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]
