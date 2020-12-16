from django.shortcuts import render
from solver.models import BoxValue, Parent
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.views import generic
from django.urls import reverse_lazy, reverse
from solver.forms import BoxFormSet, BoxValueFormSet
from .moonsolver.solver import solve_puzzle
import uuid


# Create your views here.
def index(request):

    if request.method == 'POST':
        formset = BoxFormSet(request.POST)

    else:
        formset = BoxFormSet()
        # removed: queryset=BoxValue.objects.none()

    context = {
        'formset': formset,

    }

    return render(request, 'index.html', context=context)


class PuzzleSolutionView(generic.DetailView):
    model = Parent
    template_name = 'solver/puzzle_solution.html'

    def get_context_data(self, **kwargs):
        context = super(PuzzleSolutionView, self).get_context_data(**kwargs)
        parent = self.object
        if parent.solved:
            context['fancy_solution'] = zip(parent.puzzle_solution, parent.puzzle_string)
        if parent.multiple_solution:
            context['fancy_multi_fill_1'] = zip(parent.multi_fill_1, parent.puzzle_string)
            context['fancy_multi_fill_2'] = zip(parent.multi_fill_2, parent.puzzle_string)
        if parent.no_solution:
            context['fancy_solve_attempt'] = zip(parent.solve_attempt, parent.puzzle_string)
        return context

    def get_object(self, queryset=None):
        return Parent.objects.get(uuid=self.kwargs.get('uuid'))


class PuzzleBlankView(generic.DetailView):
    model = Parent
    template_name = 'solver/puzzle_blank.html'

    def get_object(self, queryset=None):
        return Parent.objects.get(uuid=self.kwargs.get('uuid'))


class PuzzleCreate(generic.edit.CreateView):
    model = Parent
    fields = ['name']
    template_name = 'solver/puzzle_create.html'

    def get_success_url(self):
        return reverse('puzzle-entry', kwargs={'uuid': self.object.uuid})


def enter_puzzle(request, uuid):
    parent = get_object_or_404(Parent, uuid=uuid)
    name = parent.name

    if request.method == 'POST':
        formset = BoxValueFormSet(request.POST, instance=parent)

        if formset.is_valid():
            formset.save()
            value_list = [0] * 81

            for box in BoxValue.objects.filter(parent=parent):
                if box.box_value:
                    box_string = box.box_value
                else:
                    box_string = '0'
                value_list[box.box_index] = box_string

            parent.puzzle_string = ''.join(value_list)
            parent.save()

            puzzle = solve_puzzle(parent.puzzle_string, parent.name)
            parent.solved = puzzle.solved
            parent.no_solution = puzzle.no_solution
            parent.initialized = puzzle.initialized
            parent.multiple_solution = puzzle.multiple_solution
            parent.too_few_clues = puzzle.too_few_clues
            parent.error_description = puzzle.error_description
            parent.puzzle_solution = puzzle.solution
            parent.difficulty = puzzle.difficulty
            parent.solve_attempt = puzzle.final_string
            if puzzle.multiple_solution:
                parent.multi_fill_1 = puzzle.valid_completion_list[0]
                parent.multi_fill_2 = puzzle.valid_completion_list[1]
            parent.save()
            return HttpResponseRedirect(reverse('puzzle-blank', kwargs={'uuid': parent.uuid}))
        else:
            print(formset.errors)

    else:
        formset = BoxValueFormSet(instance=parent)

    context = {'formset': formset, 'name': name}

    return render(request, 'solver/puzzle_entry.html', context)
