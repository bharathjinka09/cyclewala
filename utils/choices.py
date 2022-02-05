from djchoices import ChoiceItem, DjangoChoices


class GenderType(DjangoChoices):
        Male = ChoiceItem("M")
        Female = ChoiceItem("F")
        Other = ChoiceItem("O")

