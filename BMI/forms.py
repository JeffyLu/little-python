from django import forms

#构造信息表单
class BMIForm(forms.Form):
    age = forms.IntegerField(
        label = '年龄',
        min_value = 1,
        error_messages = {'required' : '请填写年龄!'},
        widget = forms.NumberInput(
            attrs = {
                'placeholder' : '1-150岁',
                'size' : '20',
                'title' : '请填写年龄!',
            }
        ),
    )

    GENDER_CHOICE = (('男', '男'), ('女', '女'))
    gender = forms.CharField(
        label = '性别',
        error_messages = {'required' : '请选择性别!'},
        widget = forms.Select(
            choices = GENDER_CHOICE
        ),
    )

    height = forms.DecimalField(
        label = '身高',
        min_value = 20,
        error_messages = {'required' : '请填写身高!'},
        max_digits = 4,
        decimal_places = 1,
        widget = forms.NumberInput(
            attrs = {
                'placeholder' : '单位:cm',
                'size' : '20',
                'title' : '请填写身高!',
            }
        ),
    )

    weight = forms.DecimalField(
        label = '体重',
        min_value = 1,
        error_messages = {'required' : '请填写体重!'},
        max_digits = 4,
        decimal_places = 1,
        widget = forms.NumberInput(
            attrs = {
                'placeholder' : '单位:g',
                'size' : '20',
                'title' : '请填写体重!',
            }
        ),
    )

    #处理脏数据
    def clean_age(self):
        age = self.cleaned_data['age']
        if age <= 0 or age > 150:
            raise forms.ValidationError("请填写有效的年龄(1-150).")
        return age

    def clean_height(self):
        height = self.cleaned_data['height']
        if height <= 20 or height > 300:
            raise forms.ValidationError("请填写有效的身高(单位:cm).")
        return height

    def clean_weight(self):
        weight = self.cleaned_data['weight']
        if weight <= 0 or weight > 500:
            raise forms.ValidationError("请填写有效的体重(单位:g).")
        return weight
