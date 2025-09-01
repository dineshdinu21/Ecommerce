from django import forms
from .models import CustomUser,Products,PlaceOrder
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator


password_validator = RegexValidator(
    regex=r'^(?=.*\d)(?=.*[!@#$%^&*(),.?":{}|<>])',
    message='Password must contain at least one digit and one special character.'
)

class UserForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Password', 'id': 'password'})
        )
    password2 = forms.CharField(
        label="Confirm Password", 
        widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': 'Confirm Password','id':'confirm_password'}),
        required=True
    )
    user_profile = forms.ImageField(
        error_messages={
            'invalid_image': 'Please upload a valid image file (jpg, jpeg, png, svg).'
        }
    )
    class Meta:
        model = CustomUser
        fields = ['user_profile','username', 'password', 'password2', 'first_name', 'last_name', 'address', 'email', 'mobile']

        widgets={
            'username':forms.TextInput(attrs={'class': 'form-control','placeholder': 'User Name'}),
            'first_name':forms.TextInput(attrs={'class': 'form-control','placeholder': 'First Name'}),
            'last_name':forms.TextInput(attrs={'class': 'form-control','placeholder': 'Last Name'}),
            'address':forms.TextInput(attrs={'class': 'form-control','placeholder': 'Address'}),
            'email': forms.EmailInput(attrs={'class': 'form-control','placeholder': 'Email'}),
            'mobile':forms.TextInput(attrs={'class':'form-control','placeholder': 'Mobile Number', 'maxlength': 14})
            }

    def clean_password2(self):
        password1 = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match. Please try again.")
        
        password_validator(password1)

        try:
            validate_password(password1, user=self.instance)
        except ValidationError as e:
            self.add_error('password', e)

        return password2
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if get_user_model().objects.filter(username=username).exists():
            raise ValidationError('Username already exists. Please choose another.')
        return username
    

class LoginForm(forms.ModelForm):
     class Meta:
        model = CustomUser
        fields = ['username','password']
        widgets={
            'username':forms.TextInput(attrs={'class': 'form-control','placeholder': 'User Name'}),
            'password':forms.PasswordInput(attrs={'class': 'form-control','placeholder': 'Password','id':'password'}),
        }


class SellerForm(forms.ModelForm):
    password2 = forms.CharField(
        label="Confirm Password", 
        widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': 'Conform Password','id':'confirm_password'})
    )

    class Meta:
        model = CustomUser
        fields = ['seller_profile','username', 'password', 'password2', 'first_name', 'last_name', 'address', 'email', 'mobile']

        widgets={
            'username':forms.TextInput(attrs={'class': 'form-control','placeholder': 'User Name'}),
            'password':forms.PasswordInput(attrs={'class': 'form-control','placeholder': 'Password','id':'password'}),
            'first_name':forms.TextInput(attrs={'class': 'form-control','placeholder': 'First Name'}),
            'last_name':forms.TextInput(attrs={'class': 'form-control','placeholder': 'Last Name'}),
            'address':forms.TextInput(attrs={'class': 'form-control','placeholder': 'Address'}),
            'email': forms.EmailInput(attrs={'class': 'form-control','placeholder': 'Email'}),
            'mobile':forms.TextInput(attrs={'class':'form-control','placeholder': 'Mobile Number', 'maxlength': 14})
            }

    def clean_password2(self):
        password1 = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match. Please try again.")
        try:
            validate_password(password1, user=self.instance)
        except ValidationError as e:
            self.add_error('password', e)

        return password2
    

class SellerLoginForm(forms.ModelForm):
     class Meta:
        model = CustomUser
        fields = ['username','password']
        widgets={
            'username':forms.TextInput(attrs={'class': 'form-control','placeholder': 'User Name'}),
            'password':forms.PasswordInput(attrs={'class': 'form-control','placeholder': 'Password','id':'password'}), 

        }

class ProductsAddingForm(forms.ModelForm):
    class Meta:
        model=Products
        fields='__all__'
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'form-control','placeholder': 'Choose an image'}),
            'product_name': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter product name'}),
            'colour': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter color'}),
            'description': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter product description'}),
            'price': forms.NumberInput(attrs={'class': 'form-control','placeholder': 'Enter price'}),
            'discount': forms.NumberInput(attrs={'class': 'form-control','placeholder': 'Enter discount (e.g. 10%)'}),
            'delivery_charge': forms.NumberInput(attrs={'class': 'form-control','placeholder': 'Enter delivery charge'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control','placeholder': 'Enter stock quantity'}),
        }
        exclude=['seller']


CustomUser = get_user_model()

class ResetPasswordForm(forms.Form):

    old_password = forms.CharField(
        label="Old Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Old password','id':'reset_old_password'})
    )
    
    new_password = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'New password','id':'reset_new_password'})
    )
    confirm_password = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm password','id':'reset_confirm_password'})
    )

    def clean(self):
        cleaned_data = super().clean()
        new_password = self.cleaned_data.get('new_password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if new_password != confirm_password:
            print(new_password,confirm_password,
                  'Password doesnot Match')
            self.add_error('new_password',"Passwords do not match.")

        try:
            password_validator(new_password)
            print('validation error')
            validate_password(new_password)
            
        except ValidationError as e:
            self.add_error('new_password', e)

        return cleaned_data
    
class PlaceOrderForm(forms.ModelForm):
    class Meta:
        model=PlaceOrder
        exclude = ['user','product','quantity','price']
        widgets = {
            'name':forms.TextInput(attrs={'class': 'form-control'}),
            'door_no':forms.TextInput(attrs={'class': 'form-control'}),
            'street_name':forms.TextInput(attrs={'class': 'form-control'}),
            'city_name': forms.TextInput(attrs={'class': 'form-control'}),
            'zip_code':forms.TextInput(attrs={'class': 'form-control'}),
            'mobile':forms.TextInput(attrs={'class': 'form-control'}),
            'district':forms.TextInput(attrs={'class': 'form-control'}),
            'state':forms.TextInput(attrs={'class': 'form-control'}),
            'country':forms.TextInput(attrs={'class': 'form-control'}),
            'payment_option':forms.TextInput(attrs={'class': 'form-control'}),
        }
        
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None) 
        super().__init__(*args, **kwargs)
        if user:
            self.fields['city_name'].initial = user.address
            self.fields['name'].initial = user.username
            self.fields['mobile'].initial = user.mobile
    

