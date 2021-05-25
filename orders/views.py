from django.shortcuts import render, redirect

from accounts.forms import UserAdminCreationForm



# @login_required()
def registerView(req):
    form = UserAdminCreationForm()
    if req.method == 'POST':
        form = UserAdminCreationForm(req.POST)
        if form.is_valid():
            form.save()
            return redirect('profile')
    return render(req, 'accounts/register.html', {'form': form})
