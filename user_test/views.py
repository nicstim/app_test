from django.shortcuts import redirect
from django.views.generic import TemplateView
from user_test.models import Test, TestQuestion, UserTest, Answer
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data()

        context['tests'] = Test.objects.all()

        return context


class TestView(TemplateView):
    template_name = 'test.html'

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("/")
        try:
            test = Test.objects.get(id=kwargs.get('pk'))
            if not test.question.exists():
                return redirect("/")
        except Test.DoesNotExist:
            return redirect("/")
        return super().get(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(TestView, self).get_context_data()
        page_num = self.request.GET.get('page', 1)
        test = Test.objects.get(id=kwargs.get('pk'))
        user_test = UserTest.get_user_test(self.request.user.id, test.id)
        if page_num == 'result' or user_test.last_question_id == test.question.last().id:
            context['success_answer'] = user_test.test_result.get('success_answer')
            context['wrong_answer'] = user_test.test_result.get('wrong_answer')
            context['percent'] = user_test.test_result.get('success_answer') / user_test.test_result.get('total_answer')

        else:
            if user_test.last_question_id:
                question_list = TestQuestion.objects.filter(id__gt=user_test.last_question_id, test_id=test.id)
            else:
                question_list = TestQuestion.objects.filter(test_id=test.id)
            paginator = Paginator(question_list, 1)
            try:
                questions = paginator.page(page_num)
            except PageNotAnInteger:
                questions = paginator.page(1)
            except EmptyPage:
                questions = paginator.page(paginator.num_pages)

            if not questions.object_list[0].id == question_list.first().id:
                paginator = Paginator(question_list, 1)
                questions = paginator.page(1)

            context["questions"] = questions
        return context

    def post(self, request, **kwargs):
        data = request.POST
        user_test = UserTest.get_user_test(request.user.id, kwargs.get('pk'))
        if data.get("answer"):
            for item in data.getlist('answer'):
                user_test.answer.add(Answer.objects.get(id=item))
            return redirect(f"/test/{kwargs.get('pk')}?page={data.get('next')}")
        else:
            return redirect(f"/test/{kwargs.get('pk')}?page={data.get('page')}")
