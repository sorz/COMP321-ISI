from django import forms

from .models import Rating


RATING_CHOICES = (
    (1, '1 Horrible'),
    (2, '2 Bad'),
    (3, '3 Fair'),
    (4, '4 Good'),
    (5, '5 Fantastic')
)


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['point']
        widgets = {
            'point': forms.RadioSelect(choices=RATING_CHOICES),
        }

    def clean_point(self):
        point = self.cleaned_data.get('point')
        if point not in (1, 2, 3, 4, 5):
            raise forms.ValidationError('Point must be chosen from 1 to 5.',
                                        code='invalid-point')
        return point

    def clean(self):
        cleaned_data = super().clean()

        if not self.instance.product.has_bought_by_user(self.instance.user):
            raise forms.ValidationError('Cannot rate before buying it.',
                                        code='no-purchase-yet')
        return cleaned_data