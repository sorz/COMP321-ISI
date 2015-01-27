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
        fields = ['point', 'product']
        widgets = {
            'point': forms.RadioSelect(choices=RATING_CHOICES),
            'product': forms.HiddenInput()
        }

    def clean_point(self):
        point = self.cleaned_data.get('point')
        if point not in (1, 2, 3, 4, 5):
            raise forms.ValidationError('Point must be choose from 1 to 5.',
                                        code='invalid-point')
        return point

    def clean(self):
        cleaned_data = super().clean()
        product = cleaned_data.get('product')

        if not product.has_bought_by_user(self.instance.user):
            raise forms.ValidationError('Cannot rating before buy it.',
                                        code='no-purchase-yet')
        return cleaned_data