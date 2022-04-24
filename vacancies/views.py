from django.db.models import Count
from django.http import Http404
from django.shortcuts import render

from django.views.generic import TemplateView

from vacancies.models import Vacancy, Company, Specialty


class MainView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super(MainView, self).get_context_data(**kwargs)
        context['specialties'] = Specialty.objects.annotate(vacancies_count=Count('vacancies'))
        context['companies'] = Company.objects.annotate(vacancies_count=Count('vacancies'))
        return context


class ListSpecialtyVacancyView(TemplateView):
    template_name = "vacancies.html"

    def get_context_data(self, **kwargs):
        context = super(ListSpecialtyVacancyView, self).get_context_data(**kwargs)
        specialty_code = kwargs['specialty_code']
        try:
            specialty = Specialty.objects.get(code=specialty_code)
            vacancies = Vacancy.objects.filter(specialty__code=specialty_code)
            context['specialty'] = specialty
            context['vacancies'] = vacancies
        except Specialty.DoesNotExist:
            raise Http404(f"specialty code={specialty_code} not found")
        return context


class ListAllVacancyView(TemplateView):
    template_name = "vacancies.html"

    def get_context_data(self, **kwargs):
        context = super(ListAllVacancyView, self).get_context_data(**kwargs)
        context['vacancies'] = Vacancy.objects.all()
        return context


class CompanyView(TemplateView):
    template_name = "company.html"

    def get_context_data(self, **kwargs):
        context = super(CompanyView, self).get_context_data(**kwargs)
        company_id = int(self.kwargs['company_id'])
        try:
            context['company'] = Company.objects.get(id=company_id)
            context['vacancies'] = Vacancy.objects.filter(company__id=company_id)
        except Company.DoesNotExist:
            raise Http404(f"company id={company_id} not found")
        return context


class VacancyView(TemplateView):
    template_name = "vacancy.html"

    def get_context_data(self, **kwargs):
        context = super(VacancyView, self).get_context_data(**kwargs)
        vacancy_id = int(self.kwargs['vacancy_id'])
        try:
            context['vacancy'] = Vacancy.objects.get(id=vacancy_id)
        except Vacancy.DoesNotExist:
            raise Http404(f"vacancy id={vacancy_id} not found")
        return context


def custom_handler404(request, exception):
    return render(request, 'page404.html', context={'exception': exception})


def custom_handler500(request):
    return render(request, 'page500.html', status=500)
