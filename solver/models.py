from django.db import models
from django.core.validators import RegexValidator
from .moonsolver.solver import simple_solve
import uuid


class BoxValue(models.Model):
    """ A single box in a sudoku puzzle. Is either blank or contains a number 1-9."""
    digits = RegexValidator('[1-9]', 'Only numbers from 1 to 9 allowed')

    box_value = models.CharField(max_length=1, validators=[digits],
                                 help_text="Enter only values between 1 and 9 or leave blank",
                                 null=True, blank=True)

    box_index = models.IntegerField()

    parent = models.ForeignKey('Parent', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return str(self.box_index) + " - " + str(self.box_value)


class Parent(models.Model):
    """ The puzzle as entered into the system has mostly default values that are filled
    after attempting to solve the puzzle"""

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, serialize=False, editable=False)
    name = models.CharField(max_length=100, null=True, blank=True)
    create_string = models.BooleanField(default=False)
    puzzle_string = models.CharField(max_length=81, default="0" * 81)
    try_solve = models.BooleanField(default=False)
    solved = models.BooleanField(default=False)
    too_few_clues = models.BooleanField(default=False)
    no_solution = models.BooleanField(default=False)
    multiple_solution = models.BooleanField(default=False)
    multi_fill_1 = models.CharField(max_length=81, default="0" * 81)
    multi_fill_2 = models.CharField(max_length=81, default="0" * 81)
    puzzle_solution = models.CharField(max_length=81, default="0" * 81)
    error_description = models.CharField(max_length=100, default="", blank=True)
    difficulty = models.CharField(max_length=20, default='', blank=True)

    def save(self, *args, **kwargs):
        not_created = not self.uuid
        print("Not created")
        if self.try_solve:
            self.solved, self.puzzle_solution = simple_solve(self.puzzle_string, self.name)
            self.try_solve = False
        if self.create_string:
            value_list = [0]*81
            for box in BoxValue.objects.filter(parent=self):
                box_string = box.box_value if box.box_value else '0'
                value_list[box.box_index] = box_string
            self.puzzle_string = ''.join(value_list)
            self.create_string = False

        super().save(*args, **kwargs)
        # if not_created:
        #     print("Second not created")
        #     for i in range(0, 81):
        #         BoxValue.objects.create(parent=self, box_index=i)

    def __str__(self):
        return self.name
