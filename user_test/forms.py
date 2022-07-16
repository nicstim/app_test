from django.core.exceptions import ValidationError
from django.forms.models import BaseInlineFormSet


class AnswerInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super(AnswerInlineFormSet, self).clean()
        success_count = 0
        total_count = 0
        for form in self.forms:
            if form.cleaned_data and not form.cleaned_data.get('DELETE'):
                success_count += 1 if form.cleaned_data['is_success'] else 0
                total_count += 1
        if success_count == 0:
            raise ValidationError('Должен быть хотя бы 1 правильный вариант!')
        if success_count == total_count:
            raise ValidationError('Все варианты не могут быть правильными!')
